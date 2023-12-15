import json
import os


def load_config() -> dict:
	with open('/app/not-config.json', 'r') as f:
		return json.load(f) \
			.get(os.environ.get('APP_ENV').lower())



