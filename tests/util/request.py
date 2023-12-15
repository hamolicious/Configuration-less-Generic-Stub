import requests
from .geturl import get_url


def send_request(method: str, url: str, json: dict=None) -> tuple[dict | bytes, int]:
	request_type = {
		'GET': requests.get,
		'HEAD': requests.head,
		'POST': requests.post,
		'PUT': requests.put,
		'DELETE': requests.delete,
		'OPTIONS': requests.options,
		'PATCH': requests.patch,
	}[method]

	kwargs = {}
	if json is not None:
		kwargs = { 'json': json }

	with request_type(f'{get_url()}{url}', **kwargs) as r:
		try:
			return r.json(), r.status_code
		except requests.exceptions.JSONDecodeError:
			return r.content, r.status_code


