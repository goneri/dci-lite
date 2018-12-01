# -*- coding: utf-8 -*-

import io


def test_schedule(c, c_rci, my_topic):
    new_component = c.components.add(name='foo', type='aa', topic=my_topic)
    with open('/etc/fstab', 'rb') as fd:
        my_file = new_component.files.add(data=fd)
    assert my_file.id

    new_job = c_rci.jobs.schedule(topic=my_topic)
    assert new_job.id


    jobstate = c.jobstates.add(
            comment='new',
            job=new_job,
            status='new')
    new_file = c.files.add(
        data=io.StringIO(u"my string"),
        jobstate=jobstate,
        name='a file')
    assert new_file.id
