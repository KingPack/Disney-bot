# Disney-bot

A Python FastAPI automation scaffold for a bot-driven workflow.

## Project structure

app/
├── main.py
├── api/
│   └── routes.py
├── core/
│   └── config.py
├── bot/
│   ├── browser.py
│   ├── actions.py
│   ├── behavior.py
│   └── parser.py
├── tasks/
│   ├── worker.py
│   └── jobs.py
├── services/
│   ├── queue.py
│   └── scheduler.py
├── templates/
│   └── index.html
└── static/
    └── .gitkeep

## Getting started

1. Copy `.env.example` to `.env` and customize Redis/Celery settings.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   uvicorn app.main:app --reload
   ```

## Bot usage

Send a POST request to `/api/start` with JSON:

```json
{
  "email": "you@example.com",
  "password": "your_password",
  "query": "recruiter",
  "location": "San Francisco Bay Area",
  "limit": 20,
  "connect_limit": 5
}
```

The background Celery task will login, capture cookies, search recruiter profiles, and attempt connections.

## Notes

- `app/api/routes.py` contains the starter API endpoints.
- `app/tasks/worker.py` configures Celery broker/backend settings.
- `app/bot/` is prepared for browser automation and human-like behavior.
- `app/templates/index.html` provides a simple dashboard UI.
