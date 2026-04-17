from typing import TypedDict, List, Dict, Literal
from datetime import datetime


# =========================
# Agent 1: Signal Harvester
# =========================
class SignalEvent(TypedDict):
    id: str
    type: Literal['weather', 'financial', 'geo', 'shipping', 'regulatory', 'social']
    source: str
    raw_text: str
    severity: float
    affected_region: str
    affected_commodities: List[str]
    timestamp: datetime
    confidence: float


# =========================
# Agent 2: Supplier Analyzer
# =========================
class SupplierProfile(TypedDict):
    id: str
    name: str
    tier: int
    location: str
    commodities: List[str]
    risk_score: float
    risk_factors: List[str]
    historical_disruptions: int
    avg_recovery_days: float
    contract_value_inr: float
    lead_time_days: int


# =========================
# Agent 3: Impact Modeler
# =========================
class SKUImpact(TypedDict):
    sku_id: str
    sku_name: str
    supplier_id: str
    current_stock_units: int
    avg_daily_demand: float
    days_until_stockout: int
    revenue_at_risk_inr: float
    margin_at_risk_inr: float
    severity: Literal['low', 'medium', 'high', 'critical']
    alternate_supplier_available: bool


# =========================
# Agent 4: Inventory Optimizer
# =========================
class ReorderRec(TypedDict):
    sku_id: str
    current_stock: int
    recommended_reorder_qty: int
    preferred_supplier_id: str
    alternate_supplier_id: str
    estimated_cost_inr: float
    lead_time_days: int
    urgency: Literal['immediate', 'within_3d', 'within_week']
    po_draft_text: str


# =========================
# Agent 5: Response Planner
# =========================
class ResponsePlaybook(TypedDict):
    run_id: str
    severity: str
    executive_summary: str
    actions: List[Dict]
    supplier_comms: List[Dict]
    internal_alerts: List[Dict]
    escalate_to: List[str]


# =========================
# Agent 6: Orchestrator
# =========================
class OrchestratorLog(TypedDict):
    run_id: str
    triggered_by: str
    started_at: datetime
    ended_at: datetime
    agents_executed: List[str]
    final_severity: str
    total_revenue_at_risk_inr: float
    actions_generated: int
    alerts_sent: List[str]
    error_count: int


# =========================
# MASTER STATE (GLOBAL CONTRACT)
# =========================
class SupplierSenseState(TypedDict):
    # A1
    raw_signals: List[SignalEvent]
    signal_summary: str

    # A2
    supplier_risk_scores: Dict[str, float]
    supplier_profiles: Dict[str, SupplierProfile]
    disruption_detected: bool
    affected_suppliers: List[str]

    # A3
    impacted_skus: List[SKUImpact]
    total_revenue_at_risk: float
    impact_severity: Literal['low', 'medium', 'high', 'critical']

    # A4
    reorder_recommendations: List[ReorderRec]
    safety_stock_adjustments: Dict[str, int]

    # A5
    playbook: ResponsePlaybook
    escalation_required: bool

    # A6
    run_id: str
    triggered_at: datetime
    status: Literal['running', 'completed', 'escalated', 'failed']
    error_log: List[str]