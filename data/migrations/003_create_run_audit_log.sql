CREATE TABLE IF NOT EXISTS run_audit_log (
    run_id VARCHAR(64) PRIMARY KEY,
    triggered_by VARCHAR(100) NOT NULL,
    started_at TIMESTAMPTZ NOT NULL,
    ended_at TIMESTAMPTZ,
    agents_executed TEXT[] NOT NULL DEFAULT '{}',
    final_severity VARCHAR(20) NOT NULL CHECK (final_severity IN ('low', 'medium', 'high', 'critical', 'none')),
    total_revenue_at_risk_inr NUMERIC(14,2) NOT NULL DEFAULT 0 CHECK (total_revenue_at_risk_inr >= 0),
    actions_generated INT NOT NULL DEFAULT 0 CHECK (actions_generated >= 0),
    alerts_sent TEXT[] NOT NULL DEFAULT '{}',
    error_count INT NOT NULL DEFAULT 0 CHECK (error_count >= 0),
    status VARCHAR(20) NOT NULL DEFAULT 'running' CHECK (status IN ('running', 'completed', 'escalated', 'failed')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_run_audit_log_started_at ON run_audit_log(started_at);
CREATE INDEX IF NOT EXISTS idx_run_audit_log_final_severity ON run_audit_log(final_severity);
CREATE INDEX IF NOT EXISTS idx_run_audit_log_status ON run_audit_log(status);