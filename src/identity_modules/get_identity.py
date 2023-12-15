import json
from flask import Flask
from ..util import load_config
from .ip import ip
from .header_id import header_id
from .none import none

def get_identity(app: Flask) -> str:
	config = load_config()
	module = config.get('identity-module').get('name')
	kwargs = config.get('identity-module').get('args', {})

	return {
		'header-id': header_id,
		'ip': ip,
		'none': none,
	}.get(module)(app, **kwargs)



