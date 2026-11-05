"""Synthetic monthly meal service. Interests are preferences, never bookings."""
import calendar
import csv
import io
import json
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import urlencode

from fastapi import APIRouter, HTTPException, Request
from starlette.responses import RedirectResponse, Response

from app.db import connect
from app.planner import build_plan, month_parts, serving_days, validate_plan
from app.security import common_context, current_user, require_csrf, require_role

router = APIRouter()
DEFAULT_MONTH = '2026-11'


def load_menus(connection, member_id=None):
    rows = connection.execute('''SELECT m.*, COUNT(i.member_id) AS interest_count,
        MAX(CASE WHEN i.member_id=? THEN 1 ELSE 0 END) AS interested
        FROM menus m LEFT JOIN interests i ON i.menu_id=m.id GROUP BY m.id ORDER BY m.id''', (member_id,))
    menus = []
    for row in rows:
        menu = dict(row)
        menu['components'] = json.loads(menu['components'])
        menu['requires_fryer'] = bool(menu['requires_fryer'])
        menu['interested'] = bool(menu['interested'])
        menus.append(menu)
    rank = {menu['id']: index + 1 for index, menu in enumerate(sorted(menus, key=lambda item: (-item['interest_count'], item['id'])))}
    for menu in menus:
        menu['rank'] = rank[menu['id']]
    return menus


def initialize(db_path):
    with connect(db_path, write=True) as connection:
        for statement in [
            '''CREATE TABLE IF NOT EXISTS members(id INTEGER PRIMARY KEY, name TEXT NOT NULL)''',
            '''CREATE TABLE IF NOT EXISTS menus(id INTEGER PRIMARY KEY, name TEXT NOT NULL,
               category TEXT NOT NULL, price INTEGER NOT NULL CHECK(price>0), description TEXT NOT NULL,
               components TEXT NOT NULL, requires_fryer INTEGER NOT NULL CHECK(requires_fryer IN (0,1)))''',
            '''CREATE TABLE IF NOT EXISTS interests(member_id INTEGER NOT NULL REFERENCES members(id),
               menu_id INTEGER NOT NULL REFERENCES menus(id), PRIMARY KEY(member_id,menu_id))''',
            '''CREATE TABLE IF NOT EXISTS plans(month TEXT PRIMARY KEY, version INTEGER NOT NULL,
               status TEXT NOT NULL CHECK(status IN ('draft','published')), published_version INTEGER,
               updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)''',
            '''CREATE TABLE IF NOT EXISTS plan_entries(month TEXT NOT NULL REFERENCES plans(month),
               stage TEXT NOT NULL CHECK(stage IN ('draft','published')), date TEXT NOT NULL,
               menu_id INTEGER NOT NULL REFERENCES menus(id), PRIMARY KEY(month,stage,date))''',
            '''CREATE TABLE IF NOT EXISTS metadata(key TEXT PRIMARY KEY, value TEXT NOT NULL)''',
        ]:
            connection.execute(statement)
        if connection.execute("SELECT 1 FROM metadata WHERE key='synthetic_seed_v1'").fetchone():
            return
        data_path = Path(__file__).resolve().parent.parent / 'data' / 'menus.json'
        menus = json.loads(data_path.read_text(encoding='utf-8'))
        connection.executemany('INSERT INTO members(id,name) VALUES (?,?)',
                               [(member, '이하늘' if member == 1 else f'가상 회원 {member:03}') for member in range(1, 121)])
        for menu in menus:
            connection.execute('INSERT INTO menus VALUES (?,?,?,?,?,?,?)', (
                menu['id'], menu['name'], menu['category'], menu['price'], menu['description'],
                json.dumps(menu['components'], ensure_ascii=False), int(menu['requires_fryer']),
            ))
            count = 102 - (menu['id'] - 1) * 3
            connection.executemany('INSERT INTO interests(member_id,menu_id) VALUES (?,?)',
                                   [(member, menu['id']) for member in range(2, count + 2)])
        planned = build_plan(DEFAULT_MONTH, load_menus(connection))
        connection.execute("INSERT INTO plans(month,version,status,published_version) VALUES (?,1,'published',1)", (DEFAULT_MONTH,))
        write_entries(connection, DEFAULT_MONTH, 'published', planned)
        connection.execute("INSERT INTO metadata VALUES ('synthetic_seed_v1','120 fictional members; deterministic preferences; November 2026')")


def month_value(value):
    try:
        month_parts(value)
    except (ValueError, TypeError) as exc:
        raise HTTPException(422, str(exc)) from exc
    return value


def write_entries(connection, month, stage, assignments):
    connection.execute('DELETE FROM plan_entries WHERE month=? AND stage=?', (month, stage))
    connection.executemany('INSERT INTO plan_entries(month,stage,date,menu_id) VALUES (?,?,?,?)',
                           [(month, stage, day, menu_id) for day, menu_id in assignments.items()])


def assignments_for(connection, month, stage):
    return {row['date']: row['menu_id'] for row in connection.execute(
        'SELECT date,menu_id FROM plan_entries WHERE month=? AND stage=? ORDER BY date', (month, stage))}


def visible_plan(connection, month, user):
    row = connection.execute('SELECT * FROM plans WHERE month=?', (month,)).fetchone()
    empty = {'month': month, 'version': 0, 'status': 'empty', 'published_version': None, 'has_published': False}
    if not row:
        return empty, {}
    plan = dict(row)
    plan['has_published'] = plan['published_version'] is not None
    if user['role'] == 'admin':
        return plan, assignments_for(connection, month, plan['status'])
    if not plan['has_published']:
        return empty, {}
    plan.update(status='published', version=plan['published_version'])
    return plan, assignments_for(connection, month, 'published')


def summarize(month, assignments, menus):
    by_id = {menu['id']: menu for menu in menus}
    selected = [by_id[menu_id] for menu_id in assignments.values() if menu_id in by_id]
    total_cost = sum(menu['price'] for menu in selected)
    score = sum(menu['interest_count'] for menu in selected)
    try:
        baseline = build_plan(month, menus, strategy='rotation')
    except ValueError:
        baseline = {}
    baseline_score = sum(by_id[menu_id]['interest_count'] for menu_id in baseline.values())
    baseline_cost = sum(by_id[menu_id]['price'] for menu_id in baseline.values())
    improvement = round((score - baseline_score) / baseline_score * 100, 1) if baseline_score and selected else 0
    stats = {
        'days': len(serving_days(month)), 'filled': len(selected), 'total_cost': total_cost,
        'average_cost': round(total_cost / len(selected)) if selected else 0,
        'interest_score': score, 'baseline_score': baseline_score, 'improvement_pct': improvement,
        'unique_menus': len(set(assignments.values())),
    }
    comparison = {
        'planned_score': score, 'baseline_score': baseline_score, 'improvement_pct': improvement,
        'planned_average_cost': stats['average_cost'],
        'baseline_average_cost': round(baseline_cost / len(baseline)) if baseline else 0,
    }
    return stats, comparison


def month_context(month):
    year, number = month_parts(month)
    first = date(year, number, 1)
    following = (first.replace(day=28) + timedelta(days=4)).replace(day=1)
    return {
        'month': month, 'year': year, 'month_number': number,
        'prev_month': (first - timedelta(days=1)).strftime('%Y-%m'),
        'next_month': following.strftime('%Y-%m'),
    }


def render(request, name, **context):
    return request.app.state.templates.TemplateResponse(
        request=request, name=name, context=common_context(request, **context))


def redirect_notice(request, message, target='/', **query):
    request.session['message'] = message
    return RedirectResponse(target + ('?' + urlencode(query) if query else ''), status_code=303)


@router.get('/')
def index(request: Request, month: str = DEFAULT_MONTH, date: str = ''):
    month = month_value(month)
    user = current_user(request)
    with connect(request.app.state.db_path) as connection:
        menus = load_menus(connection, user['id'])
        plan, assignments = visible_plan(connection, month, user)
    by_id = {menu['id']: menu for menu in menus}
    year, number = month_parts(month)
    weeks = [[{
        'date': day.isoformat(), 'day': day.day, 'in_month': day.month == number,
        'is_workday': day.month == number and day.weekday() < 5, 'is_friday': day.weekday() == 4,
        'menu': by_id.get(assignments.get(day.isoformat())),
    } for day in week] for week in calendar.Calendar(firstweekday=6).monthdatescalendar(year, number)]
    stats, comparison = summarize(month, assignments, menus)
    issues = validate_plan(month, assignments, menus) if assignments else []
    return render(request, 'index.html', page='calendar', **month_context(month), menus=menus,
                  weeks=weeks, plan=plan, stats=stats, comparison=comparison, issues=issues,
                  selected_date=date if date in assignments else '')


@router.get('/menus')
def menu_list(request: Request, q: str = '', category: str = '', sort: str = 'interest'):
    q = q[:100]
    with connect(request.app.state.db_path) as connection:
        all_menus = load_menus(connection, current_user(request)['id'])
    categories = sorted({menu['category'] for menu in all_menus})
    menus = [menu for menu in all_menus if (not q or q.casefold() in (menu['name'] + menu['description']).casefold())
             and (not category or menu['category'] == category)]
    if sort not in ('interest', 'price', 'name'):
        sort = 'interest'
    keys = {'interest': lambda menu: (-menu['interest_count'], menu['id']),
            'price': lambda menu: (menu['price'], menu['id']), 'name': lambda menu: (menu['name'], menu['id'])}
    menus.sort(key=keys[sort])
    return render(request, 'menus.html', page='menus', menus=menus, categories=categories, q=q,
                  category=category, sort=sort, total_menus=len(all_menus))


@router.get('/insights')
def insights(request: Request, month: str = DEFAULT_MONTH):
    month = month_value(month)
    with connect(request.app.state.db_path) as connection:
        menus = load_menus(connection, current_user(request)['id'])
        plan, assignments = visible_plan(connection, month, current_user(request))
        member_count = connection.execute('SELECT COUNT(*) FROM members').fetchone()[0]
    ranked = sorted(menus, key=lambda menu: (-menu['interest_count'], menu['id']))
    stats, comparison = summarize(month, assignments, menus)
    totals = {'members': member_count, 'menus': len(menus), 'interests': sum(menu['interest_count'] for menu in menus),
              'days': stats['days'], 'interest_score': stats['interest_score'],
              'baseline_score': stats['baseline_score'], 'improvement_pct': stats['improvement_pct']}
    return render(request, 'insights.html', page='insights', **month_context(month), menus=ranked,
                  ranked=ranked, totals=totals, stats=stats, comparison=comparison, plan=plan)


@router.get('/about')
def about(request: Request):
    return render(request, 'about.html', page='about')


@router.post('/interests/{menu_id}')
async def interest(request: Request, menu_id: int):
    form = await request.form()
    require_csrf(request, form)
    user = require_role(request, 'member')
    intent = form.get('intent')
    if intent not in ('add', 'remove'):
        raise HTTPException(422, '관심 등록 또는 취소를 선택해 주세요.')
    with connect(request.app.state.db_path, write=True) as connection:
        if not connection.execute('SELECT id FROM menus WHERE id=?', (menu_id,)).fetchone():
            raise HTTPException(404, '메뉴를 찾을 수 없습니다.')
        if intent == 'add':
            connection.execute('INSERT OR IGNORE INTO interests(member_id,menu_id) VALUES (?,?)', (user['id'], menu_id))
        else:
            connection.execute('DELETE FROM interests WHERE member_id=? AND menu_id=?', (user['id'], menu_id))
        menu = next(menu for menu in load_menus(connection, user['id']) if menu['id'] == menu_id)
    if request.headers.get('HX-Request', '').lower() == 'true':
        return render(request, 'partials/menu_card.html', menu=menu, page='menus')
    return redirect_notice(request, '관심 메뉴를 등록했습니다.' if intent == 'add' else '관심 메뉴를 취소했습니다.', '/menus')


async def plan_form(request):
    form = await request.form()
    require_csrf(request, form)
    require_role(request, 'admin')
    month = month_value(form.get('month', ''))
    try:
        version = int(form.get('version', ''))
        if version < 0:
            raise ValueError
    except (ValueError, TypeError) as exc:
        raise HTTPException(422, '올바른 식단 버전이 필요합니다.') from exc
    return form, month, version


def editable_state(connection, month, version, expected_status=None, allow_empty=False):
    row = connection.execute('SELECT * FROM plans WHERE month=?', (month,)).fetchone()
    if not row:
        if allow_empty and version == 0:
            return None
        raise HTTPException(409, '식단 상태가 바뀌었습니다. 페이지를 새로 열어 주세요.')
    if row['version'] != version:
        raise HTTPException(409, '다른 변경이 먼저 저장되었습니다. 새로고침 후 다시 시도해 주세요.')
    if expected_status and row['status'] != expected_status:
        raise HTTPException(409, '확정 식단은 편집을 다시 열어야 변경할 수 있습니다.' if expected_status == 'draft' else '이미 편집 중인 식단입니다.')
    return row


def increment_version(connection, month, status, *, published=False):
    connection.execute('UPDATE plans SET version=version+1,status=?,updated_at=CURRENT_TIMESTAMP WHERE month=?', (status, month))
    if published:
        connection.execute('UPDATE plans SET published_version=version WHERE month=?', (month,))


@router.post('/plans/reopen')
async def reopen(request: Request):
    _, month, version = await plan_form(request)
    with connect(request.app.state.db_path, write=True) as connection:
        editable_state(connection, month, version, 'published')
        write_entries(connection, month, 'draft', assignments_for(connection, month, 'published'))
        increment_version(connection, month, 'draft')
    return redirect_notice(request, '편집을 열었습니다. 회원에게는 이전 확정본이 계속 보입니다.', month=month)


@router.post('/plans/generate')
async def generate(request: Request):
    _, month, version = await plan_form(request)
    with connect(request.app.state.db_path, write=True) as connection:
        current = editable_state(connection, month, version, 'draft', allow_empty=True)
        try:
            planned = build_plan(month, load_menus(connection))
        except ValueError as exc:
            raise HTTPException(422, str(exc)) from exc
        if current is None:
            connection.execute("INSERT INTO plans(month,version,status) VALUES (?,1,'draft')", (month,))
        else:
            increment_version(connection, month, 'draft')
        write_entries(connection, month, 'draft', planned)
    return redirect_notice(request, '관심 수를 우선한 유효 초안을 생성했습니다. 전체 최적해를 보장하는 방식은 아닙니다.', month=month)


@router.post('/plans/publish')
async def publish(request: Request):
    _, month, version = await plan_form(request)
    with connect(request.app.state.db_path, write=True) as connection:
        editable_state(connection, month, version, 'draft')
        draft = assignments_for(connection, month, 'draft')
        issues = validate_plan(month, draft, load_menus(connection))
        if issues:
            raise HTTPException(422, ' '.join(issues))
        write_entries(connection, month, 'published', draft)
        connection.execute("DELETE FROM plan_entries WHERE month=? AND stage='draft'", (month,))
        increment_version(connection, month, 'published', published=True)
    return redirect_notice(request, '식단을 확정했습니다. 회원 화면에 반영되었습니다.', month=month)


@router.post('/plans/{day}/replace')
async def replace(request: Request, day: str):
    form, month, version = await plan_form(request)
    try:
        menu_id = int(form.get('menu_id', ''))
    except (ValueError, TypeError) as exc:
        raise HTTPException(422, '변경할 메뉴를 선택해 주세요.') from exc
    with connect(request.app.state.db_path, write=True) as connection:
        editable_state(connection, month, version, 'draft')
        draft = assignments_for(connection, month, 'draft')
        if day not in draft:
            raise HTTPException(422, '편집 중인 월의 식사 제공일을 선택해 주세요.')
        if not connection.execute('SELECT id FROM menus WHERE id=?', (menu_id,)).fetchone():
            raise HTTPException(404, '메뉴를 찾을 수 없습니다.')
        draft[day] = menu_id
        issues = validate_plan(month, draft, load_menus(connection))
        if issues:
            raise HTTPException(422, ' '.join(issues))
        write_entries(connection, month, 'draft', draft)
        increment_version(connection, month, 'draft')
    return redirect_notice(request, '식단을 변경했습니다. 확정 전까지 회원 화면은 바뀌지 않습니다.', month=month, date=day)


@router.get('/export.csv')
def export_csv(request: Request, month: str = DEFAULT_MONTH):
    month = month_value(month)
    with connect(request.app.state.db_path) as connection:
        plan, assignments = visible_plan(connection, month, current_user(request))
        menus = {menu['id']: menu for menu in load_menus(connection)}
    output = io.StringIO(newline='')
    writer = csv.writer(output)
    writer.writerow(['date', 'menu_id', 'menu_name', 'price', 'interest_count', 'requires_fryer', 'status', 'version'])
    for day, menu_id in sorted(assignments.items()):
        menu = menus[menu_id]
        name = "'" + menu['name'] if menu['name'].startswith(('=', '+', '-', '@', '\t', '\r')) else menu['name']
        writer.writerow([day, menu_id, name, menu['price'], menu['interest_count'], int(menu['requires_fryer']), plan['status'], plan['version']])
    return Response('\ufeff' + output.getvalue(), media_type='text/csv; charset=utf-8',
                    headers={'Content-Disposition': f'attachment; filename="ondam-{month}-{plan["status"]}.csv"'})
