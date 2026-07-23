import time
import json
import httpx
import os
from typing import Optional
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse, FileResponse
import os

from evalmesh.dlp import PIIDLPScanner
from evalmesh.security import PromptInjectionFirewall, ToolRBACEnforcer
from evalmesh.cost_breaker import CostAndLoopCircuitBreaker
from evalmesh.dataset import GoldenDatasetGenerator
from evalmesh.drift import OutputDriftDetector
from evalmesh.ab_testing import MultiModelABEvaluator
from evalmesh.db import EvalMeshDatabase
from evalmesh.rules_engine import CustomRulesEngine
from evalmesh.auth import APIKeyManager
from evalmesh.smart_router import SmartCostRouter
from evalmesh.cache import SemanticPromptCache
from evalmesh.auto_heal import AutoHealingRetryEngine
from evalmesh.otel import OpenTelemetryTraceExporter
from evalmesh.enterprise import enterprise_engine

app = FastAPI(
    title="EvalMesh Proxy Engine",
    description="Cloudflare & GitHub Actions for AI Agents - Real-Time WAF, DLP, RBAC, Smart Caching, Auto-Healing & Evals",
    version="0.5.0"
)

# Core Component Instances
dlp_scanner = PIIDLPScanner()
security_firewall = PromptInjectionFirewall()
rbac_enforcer = ToolRBACEnforcer()
circuit_breaker = CostAndLoopCircuitBreaker()
dataset_generator = GoldenDatasetGenerator()
ab_evaluator = MultiModelABEvaluator()
db_engine = EvalMeshDatabase()
custom_rules = CustomRulesEngine()
key_manager = APIKeyManager()
smart_router = SmartCostRouter()
prompt_cache = SemanticPromptCache(similarity_threshold=0.90)
auto_healer = AutoHealingRetryEngine()
otel_exporter = OpenTelemetryTraceExporter()

UPSTREAM_OPENAI = "https://api.openai.com"
DASHBOARD_PATH = os.path.join(os.path.dirname(__file__), "dashboard", "index.html")

@app.get("/")
@app.get("/dashboard")
async def get_dashboard():
    """Serves the interactive EvalMesh Control Panel Web UI."""
    if os.path.exists(DASHBOARD_PATH):
        return FileResponse(DASHBOARD_PATH)
    return JSONResponse({"message": "EvalMesh Control Panel Dashboard"}, status_code=200)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "EvalMesh AI Agent Control Plane",
        "version": "0.5.0 (Semantic Caching & Auto-Healing Retries Enabled)"
    }

@app.post("/v1/keys/generate")
async def generate_api_key(payload: dict):
    """Generates a new enterprise EvalMesh API key (em_live_...)."""
    name = payload.get("name", "Developer Key")
    role = payload.get("role", "developer")
    rate_limit = payload.get("rate_limit", 60)
    new_key = key_manager.generate_key(name, role, rate_limit)
    return {"api_key": new_key, "name": name, "role": role, "rate_limit_per_min": rate_limit}

@app.get("/v1/telemetry/otel")
async def export_otel_spans():
    """Returns standard OpenTelemetry trace span format for Datadog / Grafana."""
    recent_logs = db_engine.get_recent_logs(limit=10)
    spans = []
    for log in recent_logs:
        span = otel_exporter.create_span(
            session_id=log.get("session_id", "default"),
            agent_role=log.get("agent_role", "support_agent"),
            prompt_version=log.get("prompt_version", "v1.0.0"),
            model=log.get("model", "gpt-4o"),
            latency_ms=log.get("latency_ms", 0.0),
            status_code=log.get("status_code", 200),
            waf_blocked=(log.get("status_code") == 403),
            pii_redacted_count=log.get("redactions_count", 0)
        )
        spans.append(span)
    return {"resourceSpans": spans}

@app.post("/v1/eval/auto-heal")
async def eval_auto_heal(payload: dict):
    """Evaluates payload for schema validity and returns auto-healing retry prompt if malformed."""
    content = payload.get("content", "")
    required_keys = payload.get("required_keys")
    is_valid, prompt_or_msg, parsed = auto_healer.validate_and_heal_json(content, required_keys)
    return {"is_valid": is_valid, "feedback": prompt_or_msg, "parsed": parsed}

@app.get("/v1/analytics/summary")
async def get_analytics_summary():
    """Returns persistent analytics summary from SQLite database."""
    return db_engine.get_summary_analytics()

@app.get("/v1/logs/recent")
async def get_recent_logs(limit: int = 20):
    """Returns recent telemetry audit logs."""
    return db_engine.get_recent_logs(limit=limit)

@app.post("/v1/eval/drift")
async def eval_drift(payload: dict):
    """Calculates semantic drift between baseline gold text and current output."""
    baseline = payload.get("baseline", "")
    output = payload.get("output", "")
    return OutputDriftDetector.compute_semantic_drift(baseline, output)

@app.post("/v1/datasets/record")
async def record_golden_pair(payload: dict):
    """Records a prompt-completion pair into the golden dataset."""
    prompt = payload.get("prompt", "")
    completion = payload.get("completion", "")
    return dataset_generator.record_pair(prompt, completion, payload.get("metadata"))

@app.post("/v1/chat/completions")
async def proxy_chat_completions(request: Request):
    """
    Main Reverse Proxy Gateway for OpenAI / LLM chat completion calls.
    Performs API Key Auth, Smart Cost Routing, inline PII sanitization, prompt injection screening,
    tool RBAC check, loop breaker evaluation, and forwards payload to upstream provider.
    """
    start_time = time.time()
    
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload.")

    headers = dict(request.headers)
    
    # 0. API Key Authorization & Rate Limiting Check
    raw_api_key = headers.get("authorization", "").replace("Bearer ", "").strip()
    if raw_api_key and raw_api_key.startswith("em_live_"):
        is_auth_valid, auth_err, key_info = key_manager.validate_key(raw_api_key)
        if not is_auth_valid:
            raise HTTPException(status_code=429 if "rate limit" in auth_err.lower() else 401, detail=f"[EvalMesh Auth] {auth_err}")

    # Extract Custom EvalMesh Metadata Headers
    prompt_version = headers.get("x-evalmesh-prompt-version", "v1.0.0")
    agent_role = headers.get("x-evalmesh-agent-role", "support_agent")
    session_id = headers.get("x-evalmesh-session-id", "default_session")
    
    messages = body.get("messages", [])
    requested_model = body.get("model", "gpt-4o")

    # 0.1 Semantic Prompt Cache Lookup (<5ms at $0 cost)
    user_prompt_str = " ".join([str(m.get("content", "")) for m in messages if isinstance(m, dict) and m.get("role") == "user"])
    cached_resp, sim_score = prompt_cache.get(user_prompt_str)
    if cached_resp:
        latency_ms = (time.time() - start_time) * 1000
        db_engine.log_request(session_id, agent_role, prompt_version, requested_model, latency_ms, 200, "CACHE_HIT", 0)
        return JSONResponse(
            content={
                "id": "evalmesh-cached-cmpl-001",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": requested_model,
                "choices": [{
                    "index": 0,
                    "message": {"role": "assistant", "content": cached_resp},
                    "finish_reason": "stop"
                }],
                "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
                "_evalmesh_meta": {
                    "latency_ms": round(latency_ms, 2),
                    "prompt_version": prompt_version,
                    "agent_role": agent_role,
                    "cache_hit": True,
                    "cache_similarity_score": sim_score
                }
            },
            status_code=200
        )

    # Smart Cost Optimization Route
    selected_model, was_optimized, opt_reason = smart_router.optimize_route(requested_model, messages)
    if was_optimized:
        body["model"] = selected_model
        print(f"[EvalMesh SmartRouter] {opt_reason}")
    
    # 1. Circuit Breaker & Loop Detection Check
    is_valid_session, err_msg = circuit_breaker.validate_session(session_id, messages)
    if not is_valid_session:
        db_engine.log_request(session_id, agent_role, prompt_version, body.get("model", "gpt-4o"), 0.0, 429, err_msg, 0)
        raise HTTPException(status_code=429, detail=f"[EvalMesh CircuitBreaker] {err_msg}")

    # 2. Inbound Security & PII Redaction Loop
    redaction_summary = []
    for msg in messages:
        if isinstance(msg, dict) and "content" in msg:
            content = msg["content"]
            if isinstance(content, str):
                # A. Check Prompt Injection
                injection_match = security_firewall.check_injection(content)
                if injection_match:
                    db_engine.log_request(session_id, agent_role, prompt_version, body.get("model", "gpt-4o"), 0.0, 403, f"Injection: {injection_match}", 0)
                    raise HTTPException(
                        status_code=403,
                        detail=f"[EvalMesh WAF] Prompt Injection Blocked. Matched signature: '{injection_match}'."
                    )
                
                # B. Sanitize PII
                sanitized_content, redactions = dlp_scanner.sanitize(content)
                sanitized_content, custom_redactions = custom_rules.scan_custom_rules(sanitized_content)
                msg["content"] = sanitized_content
                if redactions:
                    redaction_summary.extend(redactions)
                if custom_redactions:
                    redaction_summary.extend(custom_redactions)

    # 3. Tool Permission (RBAC) Check
    tools = body.get("tools", [])
    if tools:
        violations = rbac_enforcer.authorize_tools(agent_role, tools)
        if violations:
            db_engine.log_request(session_id, agent_role, prompt_version, body.get("model", "gpt-4o"), 0.0, 403, f"RBAC: {violations}", 0)
            raise HTTPException(
                status_code=403,
                detail=f"[EvalMesh RBAC] Unauthorized tool(s) requested for role '{agent_role}': {violations}"
            )

    # 4. Strip Host Header for Upstream Request
    headers.pop("host", None)
    headers.pop("content-length", None)
    
    # 5. Execute Upstream Request or Mock Handler
    api_key = headers.get("authorization")
    if not api_key or "bearer mock" in api_key.lower():
        # Dry-run / Local Mock Mode if no live OpenAI API key is supplied
        latency_ms = (time.time() - start_time) * 1000
        db_engine.log_request(session_id, agent_role, prompt_version, body.get("model", "gpt-4o"), latency_ms, 200, None, len(redaction_summary))
        return JSONResponse(
            content={
                "id": "evalmesh-mock-cmpl-001",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": body.get("model", "gpt-4o"),
                "choices": [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": f"[EvalMesh Verified Response] Processing completed safely. Version: {prompt_version}"
                    },
                    "finish_reason": "stop"
                }],
                "usage": {"prompt_tokens": 120, "completion_tokens": 30, "total_tokens": 150},
                "_evalmesh_meta": {
                    "latency_ms": round(latency_ms, 2),
                    "prompt_version": prompt_version,
                    "agent_role": agent_role,
                    "redactions_count": len(redaction_summary)
                }
            },
            status_code=200
        )

    # Forward to real upstream OpenAI provider
    async with httpx.AsyncClient() as client:
        try:
            upstream_resp = await client.post(
                f"{UPSTREAM_OPENAI}/v1/chat/completions",
                headers=headers,
                json=body,
                timeout=60.0
            )
        except Exception as e:
            db_engine.log_request(session_id, agent_role, prompt_version, body.get("model", "gpt-4o"), 0.0, 502, str(e), len(redaction_summary))
            raise HTTPException(status_code=502, detail=f"LLM Provider Connection Error: {str(e)}")

    latency_ms = (time.time() - start_time) * 1000
    db_engine.log_request(session_id, agent_role, prompt_version, body.get("model", "gpt-4o"), latency_ms, upstream_resp.status_code, None, len(redaction_summary))
    
    # Return response payload
    return Response(
        content=upstream_resp.content,
        status_code=upstream_resp.status_code,
        media_type="application/json",
        headers={"x-evalmesh-latency-ms": f"{latency_ms:.2f}"}
    )

# --- ENTERPRISE & COMPLIANCE ENDPOINTS ---

@app.post("/v1/auth/sso/validate")
async def validate_sso(request: Request):
    body = await request.json()
    token = body.get("token", "")
    res = enterprise_engine.validate_sso_token(token)
    if not res.get("valid"):
        raise HTTPException(status_code=401, detail=res.get("error"))
    return res

@app.post("/v1/compliance/hipaa/scrub")
async def scrub_hipaa(request: Request):
    body = await request.json()
    text = body.get("text", "")
    return enterprise_engine.scrub_hipaa_phi(text)

@app.get("/v1/compliance/soc2/audit-logs")
async def export_soc2_logs():
    return {"audit_trail": enterprise_engine.export_soc2_audit_trail()}

@app.post("/v1/compliance/gdpr/forget")
async def gdpr_forget(request: Request):
    body = await request.json()
    user_id = body.get("user_id", "")
    return enterprise_engine.process_gdpr_forget_request(user_id)

