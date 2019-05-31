# -*- coding: utf-8 -*-
import os
from json import JSONDecodeError
import requests
from requests.cookies import cookiejar_from_dict
from . import logger
from .errors import APIClientException


class APIResponse(dict):
    """APIResponse class"""
    def __init__(self, response):
        self.response = response
        self.content_type = self.response.headers.get('content-type')
        self.json = {}
        if isinstance(self.content_type, str) and self.content_type.startswith('application/json'):
            try:
                self.json = self.response.json()
            except (JSONDecodeError, TypeError):
                logger.warning(self.__class__.__name__ + ': Invalid JSON data.')
        super().__init__(self.json)


class APIClient(object):
    """APIClient class.

    For most of the parameters see `requests` module docs.

    :param base_url: Base URL of API endpoint.

    :param response_hooks: A list of response hook functions.
    """

    BASE_URL = 'http://localhost:5000'
    req_session = None

    def __init__(self, base_url, params=None, headers=None, auth=None, cookies=None, proxies=None,
            verify=None, cert=None, max_redirects=None, stream=None, response_hooks=None):
        self.BASE_URL = base_url.rstrip('/')
        self.params = params
        self.headers = headers
        self.auth = auth
        self.cookies = cookies
        self.proxies = proxies
        self.verify = verify
        self.cert = cert
        self.max_redirects = max_redirects
        self.stream = stream
        self.response_hooks = response_hooks
        self.init_session()

    def init_session(self):
        self.close_session()
        self.req_session = requests.Session()
        self.req_session.hooks['response'].append(self._log_request)
        if self.params:
            self.req_session.params = self.params
        if self.headers:
            self.req_session.headers.update(self.headers)
        if self.auth:
            self.req_session.auth = self.auth
        if self.cookies:
            self.req_session.cookies = cookiejar_from_dict(self.cookies)
        if self.proxies:
            self.req_session.proxies = self.proxies
        if self.verify is not None:
            self.req_session.verify = self.verify
        if self.cert:
            self.req_session.cert = self.cert
        if self.max_redirects:
            self.req_session.max_redirects = self.max_redirects
        if self.stream is not None:
            self.req_session.stream = self.stream
        if self.response_hooks:
            self.req_session.hooks['response'] += self.response_hooks

    def close_session(self):
        if self.req_session is not None:
            self.req_session.close()
        self.req_session = None

    def __enter__(self):
        if self.req_session is None:
            self.init_session()
        return self

    def __exit__(self, *args):
        self.close_session()

    def _log_request(self, res, *args, **kwargs):
        msg = [self.__class__.__name__ + ': Request - ' + res.request.method.upper() + ' ' + res.request.url]
        msg.append('-' * 80)
        msg.append('    * Request Headers: ' + str(res.request.headers))
        msg.append('    * Request Body: ' + str(res.request.body))
        msg.append('    * Response Time: ' + str(res.elapsed.total_seconds()) + ' seconds')
        msg.append('    * Response Status: ' + str(res.status_code) + ' ' + str(res.reason))
        msg.append('    * Response Headers: ' + str(res.headers))
        msg.append('    * Response Body: ' + str(res.text))
        msg.append('-' * 80)
        logger.debug('\n'.join(msg))

    def request(self, method, path, params=None, data=None, json=None, headers=None, **kwargs):
        """Send request to given API endpoint.

        For other parameters see `request` method of :class:`requests.Session` in `requests` module docs.

        :param method: HTTP Request Method.

        :param path: API endpoint path.
        """
        if self.req_session is None:
            raise APIClientException('Request session closed.')
        res = self.req_session.request(
            method=method,
            url=self.BASE_URL + '/' + str(path).lstrip('/'),
            params=params,
            data=data,
            json=json,
            headers=headers,
            **kwargs
        )
        return APIResponse(res)

    def get(self, path, **kwargs):
        return self.request('GET', path, **kwargs)

    def post(self, path, **kwargs):
        return self.request('POST', path, **kwargs)

    def put(self, path, **kwargs):
        return self.request('PUT', path, **kwargs)

    def patch(self, path, **kwargs):
        return self.request('PATCH', path, **kwargs)

    def delete(self, path, **kwargs):
        return self.request('DELETE', path, **kwargs)

    def head(self, path, **kwargs):
        return self.request('HEAD', path, **kwargs)

    def options(self, path, **kwargs):
        return self.request('OPTIONS', path, **kwargs)
