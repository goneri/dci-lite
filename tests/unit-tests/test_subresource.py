# -*- coding: utf-8 -*-
import dci.client

import conftest

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def test_get_resource(c, read_only_env):
    j = c.jobs.get('1')
    assert j.team.name == 'A team'


def test_get_collection(c, read_only_env):
    my_topic = c.topics.get('1')
    assert my_topic.teams.len() == 1


def test_add_subresource_with_data(c, read_only_env, monkeypatch):
    def mock_post(*a, **b):
        assert a[1] == 'http://a/api/v1/components/1/files'
        assert hasattr(b['data'], 'read')
        return conftest.r_answer(
            u'{"file": {"id": "1"}}',
            status_code=201)

    new_component = c.components.get('1')
    fd = StringIO('fooo')
    monkeypatch.setattr(dci.client.Transport, 'post', mock_post)
    my_file = new_component.files.add(data=fd)
    assert my_file.id == "1"


def test_get_subresource_with_data(c, read_only_env, monkeypatch, tmpdir):
    def mock_get(*a, **b):
        assert a[1] == 'http://a/api/v1/components/1/files/1/content'
        return conftest.r_answer(
            u'fooo',
            status_code=200)

    new_component = c.components.get('1')
    my_file = new_component.files.first()
    assert my_file.id == "1"
    monkeypatch.setattr(dci.client.Transport, 'get', mock_get)
    my_file.download(str(tmpdir.join('file')))
    assert tmpdir.join('file').read() == 'fooo'
