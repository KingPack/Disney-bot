You are a senior Python engineer and system architect.

Build a production-ready project with the following requirements:

# 🎯 Goal

Create a LinkedIn automation system that simulates human behavior to:

* search for people (recruiters and developers)
* apply filters (location, company, keywords)
* visit profiles
* optionally send connection requests

# ⚠️ Constraints

* Avoid naive automation patterns
* Implement human-like interaction behavior
* Use asynchronous and queue-based execution (NO blocking sleep)

# 🧱 Tech Stack

* Backend: FastAPI
* Automation: Selenium (prefer undetected-chromedriver if possible)
* Queue system: Celery + Redis
* Frontend: Jinja2 templates + Bulma CSS
* Realtime updates: WebSockets (FastAPI)
* Containerization: Docker (optional but preferred)

# 📁 Project Structure

Create a clean scalable structure:

app/
├── main.py                # FastAPI entrypoint
├── api/                  # routes
├── core/                 # config
├── bot/
│    ├── browser.py       # driver setup
│    ├── actions.py       # linkedin actions
│    ├── behavior.py      # human simulation
│    ├── parser.py        # profile analysis
├── tasks/
│    ├── worker.py        # celery worker
│    ├── jobs.py          # task definitions
├── services/
│    ├── queue.py
│    ├── scheduler.py
├── templates/
│    └── index.html
├── static/

# ⚙️ Features to Implement

## 1. Selenium Bot

* login to LinkedIn
* perform people search using keywords
* apply filters (location, company if possible)
* open profiles
* detect "Connect" button and click

## 2. Human Behavior Engine

Create a class that simulates real user actions:

* random delays (use distributions, not fixed)
* scrolling behavior (random depth and intervals)
* mouse movement simulation
* random decision making (sometimes skip profiles)
* reading time simulation

## 3. Queue System (Celery)

* break actions into small tasks:

  * search
  * open profile
  * scroll
  * connect
* chain tasks with countdown delays
* ensure tasks are non-blocking

## 4. Scheduler

* distribute actions over time
* simulate working hours (9am–6pm)
* limit number of connections per day (configurable)

## 5. Smart Filtering

* parse profile text
* detect recruiters using keywords:
  ["recruiter", "talent", "hiring", "hr"]
* allow filtering by company name

## 6. FastAPI Backend

* endpoint to start a bot session
* endpoint to check status
* websocket for real-time logs

## 7. Web Interface

* simple dashboard using Jinja2 + Bulma
* form inputs:

  * email
  * password
  * keyword
  * location
  * limit
* live log panel (WebSocket)

## 8. Logging System

* log every action:

  * visited profiles
  * connections sent
  * errors
* store logs in file or lightweight DB (SQLite)

## 9. Anti-Detection Measures

* randomize all actions
* avoid repetitive patterns
* configurable rate limits

## 10. Docker Setup (optional)

* Dockerfile
* docker-compose with:

  * FastAPI
  * Redis
  * Celery worker

# 🧪 Extra (if possible)

* add retry logic for failed actions
* add headless toggle
* add proxy support (basic)

# 📌 Output Requirements

* Generate full working code
* Include comments explaining key parts
* Provide instructions to run:

  * install dependencies
  * start Redis
  * run Celery worker
  * run FastAPI app

# 🚀 Priority

Focus on clean architecture, modular design, and extensibility.
Avoid monolithic scripts.
