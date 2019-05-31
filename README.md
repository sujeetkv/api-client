# api-client
Simple Client for API requests

## How to use

```python
from api_client import APIClient
from api_client.auth import TokenAuth


client = APIClient('https://httpbin.org')
res1 = client.get('/anything/one')
res2 = client.get('/anything/two')
client.close_session()

# as a context manager
with APIClient('https://httpbin.org') as client:
    res1 = client.get('/anything/one')
    res2 = client.get('/anything/two')

# for HTTP Basic auth request
client = APIClient('https://httpbin.org', auth=('username', 'password'))

# for token auth request
client = APIClient('https://httpbin.org', auth=TokenAuth('validtokenstring'))
```
