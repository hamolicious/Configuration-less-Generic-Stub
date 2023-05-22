
# Endpoints
- [POST /private/configure](#configure)
- [GET /private/state](#state)
- [GET /*](#get--post)
- [POST /*](#get--post)

## Configure
POST request to `/private/configure` (can be changed, see [not-config.json](#not-configjson)) with the following body structure:
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
			"single_use": true, // wether to remove this response after use
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

## State
GET request to `/private/state` (can be changed, see [not-config.json](#not-configjson)) is used to get the current state of the stub, this will return any and all configured responses; An example of a response sent can be seen below:
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
		}
	}
}
```
Notice that the IP address is also taken into account, this means that the stub can handle multiple concurrent connections from different services and respond separately.

## GET & POST /*
Lastly, making a request to any route other than the 2 previously mentioned will result in one of 2 cases:

### The route is configured
If you have previously created a response configuration for the route, the configured response will be returned and, if `single_use` is `True`, removed from the queue.

### The route is *not* configured
A body-less 404 response will be sent (can be changed, see [not-config.json](#not-configjson)).

## not-config.json
This file is definitely not used to configure the basic behaviour of the stub as the stub is configuration-less, regardless, this is the basic overview of how you *would* configure the stub if it used a config file:
```json
{
	"host": "0.0.0.0", // host to bind to
	"port": 3000, // port to bind to
	"config-route": "/private/configure", // route to use for configuration
	"state-route": "/private/state", // route to use for grabbing the state of the response configuration
	"not-conf-resp": { // what to return if the route is not configured
		"data": {},
		"status": 404
	},
	"default-responses": { // not implemented yet
		"/ping": {
			"GET": {
				"data": { "message": "pong" },
				"status": 200
			}
		}
	}
}
```
