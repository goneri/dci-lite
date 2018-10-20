import dci_lite.client

c = dci_lite.client.DCIClient.for_user(
    dci_login='admin',
    dci_password='admin',
    dci_cs_url='http://localhost:5000')


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
