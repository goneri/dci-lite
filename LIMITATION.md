# Current limitation

## /api/v1/topics/$topic_id/components/$component_id does not exist

The following call won't work because of the missing route:

```python
>>> c.topics.first(where='name:OSP13').components.first().delete()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/goneri/git_repos/python-dci/dci/oo.py", line 163, in delete
    uri, r.text))
dci.oo.DCIClientDeleteFailure: failed to delete at http://127.0.0.1:5000/api/v1/topics/$topic_id/components/$component_id: <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.</p>
```

As an alternative, you can do:

```python
c.components[$component_id].delete()
```
