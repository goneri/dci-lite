import dci_lite.client

import conftest


def test_get(c, get_job_1):
    j = c.jobs.get('1')
    assert j.id == '1'
    assert j.created_at.year == 2018


def test_len(c, get_jobs):
    assert c.jobs.len() == 1


def test_delete(c, get_job_1, monkeypatch):
    def mock_delete(*a, **b):
        assert a[1] == 'http://a/api/v1/jobs/1'
        assert b['headers']['If-match'] == 'b'
        return conftest.r_answer('{"_meta": {"count": 1}}', status_code=204)
    monkeypatch.setattr(dci_lite.client.Transport, 'delete', mock_delete)

    j = c.jobs.get('1')
    j.delete()


def test_update_uncommited(c, get_job_1):
    j = c.jobs.get('1')
    j.name = 'foo'
    assert j.name == 'foo'


def test_commit(c, get_job_1, monkeypatch):
    def mock_put(*a, **b):
        assert a[1] == 'http://a/api/v1/jobs/1'
        assert b['headers']['If-match'] == 'b'
        assert b['json']['name'] == 'foo'
        return conftest.r_answer('{"_meta": {"count": 1}}', status_code=200)
    monkeypatch.setattr(dci_lite.client.Transport, 'put', mock_put)

    j = c.jobs.get('1')
    j.name = 'foo'
    j.commit()
    assert j.name == 'foo'
