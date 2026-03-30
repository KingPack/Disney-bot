from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.api.routes import router

jinja_templates = Jinja2Templates(directory="app/templates")


def create_app() -> FastAPI:
    app = FastAPI(title="Disney Bot")
    app.include_router(router)
    return app


app = create_app()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return jinja_templates.TemplateResponse(
        request,
        "index.html",
        {"request": request}
    )
