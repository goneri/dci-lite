import dci_lite.client

c = dci_lite.client.DCIClient.for_user(
    dci_login='admin',
    dci_password='admin',
    dci_cs_url='http://localhost:5000')


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
