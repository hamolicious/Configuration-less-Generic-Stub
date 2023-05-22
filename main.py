from flask import Flask, request
from src.middleware import send_api_error_on_error
from src.util import dict_assert_value_exists, dict_safely_get_deep_value
from src.responses import Response, ResponseQueue, ResponseJSONEncoder
from threading import Lock
import json
from gevent.pywsgi import WSGIServer
import os


with open('not-config.json', 'rb') as f:
	config = json.load(f)

app = Flask(__name__)
resp_queue = ResponseQueue()
config_lock = Lock()


@app.route(config.get('config-route'), methods=['POST'])
@send_api_error_on_error()
def private_configure():
	body = request.get_json()

	dict_assert_value_exists(body, 'route', '`route` field is required')
	dict_assert_value_exists(body, 'method', '`method` field is required')
	dict_assert_value_exists(body, 'data', '`data` field is required')

	for data in body.get('data'):
		with config_lock:
			resp_queue.enqueue(
				Response.from_dict(data),
				request.remote_addr,
				body.get('route'),
				body.get('method'),
			)

	return {}, 204


@app.route(config.get('state-route'), methods=['GET'])
@send_api_error_on_error()
def private_state():
	return json.dumps(resp_queue.get_map(), cls=ResponseJSONEncoder), 200


@app.route(config.get('reset-route'), methods=['POST'])
@send_api_error_on_error()
def private_reset():
	print('Route: ' + str(request.get_json().get('route')))
	resp_queue.reset(request.remote_addr, request.get_json().get('route'))
	return Response({}, 204).to_resp()

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
@send_api_error_on_error()
def catch_all(path: str):
	if not path.startswith('/'):
		path = '/' + path

	resp = resp_queue.dequeue(request.remote_addr, path, request.method)
	return resp.to_resp()


if __name__ == '__main__':
	if os.environ.get('APP_ENV') == 'prod':
		http_server = WSGIServer(
			('', 3000), app,
		)
		http_server.serve_forever()
	else:
		app.run(
			host=config.get('host'),
			port=config.get('port')
		)
