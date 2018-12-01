# -*- coding: utf-8 -*-


def test_create_user_and_team(c, my_team):
    new_user = c.users.add(
        name=u'jésså',
        team=my_team,
        email='jesse@team.rocket',
        # NOTE: server will reject an user creation with
        # no password
        password='',
        fullname='Jesse')
    assert new_user.team.name == u'team_rocket'
    new_user.team.name = u'Team Rocket! :Ð'
    new_user.team.commit()
