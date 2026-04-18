CREATE TABLE IF NOT EXISTS sku_supplier_map (
    id BIGSERIAL PRIMARY KEY,
    sku_id VARCHAR(30) NOT NULL,
    sku_name VARCHAR(150) NOT NULL,
    supplier_id VARCHAR(20) NOT NULL REFERENCES supplier_master(supplier_id) ON DELETE CASCADE,
    commodity VARCHAR(80) NOT NULL,
    sourcing_share_pct NUMERIC(5,2) NOT NULL CHECK (sourcing_share_pct >= 0 AND sourcing_share_pct <= 100),
    is_primary_supplier BOOLEAN NOT NULL DEFAULT FALSE,
    unit_cost_inr NUMERIC(12,2) NOT NULL CHECK (unit_cost_inr >= 0),
    lead_time_days INT NOT NULL CHECK (lead_time_days >= 0),
    min_order_qty INT NOT NULL DEFAULT 0 CHECK (min_order_qty >= 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_sku_supplier_map_sku_id ON sku_supplier_map(sku_id);
CREATE INDEX IF NOT EXISTS idx_sku_supplier_map_supplier_id ON sku_supplier_map(supplier_id);
CREATE INDEX IF NOT EXISTS idx_sku_supplier_map_commodity ON sku_supplier_map(commodity);