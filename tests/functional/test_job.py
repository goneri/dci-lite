# -*- coding: utf-8 -*-


def test_schedule(c, c_rci, my_topic):
    new_component = c.components.add(name='foo', type='aa', topic=my_topic)
    with open('/etc/fstab') as fd:
        my_file = new_component.files.add(data=fd)
    assert my_file.id

    new_job = c_rci.jobs.schedule(topic=my_topic)
    assert new_job.id
