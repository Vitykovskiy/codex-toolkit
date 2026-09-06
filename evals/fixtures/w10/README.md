# Local authorization fixture
Requires Python 3.11+ only. app.py models a reachable HTTP request handler with
trusted authenticated actors; the request path remains actor-controlled.
Scope is local synthetic data. To call the handler from this directory:

```sh
python3 -c 'from app import ACTORS, handle_request; print(handle_request("GET", "/documents/a-1", ACTORS["alice"]))'
```

Organization isolation is required for every returned document. The reviewer may
exercise local requests and report evidence, but has no permission to change app.py.
