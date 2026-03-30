from app.bot.actions import LinkedInBot
from app.tasks.worker import celery_app


@celery_app.task(name="app.tasks.jobs.start_session")
def start_session(job_data: dict) -> dict:
    email = job_data.get("email")
    password = job_data.get("password")
    cookies = job_data.get("cookies")
    query = job_data.get("query", "recruiter")
    location = job_data.get("location")
    limit = int(job_data.get("limit", 20))
    connect_limit = int(job_data.get("connect_limit", 5))

    if not cookies and (not email or not password):
        raise ValueError("LinkedIn email/password or cookie session is required.")

    bot = LinkedInBot(headless=False)
    try:
        if cookies:
            if not bot.load_cookies(cookies):
                raise RuntimeError("Failed to restore LinkedIn session from cookies.")
        else:
            bot.login(email, password)
            cookies = bot.get_cookies()

        search_results = bot.search_recruiters(query=query, location=location, limit=limit)
        connected = bot.connect_recruiters(limit=connect_limit)
        return {
            "status": "completed",
            "cookies": cookies,
            "search_results": search_results,
            "connected": connected,
        }
    finally:
        bot.close()
