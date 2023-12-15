# not-config.json
This file is definitely not used to configure the basic behaviour of the stub as the stub is configuration-less, regardless, this is the basic overview of how you *would* configure the stub if it used a config file:

```json
{
	"test": { // load different configs based on the contents of APP_ENV environment variable
		"host": "0.0.0.0", // host to bind to
		"port": 3001, // port to bind to
		"config-route": "POST /private/configure", // "METHOD ROUTE" to use for each of the configuration endpoints
		"state-route": "GET /private/state",
		"reset-route": "POST /private/reset",
		"identity-module": { // changes the way that each request is split, header-id will use the Client-Id header, like the IP was used in the state example
			"name": "header-id",
			"args": {
				"header_name": "client-id"
			}
		},
		"not-configured-response": { // default response to use for routes that are not configured
			"data": {},
			"status": 404
		}
	},

	"dev": {
		"host": "0.0.0.0",
		"port": 3001,
		"config-route": "POST /private/configure",
		"state-route": "GET /private/state",
		"reset-route": "POST /private/reset",
		"identity-module": {
			"name": "none"
		},
		"not-configured-response": {
			"data": {},
			"status": 404
		}
	}
}
```
