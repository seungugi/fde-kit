"""Explicit local-demo identities; replace with an identity adapter before deployment."""
import secrets

from fastapi import APIRouter, HTTPException, Request
from starlette.responses import RedirectResponse

router = APIRouter()


def current_user(request):
    if not request.app.state.demo_mode:
        return {'id': None, 'name': '읽기 전용 방문자', 'role': 'member'}
    if request.session.get('demo_role') == 'admin':
        return {'id': 0, 'name': '데모 관리자', 'role': 'admin'}
    return {'id': 1, 'name': '이하늘', 'role': 'member'}


def csrf_token(request):
    if 'csrf' not in request.session:
        request.session['csrf'] = secrets.token_urlsafe(32)
    return request.session['csrf']


def require_csrf(request, form):
    expected = request.session.get('csrf')
    submitted = form.get('csrf')
    if (not isinstance(submitted, str) or not submitted.isascii()
            or not expected or not secrets.compare_digest(expected, submitted)):
        raise HTTPException(403, '요청 확인에 실패했습니다. 페이지를 새로 연 뒤 다시 시도해 주세요.')


def require_role(request, role):
    user = current_user(request)
    if not request.app.state.demo_mode or user['role'] != role:
        raise HTTPException(403, '이 작업을 수행할 권한이 없습니다. 데모 모드의 역할을 확인해 주세요.')
    return user


def common_context(request, **extra):
    return {
        'request': request, 'csrf': csrf_token(request),
        'demo_mode': request.app.state.demo_mode, 'user': current_user(request),
        'page': 'calendar', 'month': '2026-11',
        'message': request.session.pop('message', ''), 'error': '', **extra,
    }


@router.post('/demo/switch')
async def switch_demo(request: Request):
    form = await request.form()
    require_csrf(request, form)
    if not request.app.state.demo_mode:
        raise HTTPException(403, '데모 역할 전환이 비활성화되어 있습니다.')
    role = form.get('role')
    if role not in ('member', 'admin'):
        raise HTTPException(422, '회원 또는 관리자 역할을 선택해 주세요.')
    request.session['demo_role'] = role
    request.session['message'] = '데모 역할을 전환했습니다. 실제 로그인 기능은 아닙니다.'
    return RedirectResponse('/', status_code=303)
