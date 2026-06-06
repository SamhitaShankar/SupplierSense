import json
from datetime import datetime
from decimal import Decimal
from typing import Any

import redis

client = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)


def _run_key(run_id: str) -> str:
    return f"run:{run_id}"


def utc_now_iso() -> str:
    return datetime.utcnow().isoformat()


# 🔥 CRITICAL FIX: make everything JSON serializable
def _serialize(obj: Any):
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {k: _serialize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_serialize(v) for v in obj]
    return obj


def save_run(run_id: str, payload: dict):
    safe_payload = _serialize(payload)
    client.set(_run_key(run_id), json.dumps(safe_payload))


def get_run(run_id: str):
    data = client.get(_run_key(run_id))
    if not data:
        return None
    return json.loads(data)


def update_run(run_id: str, **updates):
    existing = get_run(run_id)
    if not existing:
        return

    existing.update(updates)
    existing["updated_at"] = utc_now_iso()

    save_run(run_id, existing)