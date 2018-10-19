import dci_lite.client

import json
import pytest
import requests
import StringIO


def r_answer(content, status_code=200):
    r = requests.Response()
    r.status_code = status_code
    r.raw = StringIO.StringIO(content)
    return r


@pytest.fixture
def c():
    return dci_lite.client.DCIClient.for_user(
        dci_login='admin',
        dci_password='admin',
        dci_cs_url='http://a')


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    monkeypatch.delattr("requests.sessions.Session.request")


@pytest.fixture
def get_job_1(monkeypatch):
    def f(*a, **b):
        assert a[1] == 'http://a/api/v1/jobs/1'
        return r_answer(
            json.dumps({
                "job": {
                    "id": "1",
                    "name": "jack",
                    "etag": "b",
                    "updated_at": "2018-10-19T22:56:17.967139",
                    "created_at": "2018-10-19T22:56:17.967139"}}))
    monkeypatch.setattr(dci_lite.client.Transport, 'get', f)


@pytest.fixture
def get_jobs(monkeypatch):
    def f(*a, **b):
        assert a[1] == 'http://a/api/v1/jobs'
        return r_answer(
            json.dumps({
                "jobs": [{
                    "id": "1",
                    "name": "jack",
                    "etag": "b"}
                ],
                "_meta": {"count": 1}}))
    monkeypatch.setattr(dci_lite.client.Transport, 'get', f)
