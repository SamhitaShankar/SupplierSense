import os
import sys
import time
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from psycopg.rows import dict_row


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from agents.base import embed_text_bedrock  # noqa: E402


load_dotenv()


def get_db_connection():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("Missing DATABASE_URL in environment.")
    return psycopg.connect(database_url, row_factory=dict_row)


def fetch_suppliers():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM supplier_master ORDER BY supplier_id;")
            rows = cur.fetchall()
    return rows


def safe_get(row: dict, *keys, default=""):
    for key in keys:
        if key in row and row[key] is not None:
            return row[key]
    return default


def build_supplier_profile(row: dict) -> str:
    supplier_id = safe_get(row, "supplier_id", default="")
    name = safe_get(row, "supplier_name", "name", default="")
    country = safe_get(row, "country", default="")
    region = safe_get(row, "region", "state", default="")
    city = safe_get(row, "city", default="")
    primary_commodity = safe_get(row, "primary_commodity", "commodity", default="")
    commodities = safe_get(row, "commodities", default="")
    risk_score = safe_get(row, "risk_score", default="")
    past_disruptions = safe_get(
        row,
        "past_disruptions",
        "historical_disruptions",
        default="",
    )
    avg_recovery_days = safe_get(row, "avg_recovery_days", default="")
    reliability_score = safe_get(row, "reliability_score", default="")

    if isinstance(commodities, list):
        commodities_text = ", ".join(str(x) for x in commodities)
    else:
        commodities_text = str(commodities)

    profile = f"""
Supplier ID: {supplier_id}
Supplier Name: {name}
Country: {country}
Region: {region}
City: {city}
Primary Commodity: {primary_commodity}
Other Commodities: {commodities_text}
Risk Score: {risk_score}
Past Disruptions: {past_disruptions}
Average Recovery Days: {avg_recovery_days}
Reliability Score: {reliability_score}
""".strip()

    return profile


def build_metadata(row: dict) -> dict:
    supplier_id = safe_get(row, "supplier_id", default="")
    name = safe_get(row, "supplier_name", "name", default="")
    country = safe_get(row, "country", default="")
    region = safe_get(row, "region", "state", default="")
    city = safe_get(row, "city", default="")
    primary_commodity = safe_get(row, "primary_commodity", "commodity", default="")
    risk_score = safe_get(row, "risk_score", default=0)

    return {
        "supplier_id": str(supplier_id),
        "supplier_name": str(name),
        "country": str(country),
        "region": str(region),
        "city": str(city),
        "primary_commodity": str(primary_commodity),
        "risk_score": float(risk_score) if risk_score != "" else 0.0,
    }


def ensure_index():
    api_key = os.getenv("PINECONE_API_KEY")
    cloud = os.getenv("PINECONE_CLOUD", "aws")
    region = os.getenv("PINECONE_REGION", "us-east-1")
    index_name = os.getenv("PINECONE_INDEX_NAME", "supplier-knowledge")
    dimensions = int(os.getenv("BEDROCK_EMBED_DIMENSIONS", "1024"))

    if not api_key:
        raise ValueError("Missing PINECONE_API_KEY in environment.")

    pc = Pinecone(api_key=api_key)

    if not pc.has_index(index_name):
        print(f"Creating Pinecone index: {index_name}")
        pc.create_index(
            name=index_name,
            dimension=dimensions,
            metric="cosine",
            spec=ServerlessSpec(cloud=cloud, region=region),
        )

        while True:
            description = pc.describe_index(index_name)
            status = getattr(description, "status", None)

            is_ready = False
            if isinstance(status, dict):
                is_ready = status.get("ready", False)
            elif status is not None:
                is_ready = getattr(status, "ready", False)

            if is_ready:
                break

            print("Waiting for Pinecone index to become ready...")
            time.sleep(2)
    else:
        print(f"Pinecone index already exists: {index_name}")

    return pc.Index(index_name)


def upsert_suppliers():
    suppliers = fetch_suppliers()
    if not suppliers:
        print("No supplier records found in supplier_master.")
        return

    index = ensure_index()
    batch = []

    for row in suppliers:
        supplier_id = safe_get(row, "supplier_id", default="")
        if supplier_id == "":
            continue

        profile_text = build_supplier_profile(row)
        metadata = build_metadata(row)
        vector = embed_text_bedrock(profile_text)

        batch.append(
            {
                "id": f"supplier-{supplier_id}",
                "values": vector,
                "metadata": metadata,
            }
        )

    if not batch:
        print("No valid supplier rows to upsert.")
        return

    print(f"Upserting {len(batch)} supplier vectors...")
    index.upsert(vectors=batch, namespace="suppliers")

    stats = index.describe_index_stats()
    print("Upsert complete.")
    print("Index stats:")
    print(stats)


if __name__ == "__main__":
    upsert_suppliers()