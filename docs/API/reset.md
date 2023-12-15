## Reset
Request to `reset-route` allows you to reset the responses for the entire client (by using body of `{}`) or for a single route in the client (by supplying `route` in the body, see below for example)

```json
{
	"route": "/ping" // deletes all data inside of `/ping`
}
```
