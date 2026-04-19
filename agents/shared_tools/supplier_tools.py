from __future__ import annotations

import os
from typing import Any, Optional

import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv


load_dotenv()


def get_db_connection():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL is not set in environment.")

    return psycopg.connect(database_url, row_factory=dict_row)


def lookup_supplier_by_region(region: str, commodity: Optional[str] = None) -> list[dict[str, Any]]:
    """
    Fetch suppliers from supplier_master by region.
    Optionally filter by commodity.
    """
    query = """
        SELECT *
        FROM supplier_master
        WHERE LOWER(region) = LOWER(%s)
    """
    params = [region]

    if commodity:
        query += " AND LOWER(primary_commodity) = LOWER(%s)"
        params.append(commodity)

    query += " ORDER BY risk_score ASC, supplier_name ASC"

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            results = cur.fetchall()

    return results


def query_supplier_history(supplier_id: str, limit: int = 5) -> list[dict[str, Any]]:
    """
    Fetch recent disruption history for a supplier.
    """
    query = """
        SELECT *
        FROM disruption_events
        WHERE supplier_id = %s
        ORDER BY created_at DESC
        LIMIT %s
    """

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (supplier_id, limit))
            results = cur.fetchall()

    return results


def get_dnb_stub(supplier_id: str) -> dict[str, Any]:
    """
    Stubbed D&B-style supplier metadata.
    Replace later with a real external enrichment source.
    """
    stub_map = {
        "SUP001": {
            "credit_score_band": "Low Risk",
            "business_stability": "Established",
            "years_in_operation": 12,
        },
        "SUP002": {
            "credit_score_band": "Medium Risk",
            "business_stability": "Stable",
            "years_in_operation": 8,
        },
        "SUP003": {
            "credit_score_band": "Medium Risk",
            "business_stability": "Growing",
            "years_in_operation": 6,
        },
        "SUP004": {
            "credit_score_band": "Low Risk",
            "business_stability": "Established",
            "years_in_operation": 15,
        },
    }

    return stub_map.get(
        supplier_id,
        {
            "credit_score_band": "Unknown",
            "business_stability": "Unknown",
            "years_in_operation": None,
        },
    )


def enrich_supplier_profile(supplier_id: str, history_limit: int = 5) -> dict[str, Any]:
    """
    Join supplier master + disruption history + D&B stub data
    into one enriched profile.
    """
    supplier_query = """
        SELECT *
        FROM supplier_master
        WHERE supplier_id = %s
        LIMIT 1
    """

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(supplier_query, (supplier_id,))
            supplier = cur.fetchone()

    if not supplier:
        raise ValueError(f"Supplier {supplier_id} not found in supplier_master")

    history = query_supplier_history(supplier_id, limit=history_limit)
    dnb_stub = get_dnb_stub(supplier_id)

    enriched_profile = {
        "supplier": supplier,
        "recent_disruptions": history,
        "dnb_stub": dnb_stub,
    }

    return enriched_profile