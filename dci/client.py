# -*- coding: utf-8 -*-
""""DCI Client"""

import dci.context


class DCIClient:

    def __init__(self, dci_login=None, dci_password=None, dci_client_id=None,
                 dci_api_secret=None, **kwargs):

        if dci_login:
            context = dci.context.build_dci_context(
                dci_login=dci_login,
                dci_password=dci_password,
                **kwargs)
        else:
            context = dci.context.build_signature_context(
                dci_client_id=dci_client_id,
                dci_api_secret=dci_api_secret,
                **kwargs)
        self._context = context
        self._session = context.session
        self.dci_cs_api = self._context.dci_cs_api

    def canonical_uri(self, uri):
        if uri.startswith('/'):
            return "%s%s" % (self.dci_cs_api.rstrip('/'), uri)
        else:
            return uri

    def request(self, verb, uri, **kargs):
        uri = self.canonical_uri(uri)
        action = getattr(self._session, verb)
        return action(uri, **kargs)

    def put(self, uri, **kargs):
        return self.request('put', uri, **kargs)

    def post(self, uri, **kargs):
        return self.request('post', uri, **kargs)

    def delete(self, uri, **kargs):
        return self.request('delete', uri, **kargs)

    def get(self, uri, **kargs):
        return self.request('get', uri, **kargs)
