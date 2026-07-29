from sdk.python.evalmesh_sdk import EvalMeshClient

def main():
    client = EvalMeshClient(proxy_url="http://localhost:8000", api_key="em_live_12345")

    print("1. Checking Proxy Health...")
    health = client.get_health()
    print(f"Health Status: {health['status']} | Version: {health['version']}")

    print("\n2. Fetching AI Reliability Score...")
    reliability = client.get_reliability_score()
    print(f"Overall Reliability Score: {reliability['score']}/100 ({reliability['status']})")

    print("\n3. Sending Chat Completion Prompt...")
    response = client.create_chat_completion(
        messages=[{"role": "user", "content": "What is our customer shipping policy?"}],
        agent_role="support_agent",
        model="gpt-4o"
    )
    print(f"Proxy Response: {response}")

if __name__ == "__main__":
    main()
