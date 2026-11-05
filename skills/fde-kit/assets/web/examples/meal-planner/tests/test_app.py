import csv
import io
import re
import sqlite3
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from types import SimpleNamespace

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient


def csrf(client):
    page = client.get('/menus')
    assert page.status_code == 200
    return re.search(r'name="csrf"\s+value="([^"]+)"', page.text).group(1)


def test_non_ascii_csrf_is_rejected_with_403():
    from app.security import require_csrf

    request = SimpleNamespace(session={'csrf': 'valid-ascii-session-token'})
    with pytest.raises(HTTPException) as rejected:
        require_csrf(request, {'csrf': '한글'})
    assert rejected.value.status_code == 403


def test_read_transaction_keeps_snapshot_across_concurrent_commit(tmp_path):
    from app.db import connect

    path = tmp_path / 'snapshot.sqlite3'
    with sqlite3.connect(path) as setup:
        setup.execute('PRAGMA journal_mode=WAL')
        setup.execute('CREATE TABLE state(version INTEGER NOT NULL)')
        setup.execute('INSERT INTO state VALUES (1)')
    with connect(path) as reader:
        assert reader.execute('SELECT version FROM state').fetchone()[0] == 1
        with connect(path, write=True) as writer:
            writer.execute('UPDATE state SET version=2')
        assert reader.execute('SELECT version FROM state').fetchone()[0] == 1
    with connect(path) as refreshed:
        assert refreshed.execute('SELECT version FROM state').fetchone()[0] == 2


@pytest.fixture
def setup(tmp_path):
    from app.main import create_app

    path = tmp_path / 'meal.sqlite3'
    with TestClient(create_app(path, True)) as client:
        yield client, path, csrf(client)


def rows(path, sql, args=()):
    with sqlite3.connect(path) as connection:
        connection.row_factory = sqlite3.Row
        return [dict(row) for row in connection.execute(sql, args)]


def state(path):
    return rows(path, 'SELECT * FROM plans WHERE month=?', ('2026-11',))[0]


def admin(client, token):
    assert client.post('/demo/switch', data={'csrf': token, 'role': 'admin'}).status_code == 200


def plan_post(client, path, token, action, **extra):
    return client.post('/plans/' + action, data={'csrf': token, 'month': '2026-11', 'version': state(path)['version'], **extra})


def entries(path, stage='published'):
    return rows(path, 'SELECT e.date,m.* FROM plan_entries e JOIN menus m ON e.menu_id=m.id WHERE e.month=? AND e.stage=? ORDER BY e.date', ('2026-11', stage))


def check_hard_constraints(selected):
    assert len(selected) == 21
    assert selected[0]['date'] == '2026-11-02'
    assert selected[-1]['date'] == '2026-11-30'
    counts = Counter(row['id'] for row in selected)
    assert max(counts.values()) <= 2
    previous = {}
    for index, row in enumerate(selected):
        assert date.fromisoformat(row['date']).weekday() < 5
        assert row['price'] <= 8000
        assert not (date.fromisoformat(row['date']).weekday() == 4 and row['requires_fryer'])
        if row['id'] in previous:
            assert index - previous[row['id']] >= 5
        previous[row['id']] = index


def test_seed_is_feasible_published_and_interest_is_unique_idempotent(setup):
    client, path, token = setup
    assert len(rows(path, 'SELECT id FROM members')) == 120
    assert len(rows(path, 'SELECT id FROM menus')) >= 24
    assert state(path)['status'] == 'published'
    check_hard_constraints(entries(path))
    menu_id = 1
    for intent, expected in [('add', 1), ('add', 1), ('remove', 0), ('remove', 0)]:
        response = client.post(f'/interests/{menu_id}', data={'intent': intent, 'csrf': token})
        assert response.status_code == 200
        assert len(rows(path, 'SELECT * FROM interests WHERE member_id=1 AND menu_id=?', (menu_id,))) == expected
    assert client.post('/interests/9999', data={'intent': 'add', 'csrf': token}).status_code == 404
    assert client.post('/interests/1', data={'intent': 'reserve', 'csrf': token}).status_code == 422


def test_role_csrf_and_default_mode_reject_forged_mutations(setup, tmp_path):
    from app.main import create_app

    client, path, token = setup
    original = state(path)
    assert plan_post(client, path, token, 'reopen', role='admin').status_code == 403
    assert client.post('/interests/1', data={'intent': 'add'}).status_code == 403
    admin(client, token)
    assert plan_post(client, path, 'bad', 'reopen').status_code == 403
    assert client.post('/interests/1', data={'intent': 'add', 'csrf': token}).status_code == 403
    assert state(path) == original
    with TestClient(create_app(tmp_path / 'locked.sqlite3', False)) as locked:
        locked_token = csrf(locked)
        assert locked.post('/demo/switch', data={'role': 'admin', 'csrf': locked_token}).status_code == 403
        assert locked.post('/plans/reopen', data={'role': 'admin', 'version': 1, 'month': '2026-11', 'csrf': locked_token}).status_code == 403


def test_published_lock_stale_version_and_old_publication_are_preserved(setup):
    client, path, token = setup
    admin(client, token)
    initial = entries(path)
    assert plan_post(client, path, token, 'generate').status_code == 409
    assert plan_post(client, path, token, '2026-11-02/replace', menu_id=28).status_code == 409
    assert plan_post(client, path, token, 'reopen').status_code == 200
    opened_version = state(path)['version']
    assert plan_post(client, path, token, '2026-11-02/replace', menu_id=28).status_code == 200
    changed = entries(path, 'draft')
    assert changed[0]['id'] == 28
    assert entries(path) == initial
    stale = client.post('/plans/publish', data={'csrf': token, 'month': '2026-11', 'version': opened_version})
    assert stale.status_code == 409
    assert entries(path, 'draft') == changed
    client.post('/demo/switch', data={'csrf': token, 'role': 'member'})
    exported = list(csv.DictReader(io.StringIO(client.get('/export.csv?month=2026-11').text.lstrip('\ufeff'))))
    assert int(exported[0]['menu_id']) == initial[0]['id']
    admin(client, token)
    assert plan_post(client, path, token, 'publish').status_code == 200
    assert entries(path)[0]['id'] == 28
    check_hard_constraints(entries(path))


@pytest.mark.parametrize('change', ['budget', 'friday', 'repeat', 'gap', 'unknown', 'date'])
def test_policy_invalid_replacements_roll_back(setup, change):
    client, path, token = setup
    admin(client, token)
    assert plan_post(client, path, token, 'reopen').status_code == 200
    draft = entries(path, 'draft')
    chosen_date, menu_id = '2026-11-02', 28
    if change == 'budget':
        with sqlite3.connect(path) as connection:
            connection.execute("INSERT INTO menus VALUES (99,'비싼 식단','한식',9000,'테스트','[]',0)")
        menu_id = 99
    elif change == 'friday':
        chosen_date = '2026-11-06'
        menu_id = rows(path, 'SELECT id FROM menus WHERE requires_fryer=1')[0]['id']
    elif change == 'repeat':
        repeated = Counter(row['id'] for row in draft)
        menu_id = next(key for key, count in repeated.items() if count == 2)
        chosen_date = next(row['date'] for row in draft if row['id'] != menu_id)
    elif change == 'gap':
        menu_id = draft[0]['id']
        chosen_date = '2026-11-03'
    elif change == 'unknown':
        menu_id = 9999
    elif change == 'date':
        chosen_date = '2026-11-07'
    old_state = state(path)
    response = plan_post(client, path, token, f'{chosen_date}/replace', menu_id=menu_id)
    assert response.status_code in (404, 422)
    assert entries(path, 'draft') == draft
    assert state(path) == old_state


def test_failed_generation_retains_existing_draft_and_version(setup):
    client, path, token = setup
    admin(client, token)
    plan_post(client, path, token, 'reopen')
    with sqlite3.connect(path) as connection:
        connection.execute('UPDATE menus SET price=9000')
    before = rows(path, 'SELECT * FROM plan_entries ORDER BY stage,date')
    old_state = state(path)
    assert plan_post(client, path, token, 'generate').status_code == 422
    assert state(path) == old_state
    assert rows(path, 'SELECT * FROM plan_entries ORDER BY stage,date') == before


def test_generation_csv_accounting_and_persistence(setup):
    from app.main import create_app

    client, path, token = setup
    admin(client, token)
    plan_post(client, path, token, 'reopen')
    assert plan_post(client, path, token, 'generate').status_code == 200
    planned = entries(path, 'draft')
    check_hard_constraints(planned)
    assert plan_post(client, path, token, 'publish').status_code == 200
    response = client.get('/export.csv?month=2026-11')
    exported = list(csv.DictReader(io.StringIO(response.text.lstrip('\ufeff'))))
    assert len(exported) == 21
    assert sum(int(row['price']) for row in exported) == sum(row['price'] for row in planned)
    with TestClient(create_app(path, True)) as restarted:
        assert restarted.get('/export.csv?month=2026-11').text == response.text
        for route in ['/', '/menus?q=두부', '/menus?category=한식&sort=price', '/insights', '/about']:
            assert restarted.get(route).status_code == 200


def test_planner_rejects_schema_correct_policy_violations():
    from app.planner import validate_plan

    menus = [{'id': index, 'price': 7000, 'requires_fryer': False, 'interest_count': index} for index in range(1, 30)]
    dates = ['2026-11-%02d' % day for day in [2,3,4,5,6,9,10,11,12,13,16,17,18,19,20,23,24,25,26,27,30]]
    valid = dict(zip(dates, range(1, 22)))
    assert validate_plan('2026-11', valid, menus) == []
    invalid = {**valid, '2026-11-03': 1}
    assert any('간격' in issue for issue in validate_plan('2026-11', invalid, menus))
    assert validate_plan('2026-11', {**valid, '2026-11-07': 22}, menus)


def test_greedy_and_rotation_are_deterministic_feasible_comparisons(setup):
    from app.planner import build_plan, validate_plan

    _, path, _ = setup
    menus = rows(path, 'SELECT m.*,COUNT(i.member_id) AS interest_count FROM menus m LEFT JOIN interests i ON i.menu_id=m.id GROUP BY m.id')
    greedy = build_plan('2026-11', menus)
    baseline = build_plan('2026-11', menus, strategy='rotation')
    assert build_plan('2026-11', menus) == greedy
    assert validate_plan('2026-11', greedy, menus) == []
    assert validate_plan('2026-11', baseline, menus) == []
    weights = {menu['id']: menu['interest_count'] for menu in menus}
    assert sum(weights[item] for item in greedy.values()) >= sum(weights[item] for item in baseline.values())


def test_concurrent_same_version_allows_only_one_plan_write(setup):
    client, path, token = setup
    admin(client, token)
    old_version = state(path)['version']
    payload = {'csrf': token, 'month': '2026-11', 'version': old_version}
    with ThreadPoolExecutor(max_workers=2) as pool:
        responses = list(pool.map(lambda _: client.post('/plans/reopen', data=payload, follow_redirects=False), range(2)))
    assert sorted(response.status_code for response in responses) == [303, 409]
    assert state(path)['version'] == old_version + 1
    check_hard_constraints(entries(path, 'draft'))


def test_htmx_interest_and_error_are_visible_partials(setup):
    client, _, token = setup
    response = client.post('/interests/1', data={'csrf': token, 'intent': 'add'}, headers={'HX-Request': 'true'})
    assert response.status_code == 200
    assert 'id="menu-1"' in response.text
    assert 'aria-pressed="true"' in response.text
    assert '<!DOCTYPE' not in response.text.upper()
    denied = client.post('/interests/1', data={'csrf': 'bad', 'intent': 'remove'}, headers={'HX-Request': 'true'})
    assert denied.status_code == 403
    assert denied.headers['HX-Retarget'] == '#notice'
    assert denied.headers['HX-Reswap'] == 'outerHTML'
    assert denied.text.count('id="notice"') == 1


def test_new_month_draft_stays_private_until_published(setup):
    client, path, token = setup
    admin(client, token)
    response = client.post('/plans/generate', data={'csrf': token, 'month': '2026-12', 'version': 0})
    assert response.status_code == 200
    assert response.context['plan']['status'] == 'draft'
    assert response.context['stats']['filled'] == 23
    version = response.context['plan']['version']
    client.post('/demo/switch', data={'csrf': token, 'role': 'member'})
    response = client.get('/?month=2026-12')
    assert response.context['stats']['filled'] == 0
    assert response.context['plan']['status'] == 'empty'
    assert len(list(csv.DictReader(io.StringIO(client.get('/export.csv?month=2026-12').text.lstrip('\ufeff'))))) == 0
    admin(client, token)
    assert client.post('/plans/publish', data={'csrf': token, 'month': '2026-12', 'version': version}).status_code == 200
    client.post('/demo/switch', data={'csrf': token, 'role': 'member'})
    assert client.get('/?month=2026-12').context['stats']['filled'] == 23


def test_invalid_month_and_form_values_do_not_change_plan(setup):
    client, path, token = setup
    before = state(path)
    assert client.get('/?month=2026-13').status_code == 422
    assert client.get('/export.csv?month=../secret').status_code == 422
    assert client.post('/demo/switch', data={'csrf': token, 'role': 'owner'}).status_code == 422
    admin(client, token)
    assert client.post('/plans/reopen', data={'csrf': token, 'month': '2026-11', 'version': '1.0'}).status_code == 422
    assert state(path) == before


def test_html_and_csv_escape_untrusted_menu_text(setup):
    client, path, _ = setup
    with sqlite3.connect(path) as connection:
        connection.execute('UPDATE menus SET name=? WHERE id=1', ('=1+1<script>alert(1)</script>',))
    response = client.get('/menus')
    assert '<script>alert(1)</script>' not in response.text
    assert '&lt;script&gt;alert(1)&lt;/script&gt;' in response.text
    records = list(csv.DictReader(io.StringIO(client.get('/export.csv?month=2026-11').text.lstrip('\ufeff'))))
    assert next(row for row in records if row['menu_id'] == '1')['menu_name'].startswith("'=1+1")
