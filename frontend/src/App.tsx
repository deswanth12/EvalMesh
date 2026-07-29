import React, { useState, useEffect } from 'react';

export default function App() {
  const [reliabilityScore, setReliabilityScore] = useState<number>(94);
  const [latencyMs, setLatencyMs] = useState<number>(12);

  useEffect(() => {
    fetch('/api/reliability')
      .then(res => res.json())
      .then(data => {
        if (data.score) setReliabilityScore(data.score);
      })
      .catch(() => {});

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const ws = new WebSocket(`${protocol}//${window.location.host}/ws`);
    ws.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data);
        if (payload.latency_ms) setLatencyMs(payload.latency_ms);
      } catch (e) {}
    };
    return () => ws.close();
  }, []);

  return (
    <div style={{ background: '#0b0f17', color: '#f9fafb', minHeight: '100vh', padding: '2rem', fontFamily: 'Inter, sans-serif' }}>
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '1.5rem', fontWeight: 800 }}>🛡️ EvalMesh Control Plane</h1>
        <span style={{ padding: '0.4rem 0.8rem', background: 'rgba(16, 185, 129, 0.1)', color: '#10b981', border: '1px solid rgba(16, 185, 129, 0.3)', borderRadius: '9999px', fontSize: '0.8rem' }}>
          Gateway Online ({latencyMs}ms)
        </span>
      </header>

      <main>
        <div style={{ background: '#111827', border: '1px solid #1f2937', borderRadius: '12px', padding: '1.5rem', marginBottom: '2rem' }}>
          <h2 style={{ fontSize: '1rem', color: '#9ca3af', textTransform: 'uppercase', marginBottom: '0.5rem' }}>Signature Metric</h2>
          <div style={{ fontSize: '3.5rem', fontWeight: 900, color: '#8b5cf6' }}>{reliabilityScore}/100</div>
          <p style={{ color: '#9ca3af', fontSize: '0.9rem' }}>Overall AI Agent Reliability & Security Scorecard</p>
        </div>
      </main>
    </div>
  );
}
