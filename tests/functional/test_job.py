import dci_lite.client

c = dci_lite.client.DCIClient.for_user(
    dci_login='admin',
    dci_password='admin',
    dci_cs_url='http://localhost:5000')


def test_create_update_purge_resource():
    new_topic = c.topics.add(name='roberto')
    assert new_topic.name == 'roberto'
    my_topic_search_result = c.topics.first(where='name:roberto')
    assert my_topic_search_result.name == 'roberto'
    assert new_topic.id == my_topic_search_result.id
    new_topic.name = 'boby'
    new_topic.commit()
    assert new_topic.name != my_topic_search_result.name
    my_topic_search_result.refresh()
    assert new_topic.name == my_topic_search_result.name
    c.topics.purge()


def test_create_user_and_team():
    team_rocket = c.teams.add(name='team_rocket')
    assert team_rocket.id
    new_user = c.users.add(
        name='jess',
        team=team_rocket,
        email='jesse@team.rocket',
        # NOTE: server will reject an user creation with
        # password
        password='',
        fullname='Jesse')
    assert new_user.team.name == 'team_rocket'
    new_user.team.name = 'Team Rocket!'
    new_user.team.commit()
    team_rocket.refresh()
    assert team_rocket.name == 'Team Rocket!'


def test_subresource():
    a_team = c.teams.add(name='A_team')
    my_topic = c.topics.add(name='my_totopic')
    topic_cpt = my_topic.teams.len()
    my_topic.teams.add(team=a_team)
    assert my_topic.teams.len() == topic_cpt + 1
    my_topic.teams.delete(a_team)
    assert my_topic.teams.len() == topic_cpt
    my_topic.delete()


def test_schedule():
    team_rocket = c.teams.add(name='team_gryffindor')
    my_remoteci = c.remotecis.add(name='my_remoteci', team=team_rocket)
    my_topic = c.topics.add(name='my_topic')
    my_topic.teams.add(team=team_rocket)
    new_component = c.components.add(name='foo', type='aa', topic=my_topic)
    with open('/etc/fstab') as fd:
        my_file = new_component.files.add(data=fd)
    assert my_file.id

    c_rci = dci_lite.client.DCIClient.for_remoteci(
        dci_client_id=my_remoteci.id,
        dci_api_secret=my_remoteci.api_secret,
        dci_cs_url='http://localhost:5000')

    new_job = c_rci.jobs.schedule(topic=my_topic)
    assert new_job.id
