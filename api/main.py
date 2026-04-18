import asyncio
import copy
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import BackgroundTasks, FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from graph.pipeline import graph


ROOT_DIR = Path(__file__).resolve().parents[1]
MOCK_STATE_PATH = ROOT_DIR / "data" / "fixtures" / "mock_state.json"

app = FastAPI(title="SupplierSense API")


# In-memory run store for the current development phase
RUN_STORE: dict[str, dict[str, Any]] = {}


class RunCreateResponse(BaseModel):
    run_id: str
    status: str


class RunStateResponse(BaseModel):
    run_id: str
    status: str
    state: dict[str, Any]
    error: str | None = None
    created_at: str
    updated_at: str


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, run_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.setdefault(run_id, []).append(websocket)

    def disconnect(self, run_id: str, websocket: WebSocket):
        if run_id in self.active_connections:
            if websocket in self.active_connections[run_id]:
                self.active_connections[run_id].remove(websocket)

            if not self.active_connections[run_id]:
                del self.active_connections[run_id]

    async def broadcast(self, run_id: str, message: dict[str, Any]):
        if run_id not in self.active_connections:
            return

        dead_connections = []

        for websocket in self.active_connections[run_id]:
            try:
                await websocket.send_json(message)
            except Exception:
                dead_connections.append(websocket)

        for websocket in dead_connections:
            self.disconnect(run_id, websocket)


manager = ConnectionManager()


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_mock_state() -> dict[str, Any]:
    with open(MOCK_STATE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def build_run_payload(run_id: str) -> dict[str, Any]:
    run = RUN_STORE[run_id]
    return {
        "run_id": run_id,
        "status": run["status"],
        "state": run["state"],
        "error": run.get("error"),
        "created_at": run["created_at"],
        "updated_at": run["updated_at"],
    }


async def broadcast_run_update(run_id: str):
    if run_id not in RUN_STORE:
        return
    await manager.broadcast(run_id, build_run_payload(run_id))


async def push_dashboard_update(run_id: str, dashboard_update: dict[str, Any]):
    """
    Hook for the orchestrator to call later.
    For now, it stores dashboard updates in the run state and broadcasts them.
    """
    if run_id not in RUN_STORE:
        return

    run = RUN_STORE[run_id]
    state = run["state"]

    if "dashboard_updates" not in state or not isinstance(state["dashboard_updates"], list):
        state["dashboard_updates"] = []

    state["dashboard_updates"].append(dashboard_update)
    run["updated_at"] = utc_now_iso()

    await broadcast_run_update(run_id)


async def execute_graph_run(run_id: str):
    if run_id not in RUN_STORE:
        return

    try:
        RUN_STORE[run_id]["status"] = "running"
        RUN_STORE[run_id]["updated_at"] = utc_now_iso()
        await broadcast_run_update(run_id)

        input_state = copy.deepcopy(RUN_STORE[run_id]["state"])

        # graph.invoke is synchronous, so run it in a worker thread
        result_state = await asyncio.to_thread(graph.invoke, input_state)

        RUN_STORE[run_id]["state"] = result_state
        RUN_STORE[run_id]["status"] = "completed"
        RUN_STORE[run_id]["updated_at"] = utc_now_iso()

        await broadcast_run_update(run_id)

    except Exception as e:
        RUN_STORE[run_id]["status"] = "failed"
        RUN_STORE[run_id]["error"] = str(e)
        RUN_STORE[run_id]["updated_at"] = utc_now_iso()
        await broadcast_run_update(run_id)


@app.post("/run", response_model=RunCreateResponse)
async def create_run(background_tasks: BackgroundTasks):
    run_id = str(uuid.uuid4())

    RUN_STORE[run_id] = {
        "status": "queued",
        "state": load_mock_state(),
        "error": None,
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
    }

    background_tasks.add_task(execute_graph_run, run_id)

    return RunCreateResponse(run_id=run_id, status="queued")


@app.get("/run/{run_id}", response_model=RunStateResponse)
async def get_run(run_id: str):
    if run_id not in RUN_STORE:
        raise HTTPException(status_code=404, detail="Run not found")

    payload = build_run_payload(run_id)
    return RunStateResponse(**payload)


@app.websocket("/ws/{run_id}")
async def websocket_run_updates(websocket: WebSocket, run_id: str):
    if run_id not in RUN_STORE:
        await websocket.accept()
        await websocket.send_json({"error": "Run not found"})
        await websocket.close()
        return

    await manager.connect(run_id, websocket)

    try:
        # Send current snapshot immediately on connect
        await websocket.send_json(build_run_payload(run_id))

        # Keep the socket alive and allow client pings/messages
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(run_id, websocket)