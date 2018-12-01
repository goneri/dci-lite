def test_subresource(c):
    a_team = c.teams.add(name='A_team')
    my_topic = c.topics.add(name='my_totopic')
    topic_cpt = my_topic.teams.len()
    my_topic.teams.add(team=a_team)
    assert my_topic.teams.len() == topic_cpt + 1
    my_topic.teams.delete(a_team)
    assert my_topic.teams.len() == topic_cpt
    my_topic.delete()
