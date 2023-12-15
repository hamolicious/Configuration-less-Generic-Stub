from flask import Flask, request
from src.middleware import send_api_error_on_error
from src.util import dict_assert_value_exists, dict_safely_get_deep_value
from src.responses import Response, ResponseQueue, ResponseJSONEncoder
from threading import Lock
import json
from gevent.pywsgi import WSGIServer
import os
import logging
from src import identity_modules


logging.basicConfig(level=logging.DEBUG)


with open('not-config.json', 'rb') as f:
	config = json.load(f)

app = Flask(__name__)
resp_queue = ResponseQueue()
config_lock = Lock()
IDENTITY_MODULE = identity_modules.header_id


@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
@send_api_error_on_error()
def catch_all(path: str):
	if not path.startswith('/'):
		path = '/' + path

	if f'{request.method} {path}' == config.get('reset-route'):
		resp_queue.reset(IDENTITY_MODULE(app), request.get_json().get('route'))
		return {}, 204

	if f'{request.method} {path}' == config.get('state-route'):
		return json.dumps(resp_queue.get_map(), cls=ResponseJSONEncoder), 200

	if f'{request.method} {path}' == config.get('config-route'):
		body = request.get_json()

		dict_assert_value_exists(body, 'route', '`route` field is required')
		dict_assert_value_exists(body, 'method', '`method` field is required')
		dict_assert_value_exists(body, 'data', '`data` field is required')

		for data in body.get('data'):
			with config_lock:
				resp_queue.enqueue(
					resp=Response.from_dict(data),
					id_=IDENTITY_MODULE(app),
					route=body.get('route'),
					method=body.get('method'),
				)

		return {}, 204


	resp = resp_queue.dequeue(IDENTITY_MODULE(app), path, request.method)
	resp.execute_delay()
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
			port=config.get('port'),
			debug=True,
		)
