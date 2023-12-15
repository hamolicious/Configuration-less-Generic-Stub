## State
Request to `state-route` is used to get the current state of the stub, this will return any and all configured responses; An example of a response sent can be seen below:

```json
{
	"127.0.0.1": {
		"/ping": {
			"GET": [
				{
					"data": {
						"message": "pong"
					},
					"status": 200,
					"single_use": true
				}
			]
		},
		"/other-endpoint": {
			"FETCH": [
				{
					"data": {
						"message": "hello world"
					},
					"status": 418,
					"single_use": true
				}
			]
		}
	}
}
```
Notice that the IP address is also taken into account, this means that the stub can handle multiple concurrent connections from different services/tests and respond separately.
The identifier (in this case the IP) can be changed in the `not-config.json` (not) config file, see [config](/docs/config/README.md) section.
