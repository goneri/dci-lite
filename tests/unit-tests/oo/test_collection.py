# -*- coding: utf-8 -*-
import pytest

import dci.oo

import conftest


def mock_get(*a, **b):
    assert a[1] == 'http://a/api/v1/teams'
    assert b['params']['where'] == "name:Bob L'éponge"
    return conftest.r_answer(
        '{"_meta": {"count": 0}, "teams": []}',
        status_code=201)


def mock_post(*a, **b):
    assert a[1] == 'http://a/api/v1/teams'
    return conftest.r_answer(
        '{"team": {"name": "Habs", "id": "3"}}',
        status_code=201)


def mock_post_failure(*a, **b):
    assert a[1] == 'http://a/api/v1/teams'
    return conftest.r_answer(
        'Nooope!',
        status_code=500)


def mock_delete(*a, **b):
    assert a[1] == 'http://a/api/v1/teams/1'
    return conftest.r_answer(
        '',
        status_code=204)


def test_find_or_add_exists(c, read_only_env):
    t = c.users.find_or_add(name="Bob L'éponge")
    assert t.id == '1'


def test_find_or_add_creates(c, read_only_env, monkeypatch):
    monkeypatch.setattr(dci.client.DCIClient, 'get', mock_get)
    monkeypatch.setattr(dci.client.DCIClient, 'post', mock_post)
    t = c.teams.find_or_add(name="Bob L'éponge")
    assert t.id == '3'


def test_add(c, monkeypatch):
    monkeypatch.setattr(dci.client.DCIClient, 'post', mock_post)
    t = c.teams.add(name='Habs')
    assert t.id == '3'


def test_add_failure(c, monkeypatch):
    monkeypatch.setattr(dci.client.DCIClient, 'post', mock_post_failure)
    with pytest.raises(dci.oo.DCIClientFailure) as excinfo:
        c.teams.add(name='Habs')


def test_len(c, read_only_env):
    assert c.teams.len() == 2


def test_list(c, read_only_env):
    cpt = 0
    for _ in c.teams:
        cpt += 1
    assert cpt == 2


def test_first(c, read_only_env):
    assert c.teams.first().name == "A team"


def test_delete(c, read_only_env, monkeypatch):
    monkeypatch.setattr(dci.client.DCIClient, 'delete', mock_delete)
    t = c.teams['1']
    del c.teams[t]
