/**
 * Official Standalone EvalMesh TypeScript Client SDK (@evalmesh/sdk).
 */

export interface EvalMeshConfig {
  proxyUrl?: string;
  apiKey?: string;
}

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export class EvalMeshClient {
  private proxyUrl: string;
  private apiKey?: string;

  constructor(config: EvalMeshConfig = {}) {
    this.proxyUrl = (config.proxyUrl || 'http://localhost:8000').replace(/\/$/, '');
    this.apiKey = config.apiKey;
  }

  async getHealth(): Promise<Record<string, any>> {
    const res = await fetch(`${this.proxyUrl}/health`);
    return await res.json();
  }

  async getReliabilityScore(): Promise<Record<string, any>> {
    const res = await fetch(`${this.proxyUrl}/api/reliability`);
    return await res.json();
  }

  async createChatCompletion(messages: ChatMessage[], agentRole: string = 'support_agent', model: string = 'gpt-4o'): Promise<Record<string, any>> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      'x-evalmesh-agent-role': agentRole
    };
    if (this.apiKey) {
      headers['Authorization'] = `Bearer ${this.apiKey}`;
    }

    const res = await fetch(`${this.proxyUrl}/v1/chat/completions`, {
      method: 'POST',
      headers,
      body: JSON.stringify({ model, messages })
    });

    return await res.json();
  }
}
