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


def normalize_region(region: str) -> str:
    """
    Convert signals like 'Chennai, India' → '%chennai%'
    """
    if not region:
        return "%"
    base = region.split(",")[0].strip().lower()
    return f"%{base}%"


def lookup_supplier_by_region(region: str, commodity: Optional[str] = None) -> list[dict[str, Any]]:
    """
    Fetch suppliers using flexible matching:
    - region
    - city
    - country
    """

    region_pattern = normalize_region(region)

    query = """
        SELECT *
        FROM supplier_master
        WHERE (
            LOWER(region) LIKE %s
            OR LOWER(city) LIKE %s
            OR LOWER(country) LIKE %s
        )
    """

    params = [region_pattern, region_pattern, region_pattern]

    if commodity:
        query += """
            AND (
                LOWER(primary_commodity) = LOWER(%s)
                OR EXISTS (
                    SELECT 1 FROM unnest(commodities) AS c
                    WHERE LOWER(c) = LOWER(%s)
                )
            )
        """
        params.extend([commodity, commodity])

    query += " ORDER BY risk_score ASC, supplier_name ASC"

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            results = cur.fetchall()

    return results


def query_supplier_history(supplier_id: str, limit: int = 5) -> list[dict[str, Any]]:
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
            return cur.fetchall()


def get_dnb_stub(supplier_id: str) -> dict[str, Any]:
    return {
        "credit_score_band": "Low Risk",
        "business_stability": "Stable",
        "years_in_operation": 10,
    }


def enrich_supplier_profile(supplier_id: str, history_limit: int = 5) -> dict[str, Any]:
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
        return {}

    history = query_supplier_history(supplier_id, history_limit)

    return {
        "supplier": supplier,
        "recent_disruptions": history,
        "dnb_stub": get_dnb_stub(supplier_id),
    }