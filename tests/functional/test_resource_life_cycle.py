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
