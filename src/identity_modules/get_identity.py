import json
from flask import Flask
from .ip import ip
from .header_id import header_id
from .none import none

def get_identity(app: Flask) -> str:
	with open('/app/not-config.json', 'r') as f:
		data = json.load(f)
	module = data.get('identity-module').get('name')
	kwargs = data.get('identity-module').get('args', {})

	return {
		'header-id': header_id,
		'ip': ip,
		'none': none,
	}.get(module)(app, **kwargs)



