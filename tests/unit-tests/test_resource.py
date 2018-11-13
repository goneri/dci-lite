# -*- coding: utf-8 -*-
import dci.client

import conftest
import mock


def test_get(c, read_only_env):
    j = c.jobs.get('1')
    assert j.id == '1'
    assert j.created_at.year == 2018


def test_len(c, read_only_env):
    assert c.jobs.len() == 1


def test_delete(c, read_only_env, monkeypatch):
    def mock_delete(*a, **b):
        assert a[1] == 'http://a/api/v1/jobs/1'
        assert b['headers']['If-match'] == 'b'
        return conftest.r_answer(
            '{"_meta": {"count": 1}}',
            status_code=204)
    monkeypatch.setattr(dci.client.Transport, 'delete', mock_delete)

    j = c.jobs.get('1')
    j.delete()


def test_update_uncommited(c, read_only_env):
    j = c.jobs.get('1')
    j.name = 'foo'
    assert j.name == 'foo'


def test_update_set_object(c, read_only_env):
    u = c.users.get('1')
    t2 = c.teams.get('2')
    u.team = t2
    assert u.team.id == t2.id
    assert u.team_id == t2.id
    assert u.team.name == t2.name


def test_update_set_id(c, read_only_env):
    u = c.users.get('1')
    t2 = c.teams.get('2')
    u.team_id = t2.id
    assert u.team.id == t2.id
    assert u.team_id == t2.id
    assert u.team.name == t2.name


def test_refresh(c, read_only_env):
    u = c.users.get('1')
    assert u.name == u"Bob L'éponge"
    u._data['name'] = 'corrupted name'
    assert u.name == 'corrupted name'
    u.refresh()
    assert u.name == u"Bob L'éponge"


def test_commit(c, read_only_env, monkeypatch):
    def mock_put(*a, **b):
        assert a[1] == 'http://a/api/v1/jobs/1'
        assert b['headers']['If-match'] == 'b'
        assert b['json']['name'] == 'foo'
        return conftest.r_answer('{"_meta": {"count": 1}}', status_code=200)
    monkeypatch.setattr(dci.client.Transport, 'put', mock_put)

    j = c.jobs.get('1')
    j.name = 'foo'
    j.commit()
    assert j.name == 'foo'


def test_commit_with_change(c, read_only_env, monkeypatch):
    mock_put = mock.Mock()
    monkeypatch.setattr(dci.client.Transport, 'put', mock_put)

    j = c.jobs.get('1')
    j.commit()
    assert mock_put.call_count == 0


def test_commit_no_change(c, read_only_env, monkeypatch):
    def mock_delete(*a, **b):
        assert False
    monkeypatch.setattr(dci.client.Transport, 'put', mock_delete)
    t = c.teams.get('1')
    t.commit()
    assert True


def test_call_method(c, read_only_env, monkeypatch):
    def mock_post(*a, **b):
        assert a[1] == 'http://a/api/v1/jobs/schedule'
        return conftest.r_answer(
            '{"job": {"id": "4"}}',
            status_code=201)
    monkeypatch.setattr(dci.client.Transport, 'post', mock_post)
    j = c.jobs.schedule()
    assert j.id
