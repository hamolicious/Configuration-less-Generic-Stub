## Configure
Request to `config-route` to configure a new response.

```json
{
	"route": "/ping", // the route that the configuration should apply to
	"method": "GET", // the request method for the route
	"data": [ // response queue
		{
			"data": { // response data
				"message": "pong"
			},
			"status": 200,  // status code to return
			"single_use": true, // *optional* wether to remove this response after use
			"delay": 500, // *optional* ms to delay response for. Useful for load-testing and mimicking dependencies' behaviour (-1 to disable)
		}
	]
}
```
Responses that are `single_use == True` will be discarded once returned. `data` does not have to be JSON object, can also be HTML, see below:
```json
// ...
	"data": "<h1>Hello World</h1>"
// ...
```