import asyncio
import json
import uuid
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from core.run_store import get_run, save_run, utc_now_iso
from worker.tasks import run_agent_graph


ROOT_DIR = Path(__file__).resolve().parents[1]
MOCK_STATE_PATH = ROOT_DIR / "data" / "fixtures" / "mock_state.json"

app = FastAPI(title="SupplierSense API")


class RunCreateResponse(BaseModel):
    run_id: str
    status: str
    celery_task_id: str


class RunStateResponse(BaseModel):
    run_id: str
    status: str
    state: dict[str, Any]
    error: str | None = None
    created_at: str
    updated_at: str
    celery_task_id: str | None = None
    trigger_type: str | None = None
    context: dict[str, Any] | None = None


def load_mock_state() -> dict[str, Any]:
    with open(MOCK_STATE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@app.post("/run", response_model=RunCreateResponse)
async def create_run():
    run_id = str(uuid.uuid4())
    trigger_type = "manual"
    context = {}

    initial_payload = {
        "run_id": run_id,
        "status": "queued",
        "state": load_mock_state(),
        "error": None,
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
        "celery_task_id": None,
        "trigger_type": trigger_type,
        "context": context,
    }

    save_run(run_id, initial_payload)

    async_result = run_agent_graph.delay(trigger_type, context, run_id)

    initial_payload["celery_task_id"] = async_result.id
    initial_payload["updated_at"] = utc_now_iso()
    save_run(run_id, initial_payload)

    return RunCreateResponse(
        run_id=run_id,
        status="queued",
        celery_task_id=async_result.id,
    )


@app.get("/run/{run_id}", response_model=RunStateResponse)
async def get_run_state(run_id: str):
    run = get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    return RunStateResponse(**run)


@app.websocket("/ws/{run_id}")
async def websocket_run_updates(websocket: WebSocket, run_id: str):
    run = get_run(run_id)
    if not run:
        await websocket.accept()
        await websocket.send_json({"error": "Run not found"})
        await websocket.close()
        return

    await websocket.accept()

    last_updated_at = None

    try:
        while True:
            run = get_run(run_id)
            if not run:
                await websocket.send_json({"error": "Run deleted or expired"})
                await websocket.close()
                return

            current_updated_at = run.get("updated_at")

            if current_updated_at != last_updated_at:
                await websocket.send_json(run)
                last_updated_at = current_updated_at

            await asyncio.sleep(1)

    except WebSocketDisconnect:
        return