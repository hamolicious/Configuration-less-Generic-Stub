import requests
from tests.util import get_url

def assert404(self, route: str):
	with requests.get(f'{get_url()}{route}') as r:
		self.assertEqual(r.status_code, 404)
