import logging
from api_client import APIClient


logging.basicConfig(level=logging.DEBUG)


with APIClient('https://httpbin.org') as client:
    res = client.get('/anything/one')
    print(res)
    print(res.response.status_code)
    print(res.response.headers)
