-- EvalMesh PostgreSQL 15 Enterprise Database Schema
-- Production Schema for Multi-Tenant AI Operations Platform

CREATE TABLE IF NOT EXISTS organizations (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    plan VARCHAR(50) DEFAULT 'enterprise',
    sso_enabled BOOLEAN DEFAULT TRUE,
    created_at DOUBLE PRECISION DEFAULT EXTRACT(EPOCH FROM NOW())
);

CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(64) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'developer',
    organization_id VARCHAR(64) REFERENCES organizations(id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at DOUBLE PRECISION DEFAULT EXTRACT(EPOCH FROM NOW())
);

CREATE TABLE IF NOT EXISTS agents (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    version VARCHAR(50) DEFAULT 'v1.0.0',
    model VARCHAR(100) DEFAULT 'gpt-4o',
    environment VARCHAR(50) DEFAULT 'production',
    status VARCHAR(50) DEFAULT 'ACTIVE',
    created_at DOUBLE PRECISION DEFAULT EXTRACT(EPOCH FROM NOW())
);

CREATE TABLE IF NOT EXISTS telemetry_spans (
    id VARCHAR(64) PRIMARY KEY,
    session_id VARCHAR(64) NOT NULL,
    agent_id VARCHAR(64) REFERENCES agents(id),
    latency_ms DOUBLE PRECISION NOT NULL,
    tokens_used INT DEFAULT 0,
    cost_usd DOUBLE PRECISION DEFAULT 0.0,
    waf_blocked BOOLEAN DEFAULT FALSE,
    pii_redact_count INT DEFAULT 0,
    created_at DOUBLE PRECISION DEFAULT EXTRACT(EPOCH FROM NOW())
);

CREATE TABLE IF NOT EXISTS api_keys (
    id VARCHAR(64) PRIMARY KEY,
    user_id VARCHAR(64) REFERENCES users(id),
    organization_id VARCHAR(64) REFERENCES organizations(id),
    key_hash VARCHAR(255) UNIQUE NOT NULL,
    permissions VARCHAR(255) DEFAULT 'developer',
    last_used DOUBLE PRECISION,
    created_at DOUBLE PRECISION DEFAULT EXTRACT(EPOCH FROM NOW())
);

CREATE TABLE IF NOT EXISTS sessions (
    id VARCHAR(64) PRIMARY KEY,
    user_id VARCHAR(64) REFERENCES users(id),
    refresh_token_hash VARCHAR(255) NOT NULL,
    device VARCHAR(255),
    ip_address VARCHAR(45),
    expires_at DOUBLE PRECISION NOT NULL,
    created_at DOUBLE PRECISION DEFAULT EXTRACT(EPOCH FROM NOW())
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id VARCHAR(64) PRIMARY KEY,
    user_id VARCHAR(64) REFERENCES users(id),
    action VARCHAR(255) NOT NULL,
    details TEXT,
    created_at DOUBLE PRECISION DEFAULT EXTRACT(EPOCH FROM NOW())
);

