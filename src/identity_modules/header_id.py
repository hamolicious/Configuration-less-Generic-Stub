from flask import Flask, request
from ..exceptions import API_Error
import logging


def header_id(app: Flask) -> str:
	with app.app_context():
		client_id = request.headers.get('client-id')
		logging.info(request.headers)
		if client_id is None:
			raise API_Error({
				'message': 'missing `client-id` header',
				'status': 400,
			})

	return client_id
