# -*- coding: utf-8 -*-
"""Simple Client for API requests

Basic Usage::

    from api_client import APIClient

    client = APIClient('https://httpbin.org')
    res1 = client.get('/anything/one')
    res2 = client.get('/anything/two')
    client.close_session()

Or as a context manager::

    from api_client import APIClient

    with APIClient('https://httpbin.org') as client:
        res1 = client.get('/anything/one')
        res2 = client.get('/anything/two')

HTTP Basic auth example::

    from api_client import APIClient

    client = APIClient('https://httpbin.org', auth=('username', 'password'))

Token auth example::

    from api_client import APIClient
    from api_client.auth import TokenAuth

    client = APIClient('https://httpbin.org', auth=TokenAuth('validtokenstring'))
"""

import os
import logging


logger = logging.getLogger(__name__)

from .base import APIClient, APIResponse
