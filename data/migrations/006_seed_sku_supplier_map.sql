INSERT INTO sku_supplier_map (
    sku_id, sku_name, supplier_id, commodity, sourcing_share_pct,
    is_primary_supplier, unit_cost_inr, lead_time_days, min_order_qty
) VALUES
('SKU001', 'Industrial PCB Board', 'SUP003', 'pcb', 80.00, TRUE, 420.00, 21, 100),
('SKU001', 'Industrial PCB Board', 'SUP001', 'electronics', 20.00, FALSE, 450.00, 12, 80),
('SKU002', 'Food Grade Packaging Roll', 'SUP002', 'packaging', 60.00, TRUE, 110.00, 10, 200),
('SKU002', 'Food Grade Packaging Roll', 'SUP008', 'packaging', 40.00, FALSE, 105.00, 13, 200),
('SKU003', 'Cotton Fabric Bundle', 'SUP006', 'textiles', 100.00, TRUE, 780.00, 24, 50),
('SKU004', 'Aluminium Housing Unit', 'SUP007', 'aluminium', 100.00, TRUE, 1250.00, 14, 40),
('SKU005', 'Retail Fastener Kit', 'SUP010', 'fasteners', 100.00, TRUE, 95.00, 9, 500),
('SKU006', 'Refined Palm Oil Drum', 'SUP009', 'food oils', 100.00, TRUE, 3200.00, 19, 20)
ON CONFLICT DO NOTHING;