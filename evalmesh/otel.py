import time
import json
from typing import Dict, Any

class OpenTelemetryTraceExporter:
    """
    OpenTelemetry (OTel) Exporter for EvalMesh.
    Formats agent proxy transactions into standard W3C / OTel trace spans 
    for seamless integration into Datadog, Grafana Tempo, and Dynatrace.
    """

    @classmethod
    def create_span(
        self,
        session_id: str,
        agent_role: str,
        prompt_version: str,
        model: str,
        latency_ms: float,
        status_code: int,
        waf_blocked: bool = False,
        pii_redacted_count: int = 0
    ) -> Dict[str, Any]:
        
        now_ns = int(time.time() * 1e9)
        duration_ns = int(latency_ms * 1e6)

        return {
            "trace_id": f"evalmesh_{session_id}_{int(time.time())}",
            "span_id": f"span_{int(time.time()*1000)}",
            "name": f"evalmesh.proxy/{model}",
            "kind": "SPAN_KIND_SERVER",
            "start_time_unix_nano": now_ns - duration_ns,
            "end_time_unix_nano": now_ns,
            "attributes": {
                "service.name": "evalmesh-agent-gateway",
                "evalmesh.agent_role": agent_role,
                "evalmesh.prompt_version": prompt_version,
                "evalmesh.model": model,
                "evalmesh.latency_ms": latency_ms,
                "evalmesh.status_code": status_code,
                "evalmesh.waf_blocked": waf_blocked,
                "evalmesh.pii_redactions": pii_redacted_count,
                "http.status_code": status_code
            },
            "status": {
                "code": "STATUS_CODE_OK" if status_code == 200 else "STATUS_CODE_ERROR"
            }
        }
