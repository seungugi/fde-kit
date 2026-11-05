"""Deterministic feasible heuristics, with an independent full-plan policy validator."""
import calendar
import re
from collections import Counter
from datetime import date

MAX_PRICE = 8000
MAX_REPEATS = 2
MIN_GAP = 5


def month_parts(month):
    if not isinstance(month, str) or not re.fullmatch(r'\d{4}-\d{2}', month):
        raise ValueError('월은 YYYY-MM 형식으로 입력해 주세요.')
    year, number = map(int, month.split('-'))
    if year < 2020 or year > 2100 or number < 1 or number > 12:
        raise ValueError('2020년부터 2100년 사이의 올바른 월을 선택해 주세요.')
    return year, number


def serving_days(month):
    year, number = month_parts(month)
    return [date(year, number, day) for day in range(1, calendar.monthrange(year, number)[1] + 1)
            if date(year, number, day).weekday() < 5]


def validate_plan(month, assignments, menus):
    days = serving_days(month)
    expected = {day.isoformat() for day in days}
    issues = []
    if set(assignments) != expected:
        issues.append('해당 월의 모든 평일에 정확히 한 개의 식단이 필요합니다.')
    by_id = {menu['id']: menu for menu in menus}
    counts = Counter()
    last = {}
    for index, day in enumerate(days):
        menu_id = assignments.get(day.isoformat())
        menu = by_id.get(menu_id)
        if menu is None:
            issues.append(f'{day.isoformat()}: 존재하는 메뉴를 선택해 주세요.')
            continue
        if menu['price'] > MAX_PRICE or menu['price'] <= 0:
            issues.append(f'{day.isoformat()}: 식단 가격은 1~8,000원이어야 합니다.')
        if day.weekday() == 4 and menu['requires_fryer']:
            issues.append(f'{day.isoformat()}: 금요일에는 튀김기를 사용할 수 없습니다.')
        counts[menu_id] += 1
        if counts[menu_id] > MAX_REPEATS:
            issues.append(f'{day.isoformat()}: 같은 메뉴는 월 2회까지만 제공합니다.')
        if menu_id in last and index - last[menu_id] < MIN_GAP:
            issues.append(f'{day.isoformat()}: 같은 메뉴의 간격은 5영업일 이상이어야 합니다.')
        last[menu_id] = index
    return issues


def build_plan(month, menus, strategy='greedy'):
    if strategy not in ('greedy', 'rotation'):
        raise ValueError('지원하지 않는 식단 생성 방식입니다.')
    counts = Counter()
    last = {}
    selected = {}
    rotation = sorted(menus, key=lambda menu: menu['id'])
    cursor = 0
    for index, day in enumerate(serving_days(month)):
        eligible = [menu for menu in menus if 0 < menu['price'] <= MAX_PRICE
                    and counts[menu['id']] < MAX_REPEATS
                    and index - last.get(menu['id'], -MIN_GAP) >= MIN_GAP
                    and not (day.weekday() == 4 and menu['requires_fryer'])]
        if not eligible:
            raise ValueError('조건에 맞는 메뉴가 부족합니다. 메뉴 구성을 확인해 주세요. 기존 식단은 보존됩니다.')
        if strategy == 'greedy':
            chosen = min(eligible, key=lambda menu: (-menu['interest_count'], counts[menu['id']], menu['price'], menu['id']))
        else:
            allowed = {menu['id'] for menu in eligible}
            for offset in range(len(rotation)):
                position = (cursor + offset) % len(rotation)
                if rotation[position]['id'] in allowed:
                    chosen = rotation[position]
                    cursor = (position + 1) % len(rotation)
                    break
        selected[day.isoformat()] = chosen['id']
        counts[chosen['id']] += 1
        last[chosen['id']] = index
    issues = validate_plan(month, selected, menus)
    if issues:
        raise ValueError(' '.join(issues))
    return selected
