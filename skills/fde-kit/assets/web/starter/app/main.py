import os
import secrets
from pathlib import Path

from fastapi import FastAPI, Request
from starlette.exceptions import HTTPException
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from app import features
from app.security import common_context, router as security_router

ROOT = Path(__file__).resolve().parent.parent
LOCAL_SECRET = secrets.token_urlsafe(48)


def create_app(db_path=None, demo_mode=None):
    application = FastAPI(title='FDE Web Starter', docs_url=None, redoc_url=None)
    application.state.db_path = Path(db_path or os.environ.get('APP_DB', ROOT / 'data' / 'app.sqlite3'))
    application.state.db_path.parent.mkdir(parents=True, exist_ok=True)
    application.state.demo_mode = (os.environ.get('DEMO_MODE', '0') == '1') if demo_mode is None else bool(demo_mode)
    application.state.templates = Jinja2Templates(directory=str(ROOT / 'templates'))
    application.add_middleware(
        SessionMiddleware, secret_key=os.environ.get('APP_SECRET') or LOCAL_SECRET,
        same_site='lax', https_only=os.environ.get('COOKIE_SECURE', '0') == '1',
        max_age=8 * 60 * 60,
    )
    application.mount('/static', StaticFiles(directory=str(ROOT / 'static'), check_dir=False), name='static')
    features.initialize(application.state.db_path)
    application.include_router(security_router)
    application.include_router(features.router)

    @application.get('/health')
    def health():
        return {'status': 'ok', 'demo_mode': application.state.demo_mode}

    @application.exception_handler(HTTPException)
    async def http_error(request: Request, exc: HTTPException):
        context = common_context(request, error=str(exc.detail), status_code=exc.status_code, page='error')
        partial = request.headers.get('HX-Request', '').lower() == 'true'
        headers = dict(exc.headers or {})
        if partial:
            headers.update({'HX-Retarget': '#notice', 'HX-Reswap': 'outerHTML'})
        return application.state.templates.TemplateResponse(
            request=request, name='partials/notice.html' if partial else 'error.html',
            context=context, status_code=exc.status_code, headers=headers,
        )

    return application


app = create_app()
