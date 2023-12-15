from functools import wraps
from ..exceptions import API_Error
import logging


def send_api_error_on_error():
	def _send_api_error_on_error(f):
		@wraps(f)
		def __send_api_error_on_error(*args, **kwargs):
			try:
				return f(*args, **kwargs)
			except API_Error as e:
				data = {'message': e.args[0].get('message')}, e.args[0].get('status')
				logging.info(f'Error handler invoked, {data}')
				return {'message': e.args[0].get('message')}, e.args[0].get('status')

		return __send_api_error_on_error
	return _send_api_error_on_error
