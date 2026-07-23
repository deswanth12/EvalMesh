import uvicorn
import argparse

def main():
    parser = argparse.ArgumentParser(description="EvalMesh: Cloudflare & GitHub Actions for AI Agents")
    parser.add_argument("--host", default="0.0.0.0", help="Host address to bind proxy server")
    parser.add_argument("--port", type=int, default=8000, help="Port to run proxy server on")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")

    args = parser.parse_args()

    print("=" * 65)
    print(" 🚀 EvalMesh: Cloudflare & GitHub Actions for AI Agents (v0.1.0)")
    print("=" * 65)
    print(f" ► Proxy Gateway Listening on : http://{args.host}:{args.port}")
    print(f" ► Target LLM Endpoint      : https://api.openai.com/v1")
    print(f" ► Active Shield Rules       : PII DLP | WAF Security | Tool RBAC | CircuitBreaker")
    print("=" * 65)

    uvicorn.run("evalmesh.proxy:app", host=args.host, port=args.port, reload=args.reload)

if __name__ == "__main__":
    main()
