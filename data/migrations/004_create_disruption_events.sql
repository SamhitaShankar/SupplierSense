CREATE TABLE IF NOT EXISTS disruption_events (
    event_id VARCHAR(40) PRIMARY KEY,
    run_id VARCHAR(64) REFERENCES run_audit_log(run_id) ON DELETE SET NULL,
    supplier_id VARCHAR(20) REFERENCES supplier_master(supplier_id) ON DELETE SET NULL,
    signal_id VARCHAR(40) NOT NULL,
    event_type VARCHAR(30) NOT NULL CHECK (event_type IN ('weather', 'financial', 'geo', 'shipping', 'regulatory', 'social')),
    source VARCHAR(80) NOT NULL,
    severity NUMERIC(4,3) NOT NULL CHECK (severity >= 0 AND severity <= 1),
    confidence NUMERIC(4,3) NOT NULL CHECK (confidence >= 0 AND confidence <= 1),
    affected_region VARCHAR(150) NOT NULL,
    affected_commodities TEXT[] NOT NULL,
    raw_text TEXT NOT NULL,
    detected_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_disruption_events_run_id ON disruption_events(run_id);
CREATE INDEX IF NOT EXISTS idx_disruption_events_supplier_id ON disruption_events(supplier_id);
CREATE INDEX IF NOT EXISTS idx_disruption_events_event_type ON disruption_events(event_type);
CREATE INDEX IF NOT EXISTS idx_disruption_events_detected_at ON disruption_events(detected_at);