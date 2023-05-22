import json
import requests
from . import get_url


def pretty_print_state():
	with requests.get(f'{get_url()}/private/state') as r:
		data = r.json()

	print(json.dumps(
		data,
		indent=2
	))

