import copy

from graph.pipeline import graph
from core.run_store import get_run, update_run
from worker.celery_app import celery_app


@celery_app.task(name="worker.tasks.run_agent_graph")
def run_agent_graph(trigger_type: str, context: dict, run_id: str):
    """
    Background task that runs the SupplierSense graph.
    """
    run = get_run(run_id)
    if not run:
        raise ValueError(f"Run {run_id} not found.")

    try:
        update_run(
            run_id,
            status="running",
            trigger_type=trigger_type,
            context=context or {},
            error=None,
        )

        input_state = copy.deepcopy(run["state"])
        result_state = graph.invoke(input_state)

        update_run(
            run_id,
            status="completed",
            state=result_state,
            error=None,
        )

        return {
            "run_id": run_id,
            "status": "completed",
        }

    except Exception as e:
        update_run(
            run_id,
            status="failed",
            error=str(e),
        )
        raise