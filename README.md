# Configuration-less Generic Stub
Highly flexible and customisable stub for you testing needs.

## High Level Overview
The idea behind this stub is that it 0 configuration or setup, the responses for each path configured before a call (per client), the intended use would be something like this:
0. I am testing an application that sends a request to the server on the `GET /ping` endpoint and the correct behaviour of the server is to send back `{ "message": "pong" }`. What happens to my app if the server times out, crashes or sends back the completely wrong data?
1. We can simulate the latter 2 using this stub, first, lets test the expected behaviour, deploy the app into a testing env, unhook the server and hook up the stub instead.
	A. The test should first prime the endpoint, so the test makes a request directly to the stub on `POST /private/configure` with the data expected by the app (see [Docs](/docs/README.md)).
	B. the test then triggers the required actions and the app therefore makes a request to the stub, the stub then responds with the data that the test primed above, this in turn is received by the app and we can test what the app does.
2. Testing errors is really simple too, you have control over the entire payload and status code, just send back a 500 with whatever the usual error is.

## Documentation
The entire stub is like 150 lines long and is extremely simple, the entirety of the documentation for the server can be found in [Docs](/docs/README.md).

## Whats Next
- [ ] Add url parameter differentiation, call to `/?a=b` will be different to `/?a=c`

## How to
### Test

```bash
make test
```

### Run locally
```bash
make start
```