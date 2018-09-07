import dateutil.parser

from dciclient.v1.api import context as dci_context
from dciclient.v1.api import base as dci_base

import json.decoder
import os

class Cache():
    def __init__(self):
        self._data = {}
    def set(self, resource, item_id, obj):
        if resource not in self._data:
            self._data[resource] = {}
        self._data[resource][item_id] = obj
        return obj

    def get(self, resource, item_id):
        return self._data[resource][item_id]


cache = Cache()

class DCILiteNotFound(Exception):
    pass


class DCILiteDeleteFailure(Exception):
    pass


class DCIResource():
    def __init__(self, transport, resource, data, parent_resource=None, subresource=None):
        self._transport = transport
        self._resource = resource
        self._parent_resource = parent_resource
        self._subresource = subresource
        self._uri = self._build_uri()
        self._data = data
        self._new_data = {}

    @classmethod
    def from_id(cls, transport, resource, item_id, **kwargs):
        uri = '%s/%s/%s' % (transport.dci_cs_api, resource, item_id)
        try:
            return cache.get(resource, item_id)
        except KeyError:
            pass
        r = transport.get(uri, timeout=dci_base.HTTP_TIMEOUT, params=kwargs)
        if r.status_code == 404:
            raise DCILiteNotFound('resource not found at %s: %s' % (uri, r.text))
        if r.status_code != 200:
            raise(Exception('Failed to get resource %s: %s' % (uri, r.text)))
        obj = cls(transport, resource, list(r.json().values())[0])
        cache.set(resource, item_id, obj)
        return obj

    # TODO: DUP in DCIResourceCollection
    def _build_uri(self):
        if self._subresource:
            return '%s/%s/%s/%s' % (self._transport.dci_cs_api, self._resource, self._parent_resource.id(), self._subresource)
        else:
            return '%s/%s' % (self._transport.dci_cs_api, self._resource)

    def commit(self):
        """Update a specific resource"""
        if not self._new_data:
            return

        uri = self._uri + '/' + self._data['id']
        r = self._transport.put(uri, timeout=dci_base.HTTP_TIMEOUT,
                                headers={'If-match': self._data['etag']},
                                json=self._new_data)
        if r.status_code != 204:
            raise(Exception(r.text))

        # Reinitialize the object
        for i in self._new_data:
            self._data[i] = self._new_data[i]
        self._new_data = {}
        return r


    def download(self, target):
        uri = self._uri + '/' + self._data['id'] + '/content'
        r = self._transport.get(uri, stream=True, timeout=dci_base.HTTP_TIMEOUT)
        r.raise_for_status()
        with open(target + '.part', 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        os.rename(target + '.part', target)
        return r


    def __str__(self):
        return "resource %s\ndata: %s\nuncommited data: %s" % (
            self._uri, self._data, self._new_data)


    def __getattr__(self, name):
        def return_func(name, params={}):
            def attribute(*v):
                if len(v) == 1:
                    self._data[name] = v[0]
                    self._new_data[name] = v[0]
                # Return a datetime object
                if name in ('created_at', 'updated_at'):
                    return dateutil.parser.parse(self._data[name])
                return self._data[name]

            if name in self._data:
                return attribute
            elif name + '_id' in self._data:
                guessed_resource_name = name + 's'
                # NOTE: We should be able to just create a new DCIResource
                # instance here.
                return DCIResource.from_id(self._transport, resource=guessed_resource_name, item_id=self._data[name + '_id'])
            else:
                return DCIResourceCollection(self._transport, self._resource, parent_resource=self, subresource=name)
        return return_func(name)

    def delete(self):
        uri = self._uri + '/' + self._data['id']
        r = self._transport.delete(
            uri, timeout=dci_base.HTTP_TIMEOUT,
            headers={'If-match': self._data['etag']})
        if r.status_code != 204:
            raise DCILiteDeleteFailure('failed to delete at %s: %s' % (
                uri, r.text))


class DCIResourceCollection:
    def __init__(self, transport, resource, parent_resource=None, subresource=None):
        self._transport = transport
        self._resource = resource
        self._parent_resource = parent_resource
        self._subresource = subresource
        self._uri = self._build_uri()


    def _kwargs_to_data(self, kwargs):
        # Handle the FK
        data = {}
        for i in kwargs:
            if hasattr(kwargs[i], 'id'):
                data[i + '_id'] = kwargs[i].id()
            else:
                data[i] = kwargs[i]
        return data

    def _build_uri(self):
        if self._subresource:
            return '%s/%s/%s/%s' % (self._transport.dci_cs_api, self._resource, self._parent_resource.id(), self._subresource)
        else:
            return '%s/%s' % (self._transport.dci_cs_api, self._resource)

    def add(self, **kwargs):
        uri = self._uri

        if 'data' in kwargs and hasattr(kwargs['data'], 'read'):
            r = self._transport.post(
                uri,
                timeout=dci_base.HTTP_TIMEOUT,
                data=kwargs['data'])
        else:
            data = self._kwargs_to_data(kwargs)
            r = self._transport.post(
                uri,
                timeout=dci_base.HTTP_TIMEOUT,
                json=data)
        if r.status_code != 201:
            raise(Exception('Failed to add %s: %s' % (uri, r.text)))
        if self._subresource:
            return DCIResource(self._transport, self._resource, list(r.json().values())[0], parent_resource=self._parent_resource, subresource=self._subresource)
        else:
            return DCIResource(self._transport, self._resource, list(r.json().values())[0])


    def __iter__(self):
        return self.list()


    def __getitem__(self, item_id):
        return self.get(item_id)


    def __delitem__(self, item):
        self.delete(item)


    def get(self, item_id, **kwargs):
        uri = self._uri + '/' + item_id
        try:
            return cache.get(self._resource, item_id)
        except KeyError:
            pass
        r = self._transport.get(uri, timeout=dci_base.HTTP_TIMEOUT, params=kwargs)
        if r.status_code == 404:
            raise DCILiteNotFound('resource not found at %s: %s' % (uri, r.text))
        if r.status_code != 200:
            raise(Exception('Failed to get resource %s: %s' % (uri, r.text)))
        obj = DCIResource(self._transport, self._resource, list(r.json().values())[0])
        cache.set(self._resource, item_id, obj)
        return obj

    def delete(self, item):
        uri = self._uri + '/' + item
        r = self._transport.delete(uri, timeout=dci_base.HTTP_TIMEOUT,
                               headers={'If-match': item.etag()})
        if r.status_code != 204:
            raise DCILiteDeleteFailure('failed to delete at %s: %s' % (
                uri, r.text))
        return r


    def first(self, **kwargs):
        gen = self.list(**kwargs)
        return next(gen)


    def find_or_add(self, **kwargs):
        try:
            return self.first(where='name:%s' % kwargs['name'])
        except StopIteration:
            return self.add(**kwargs)


    def len(self, **kwargs):
        """List all resources"""
        uri = self._uri
        data = self._kwargs_to_data(kwargs)
        id = data.pop('id', None)
        data['limit'] = data.get('limit', 1)

        # Type of resource that we will loop
        resource_type = self._subresource or self._resource

        r = self._transport.get(uri, timeout=dci_base.HTTP_TIMEOUT, params=data)
        if r.status_code == 404:
            raise DCILiteNotFound('Resource not found at %s: %s' % (uri, r.text))
        try:
                j = r.json()
        except (json.decoder.JSONDecodeError):
            raise Exception('Invalid answer from server for %s: %s' % (uri, r.text))
        return j['_meta']['count']

    def count(self, **kwargs):
        return self.len(**kwargs)


    def list(self, **kwargs):
        """List all resources"""
        uri = self._uri
        data = self._kwargs_to_data(kwargs)
        id = data.pop('id', None)
        data['limit'] = data.get('limit', 1000)

        # Type of resource that we will loop
        resource_type = self._subresource or self._resource

        data['offset'] = 0
        while True:
            r = self._transport.get(uri, timeout=dci_base.HTTP_TIMEOUT, params=data)
            if r.status_code == 404:
                raise DCILiteNotFound('resource not found at %s: %s' % (uri, r.text))
            try:
                j = r.json()
                del j['_meta']
            except (KeyError, json.decoder.JSONDecodeError):
                raise Exception('Invalid answer from server for %s: %s' % (uri, r.text))
            items = list(j.values())[0]
            if not len(items):
                break
            for i in items:
                yield DCIResource(self._transport, resource_type, i)
            data['offset'] += data['limit']


    def purge(self):
        uri = self._uri + '/purge'
        r = self._transport.post(uri, timeout=dci_base.HTTP_TIMEOUT)
        if r.status_code != 204:
            raise(Exception('Failed to purge resource %s: %s' % (uri, r.text)))
        return r


class Transport:
    def __init__(self, context):
        self._context = context
        self._session = context.session
        self.dci_cs_api = self._context.dci_cs_api

    def put(self, uri, **kargs):
        r = self._session.put(uri, **kargs)
        return r

    def post(self, uri, **kargs):
        r = self._session.post(uri, **kargs)
        return r

    def delete(self, uri, **kargs):
        r = self._session.delete(uri, **kargs)
        return r

    def get(self, uri, **kargs):
        r = self._session.get(uri, **kargs)
        return r


class DCIClient:

    def __init__(self, dci_login=None, dci_password=None, dci_cs_url=None):
        context = dci_context.build_dci_context(dci_login=dci_login,
                                                dci_password=dci_password,
                                                dci_cs_url=dci_cs_url)
        self._transport = Transport(context)

    def __getattr__(self, resource):
        def return_collection(params={}):
            return DCIResourceCollection(self._transport, resource)
        return return_collection(resource)
