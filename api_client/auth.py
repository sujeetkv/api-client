# -*- coding: utf-8 -*-
from requests.auth import AuthBase


class TokenAuth(AuthBase):
    """Attaches Token Authentication to the given Request object.

    :param token: valid token string.

    :param auth_scheme: HTTP Authentication Scheme e.g. Bearer, OAuth, Token, etc. It can be `None` also.
    """
    def __init__(self, token, auth_scheme='Bearer'):
        self.token = auth_scheme + ' ' + token if auth_scheme else token

    def __call__(self, req):
        req.headers['Authorization'] = self.token
        return req
