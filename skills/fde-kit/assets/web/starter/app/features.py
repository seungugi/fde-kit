from fastapi import APIRouter, HTTPException, Request
from starlette.responses import RedirectResponse

from app.db import connect
from app.security import common_context, require_csrf, require_role

router = APIRouter()


def initialize(db_path):
    with connect(db_path, write=True) as connection:
        connection.execute('''CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY, title TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )''')


@router.get('/')
def index(request: Request):
    with connect(request.app.state.db_path) as connection:
        items = [dict(row) for row in connection.execute('SELECT * FROM items ORDER BY id DESC')]
    return request.app.state.templates.TemplateResponse(
        request=request, name='index.html', context=common_context(request, items=items, page='home'),
    )


@router.post('/items')
async def add_item(request: Request):
    form = await request.form()
    require_csrf(request, form)
    require_role(request, 'admin')
    title = str(form.get('title', '')).strip()
    if not title or len(title) > 200:
        raise HTTPException(422, '제목은 1~200자로 입력해 주세요.')
    with connect(request.app.state.db_path, write=True) as connection:
        connection.execute('INSERT INTO items(title) VALUES (?)', (title,))
    request.session['message'] = '항목을 추가했습니다.'
    return RedirectResponse('/', status_code=303)


@router.post('/items/{item_id}/delete')
async def delete_item(request: Request, item_id: int):
    form = await request.form()
    require_csrf(request, form)
    require_role(request, 'admin')
    with connect(request.app.state.db_path, write=True) as connection:
        connection.execute('DELETE FROM items WHERE id=?', (item_id,))
    request.session['message'] = '항목을 삭제했습니다.'
    return RedirectResponse('/', status_code=303)
