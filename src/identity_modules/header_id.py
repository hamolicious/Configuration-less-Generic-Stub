from flask import Flask, request
from ..exceptions import API_Error
import logging


def header_id(app: Flask, header_name:str='client-id') -> str:
	with app.app_context():
		client_id = request.headers.get(header_name)
		logging.info(request.headers)
		if client_id is None:
			raise API_Error({
				'message': f'missing `{header_name}` header',
				'status': 400,
			})

	return client_id
