from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.services.queue import enqueue_start_session

router = APIRouter(prefix="/api", tags=["bot"])


@router.post("/start")
async def start_bot(payload: dict):
    if not payload.get("cookies") and (
        not payload.get("email") or not payload.get("password")
    ):
        return JSONResponse(
            {
                "status": "error",
                "detail": "Provide email/password or a LinkedIn cookie session.",
            },
            status_code=400,
        )

    task_id = enqueue_start_session(payload)
    return JSONResponse({"status": "queued", "task_id": task_id})


@router.get("/status")
async def status():
    return {"status": "idle", "active_jobs": 0}
