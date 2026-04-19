CREATE TABLE IF NOT EXISTS supplier_master (
    supplier_id VARCHAR(20) PRIMARY KEY,
    supplier_name VARCHAR(150) NOT NULL,
    tier INT NOT NULL CHECK (tier IN (1, 2, 3)),
    country VARCHAR(80) NOT NULL,
    region VARCHAR(120) NOT NULL,
    city VARCHAR(120) NOT NULL,
    commodities TEXT[] NOT NULL,
    primary_commodity VARCHAR(80) NOT NULL,
    lead_time_days INT NOT NULL CHECK (lead_time_days >= 0),
    contract_value_inr NUMERIC(14,2) NOT NULL CHECK (contract_value_inr >= 0),
    risk_score NUMERIC(4,3) NOT NULL DEFAULT 0.000 CHECK (risk_score >= 0 AND risk_score <= 1),
    historical_disruptions INT NOT NULL DEFAULT 0 CHECK (historical_disruptions >= 0),
    avg_recovery_days NUMERIC(6,2) NOT NULL DEFAULT 0 CHECK (avg_recovery_days >= 0),
    contact_name VARCHAR(120) NOT NULL,
    contact_email VARCHAR(150) NOT NULL,
    contact_phone VARCHAR(30) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_supplier_master_country ON supplier_master(country);
CREATE INDEX IF NOT EXISTS idx_supplier_master_region ON supplier_master(region);
CREATE INDEX IF NOT EXISTS idx_supplier_master_primary_commodity ON supplier_master(primary_commodity);
CREATE INDEX IF NOT EXISTS idx_supplier_master_risk_score ON supplier_master(risk_score);