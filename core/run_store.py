import json
import os
from datetime import datetime, timezone
from typing import Any

import redis
from dotenv import load_dotenv


load_dotenv()


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _redis_client() -> redis.Redis:
    redis_url = os.getenv("RUN_STATE_REDIS_URL", "redis://localhost:6379/2")
    return redis.Redis.from_url(redis_url, decode_responses=True)


def _run_key(run_id: str) -> str:
    return f"run:{run_id}"


def save_run(run_id: str, payload: dict[str, Any]) -> None:
    client = _redis_client()
    client.set(_run_key(run_id), json.dumps(payload))


def get_run(run_id: str) -> dict[str, Any] | None:
    client = _redis_client()
    raw = client.get(_run_key(run_id))
    if not raw:
        return None
    return json.loads(raw)


def update_run(run_id: str, **updates) -> dict[str, Any]:
    existing = get_run(run_id)
    if not existing:
        raise KeyError(f"Run {run_id} not found in Redis.")

    existing.update(updates)
    existing["updated_at"] = utc_now_iso()
    save_run(run_id, existing)
    return existing


def append_dashboard_update(run_id: str, dashboard_update: dict[str, Any]) -> dict[str, Any]:
    existing = get_run(run_id)
    if not existing:
        raise KeyError(f"Run {run_id} not found in Redis.")

    state = existing.setdefault("state", {})
    dashboard_updates = state.setdefault("dashboard_updates", [])
    dashboard_updates.append(dashboard_update)

    existing["updated_at"] = utc_now_iso()
    save_run(run_id, existing)
    return existing