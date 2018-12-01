# python-dci

`python-dci` is a transport layer with a nice API to interact with Distributed-CI.

## Direct access to the REST API

You can this library to directly the DCI API. In this example, we want to retrieve
all the details from a given job:

```python
import dci.client

job_id = '28cd1fe9-f5a8-4f65-8f76-d6b7aa89e08d'

c = dci.client.DCIClient()

uri_tpl = (
    '/jobs/%s'
    '?embed=topic,remoteci,components,rconfiguration')

job_info = c.get(uri_tpl % job_id).json()
print(job_info)
```

## The Object interface

This library also provide an object layer on top of the class DCI API.

```python
import dci.oo

job_id = '28cd1fe9-f5a8-4f65-8f76-d6b7aa89e08d'

c = dci.oo.Engine()
j = c.jobs.get('1')
``
