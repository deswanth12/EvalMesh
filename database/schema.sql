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

CREATE TABLE IF NOT EXISTS organization_members (
    user_id VARCHAR(64) REFERENCES users(id),
    organization_id VARCHAR(64) REFERENCES organizations(id),
    role VARCHAR(50) DEFAULT 'developer',
    joined_at DOUBLE PRECISION DEFAULT EXTRACT(EPOCH FROM NOW()),
    PRIMARY KEY (user_id, organization_id)
);

CREATE TABLE IF NOT EXISTS api_keys (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) DEFAULT 'Developer Key',
    description TEXT,
    user_id VARCHAR(64) REFERENCES users(id),
    organization_id VARCHAR(64) REFERENCES organizations(id),
    key_hash VARCHAR(255) UNIQUE NOT NULL,
    scopes TEXT DEFAULT 'chat:read,chat:write,evaluate:run',
    expires_at DOUBLE PRECISION,
    last_used DOUBLE PRECISION,
    revoked BOOLEAN DEFAULT FALSE,
    created_at DOUBLE PRECISION DEFAULT EXTRACT(EPOCH FROM NOW())
);

CREATE TABLE IF NOT EXISTS sessions (
    id VARCHAR(64) PRIMARY KEY,
    user_id VARCHAR(64) REFERENCES users(id),
    refresh_token_hash VARCHAR(255) NOT NULL,
    user_agent VARCHAR(255),
    ip_address VARCHAR(45),
    last_seen_at DOUBLE PRECISION,
    expires_at DOUBLE PRECISION NOT NULL,
    revoked_at DOUBLE PRECISION,
    created_at DOUBLE PRECISION DEFAULT EXTRACT(EPOCH FROM NOW())
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id VARCHAR(64) PRIMARY KEY,
    request_id VARCHAR(64),
    actor VARCHAR(255) NOT NULL,
    organization_id VARCHAR(64) REFERENCES organizations(id),
    action VARCHAR(255) NOT NULL,
    resource VARCHAR(255),
    result VARCHAR(50) DEFAULT 'SUCCESS',
    ip_address VARCHAR(45),
    details TEXT,
    created_at DOUBLE PRECISION DEFAULT EXTRACT(EPOCH FROM NOW())
);


