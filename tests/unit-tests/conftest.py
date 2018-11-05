# -*- coding: utf-8 -*-
import dci_lite.client

import json
import pytest
import requests
import sys

import io


def r_answer(content, status_code=200):
    r = requests.Response()
    if sys.version_info < (3, 0):
        bContent = io.BytesIO(content.encode())
    else:
        bContent = io.BytesIO(content.encode('utf-8'))

    r.status_code = status_code
    r.raw = bContent
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
def read_only_env(monkeypatch):
    def f(*a, **b):
        if a[1] == 'http://a/api/v1/jobs':
            data = json.dumps({
                "jobs": [{
                    "id": "1",
                    "name": "jack",
                    "etag": "b"}
                ],
                "_meta": {"count": 1}})
        elif a[1] == 'http://a/api/v1/jobs/1':
            data = json.dumps({
                "job": {
                    "id": "1",
                    "name": "jack",
                    "etag": "b",
                    "updated_at": "2018-10-19T22:56:17.967139",
                    "created_at": "2018-10-19T22:56:17.967139",
                    "team_id": "1"}})
        elif a[1] == 'http://a/api/v1/teams/1':
            data = json.dumps({
                "team": {
                    "id": "1",
                    "name": "A team",
                    "etag": "b",
                    "updated_at": "2018-10-19T22:56:17.967139",
                    "created_at": "2018-10-19T22:56:17.967139"}})
        elif a[1] == 'http://a/api/v1/teams/2':
            data = json.dumps({
                "team": {
                    "id": "2",
                    "name": "Team Rocket!",
                    "etag": "b",
                    "updated_at": "2018-10-19T22:56:17.967139",
                    "created_at": "2018-10-19T22:56:17.967139"}})
        elif a[1] == 'http://a/api/v1/teams':
            data = json.dumps({
                "_meta": {"count": 2},
                "teams": [
                    {
                        "id": "1",
                        "name": "A team"
                    },
                    {
                        "id": "2",
                        "name": "Team Rocket!"
                    }
                ]})
        elif a[1] == 'http://a/api/v1/topics/1':
            data = json.dumps({
                "topic": {
                    "id": "1",
                    "name": "my topic",
                    "etag": "b",
                    "updated_at": "2018-10-19T22:56:17.967139",
                    "created_at": "2018-10-19T22:56:17.967139"}})
        elif a[1] == 'http://a/api/v1/topics/1/teams':
            data = json.dumps({
                "_meta": {"count": 1},
                "teams": [{
                    "id": "1",
                    "name": "A team"
                }]})
        elif a[1] == 'http://a/api/v1/users/1':
            data = json.dumps({
                "user": {
                    "id": "1",
                    "name": u"Bob L'éponge",
                    "team_id": "1"
                }})
        elif a[1] == 'http://a/api/v1/users':
            data = json.dumps({
                "_meta": {"count": 2},
                "users": [{
                    "id": "1",
                    "name": u"Bob L'éponge",
                    "team_id": "1"
                }]})
        elif a[1] == 'http://a/api/v1/components/1':
            data = json.dumps({
                "component": {
                    "id": "1",
                    "name": "my component",
                    "topic_id": "1"
                }})
        elif a[1] == 'http://a/api/v1/components/1/files':
            data = json.dumps({
                "_meta": {"count": 1},
                "files": [{
                    "id": "1",
                    "name": "my component",
                    "topic_id": "1"
                }]})
        else:
            raise Exception('Bad request: %s' % a[1])

        return r_answer(data)
    monkeypatch.setattr(dci_lite.client.Transport, 'get', f)
