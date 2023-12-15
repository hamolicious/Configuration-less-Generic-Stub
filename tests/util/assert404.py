import requests
from tests.util import get_url
from tests.util import send_request

def assert404(self, route: str):
	_, status = send_request('GET', route)
	self.assertEqual(status, 404)
