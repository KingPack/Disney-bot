from app.tasks.jobs import start_session


def enqueue_start_session(payload: dict) -> str:
    task = start_session.delay(payload)
    return task.id
