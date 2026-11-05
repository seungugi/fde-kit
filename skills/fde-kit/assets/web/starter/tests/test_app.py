import re
import sqlite3
from types import SimpleNamespace

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient


def csrf(client):
    response = client.get('/')
    return re.search(r'name="csrf"\s+value="([^"]+)"', response.text).group(1)


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


def test_persistent_board_requires_demo_admin_and_csrf(tmp_path):
    from app.main import create_app

    path = tmp_path / 'board.sqlite3'
    with TestClient(create_app(path, True)) as client:
        token = csrf(client)
        assert client.get('/health').json()['status'] == 'ok'
        assert client.post('/items', data={'title': 'Persistent item', 'csrf': token}).status_code == 403
        assert client.post('/demo/switch', data={'role': 'admin', 'csrf': token}).status_code == 200
        assert client.post('/items', data={'title': 'Persistent item'}).status_code == 403
        assert client.post('/items', data={'title': 'Persistent item', 'csrf': token}).status_code == 200
    with TestClient(create_app(path, True)) as client:
        assert 'Persistent item' in client.get('/').text
        token = csrf(client)
        client.post('/demo/switch', data={'role': 'admin', 'csrf': token})
        with sqlite3.connect(path) as connection:
            item_id = connection.execute('SELECT id FROM items').fetchone()[0]
        assert client.post(f'/items/{item_id}/delete', data={'csrf': token}).status_code == 200
        assert 'Persistent item' not in client.get('/').text


def test_non_demo_cannot_enable_mutations(tmp_path):
    from app.main import create_app

    with TestClient(create_app(tmp_path / 'board.sqlite3', False)) as client:
        token = csrf(client)
        assert client.post('/demo/switch', data={'role': 'admin', 'csrf': token}).status_code == 403
        assert client.post('/items', data={'title': 'No', 'role': 'admin', 'csrf': token}).status_code == 403
