import pytest

import dci.client


@pytest.fixture
def c():
    c = dci.client.DCIClient(
        dci_login='admin',
        dci_password='admin',
        dci_cs_url='http://localhost:5000')
    if c.teams.len() > 1 or c.users.len() > 1:
        pytest.skip("DB is not empty")

    yield c
    for team in c.teams:
        if team.name != 'admin':
            team.delete()
    for topic in c.topics:
        topic.delete()

    c.jobs.purge()
    c.users.purge()
    c.teams.purge()
    c.topics.purge()


@pytest.fixture
def c_rci(my_remoteci):
    return dci.client.DCIClient(
        dci_client_id=my_remoteci.id,
        dci_api_secret=my_remoteci.api_secret,
        dci_cs_url='http://localhost:5000')


@pytest.fixture
def my_team(c, my_topic):
    team_rocket = c.teams.add(name='team_rocket')
    my_topic.teams.add(team=team_rocket)
    return team_rocket


@pytest.fixture
def my_remoteci(c, my_team):
    return c.remotecis.add(name='my_remoteci', team=my_team)


@pytest.fixture
def my_topic(c):
    return c.topics.add(name='my_topic')
