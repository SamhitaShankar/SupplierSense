INSERT INTO supplier_master (
    supplier_id, supplier_name, tier, country, region, city, commodities, primary_commodity,
    lead_time_days, contract_value_inr, risk_score, historical_disruptions, avg_recovery_days,
    contact_name, contact_email, contact_phone, is_active
) VALUES
('SUP001', 'Chennai Components Pvt Ltd', 1, 'India', 'Tamil Nadu', 'Chennai', ARRAY['electronics','semiconductors'], 'electronics', 12, 8500000.00, 0.220, 2, 4.5, 'Arun Prakash', 'arun@chennaicomponents.test', '+91-9000000001', TRUE),
('SUP002', 'Gujarat Polymers Ltd', 2, 'India', 'Gujarat', 'Ahmedabad', ARRAY['plastics','packaging'], 'packaging', 10, 6200000.00, 0.180, 1, 3.0, 'Meera Shah', 'meera@gujaratpolymers.test', '+91-9000000002', TRUE),
('SUP003', 'Shenzhen Micro Devices', 1, 'China', 'Guangdong', 'Shenzhen', ARRAY['electronics','pcb'], 'pcb', 21, 15400000.00, 0.410, 4, 8.0, 'Liu Wen', 'liu@szmicro.test', '+86-1000000003', TRUE),
('SUP004', 'Bangkok Agro Inputs', 2, 'Thailand', 'Bangkok', 'Bangkok', ARRAY['agri-inputs','chemicals'], 'agri-inputs', 16, 4700000.00, 0.260, 2, 5.0, 'Narin Chai', 'narin@bangkokagro.test', '+66-1000000004', TRUE),
('SUP005', 'Hamburg Cold Chain GmbH', 1, 'Germany', 'Hamburg', 'Hamburg', ARRAY['cold-chain','food logistics'], 'cold-chain', 18, 9800000.00, 0.120, 1, 2.5, 'Anna Keller', 'anna@hamburgcold.test', '+49-1000000005', TRUE),
('SUP006', 'Sao Paulo Textiles SA', 2, 'Brazil', 'Sao Paulo', 'Sao Paulo', ARRAY['textiles','cotton'], 'textiles', 24, 7100000.00, 0.330, 3, 6.5, 'Rafael Costa', 'rafael@sptextiles.test', '+55-1000000006', TRUE),
('SUP007', 'Dubai Metals Trading', 1, 'UAE', 'Dubai', 'Dubai', ARRAY['metals','aluminium'], 'aluminium', 14, 11200000.00, 0.250, 2, 4.0, 'Layla Rahman', 'layla@dubaimetals.test', '+971-1000000007', TRUE),
('SUP008', 'Ho Chi Minh Packaging Co', 2, 'Vietnam', 'Ho Chi Minh City', 'Ho Chi Minh City', ARRAY['packaging','paper'], 'packaging', 13, 5300000.00, 0.200, 1, 3.5, 'Tran Minh', 'tran@hcmpackaging.test', '+84-1000000008', TRUE),
('SUP009', 'Jakarta Palm Ingredients', 3, 'Indonesia', 'Jakarta', 'Jakarta', ARRAY['food oils','fmcg ingredients'], 'food oils', 19, 4450000.00, 0.370, 5, 7.5, 'Dewi Santoso', 'dewi@jakartaingredients.test', '+62-1000000009', TRUE),
('SUP010', 'Pune Precision Fasteners', 1, 'India', 'Maharashtra', 'Pune', ARRAY['fasteners','industrial hardware'], 'fasteners', 9, 6700000.00, 0.160, 1, 2.0, 'Rohit Kulkarni', 'rohit@punefasteners.test', '+91-9000000010', TRUE)
ON CONFLICT (supplier_id) DO NOTHING;