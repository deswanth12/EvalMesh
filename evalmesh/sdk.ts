/**
 * EvalMesh TypeScript / JavaScript Client SDK
 * Official SDK for routing AI Agent LLM calls through EvalMesh Proxy Gateway.
 */

export interface EvalMeshMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export interface EvalMeshOptions {
  baseUrl?: string;
  apiKey?: string;
}

export interface ChatCompletionRequest {
  messages: EvalMeshMessage[];
  model?: string;
  agentRole?: string;
  promptVersion?: string;
  tools?: any[];
}

export interface ChatCompletionResponse {
  id: string;
  object: string;
  created: number;
  model: string;
  choices: Array<{
    index: number;
    message: EvalMeshMessage;
    finish_reason: string;
  }>;
  usage?: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
  _evalmesh_meta?: {
    latency_ms: number;
    prompt_version: string;
    agent_role: string;
    redactions_count: number;
    cache_hit?: boolean;
  };
}

export class EvalMeshClient {
  private baseUrl: string;
  private apiKey: string;

  constructor(options: EvalMeshOptions = {}) {
    this.baseUrl = (options.baseUrl || 'http://localhost:8000').replace(/\/$/, '');
    this.apiKey = options.apiKey || 'em_live_demo_123456789';
  }

  async createChatCompletion(request: ChatCompletionRequest): Promise<ChatCompletionResponse> {
    const url = `${this.baseUrl}/v1/chat/completions`;
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${this.apiKey}`,
      'x-evalmesh-agent-role': request.agentRole || 'support_agent',
      'x-evalmesh-prompt-version': request.promptVersion || 'v1.0.0'
    };

    const body = {
      model: request.model || 'gpt-4o',
      messages: request.messages,
      tools: request.tools
    };

    const response = await fetch(url, {
      method: 'POST',
      headers,
      body: JSON.stringify(body)
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`EvalMesh Proxy Error (${response.status}): ${errorText}`);
    }

    return (await response.json()) as ChatCompletionResponse;
  }
}
