import unittest
import requests
from tests.util import get_url, assert404
from tests.util.requests import ping


class TestAPI(unittest.TestCase):
	def setUp(self) -> None:
		while True: # HACK: this needs to be done properly
			with requests.get(f'{get_url()}{ping.url}') as r:
				if r.status_code == 404:
					return

	def test_configure_ping(self):
		with requests.post(f'{get_url()}/private/configure', json=ping.request) as r:
			r.close()

		with requests.get(f'{get_url()}{ping.url}') as r:
			self.assertEqual(r.json().get('message'), 'pong')
			self.assertEqual(r.status_code, 200)

		assert404(self, ping.url)

	def test_configure_ping_queue(self):
		with requests.post(f'{get_url()}/private/configure', json=ping.request) as r:
			r.close()

		new_request = {
                    "route": "/ping",
                    "method": "GET",
                    "data": [
                        {
                            "data": {
                                "message": "pong-again"
                            },
                            "status": 200,
                        }
                    ]
                }
		new_request['data'][0]['data']['message'] = 'pong-again'
		with requests.post(f'{get_url()}/private/configure', json=new_request) as r:
			r.close()

		with requests.get(f'{get_url()}{ping.url}') as r:
			self.assertEqual(r.json().get('message'), 'pong')
			self.assertEqual(r.status_code, 200)

		with requests.get(f'{get_url()}{ping.url}') as r:
			self.assertEqual(r.json().get('message'), 'pong-again')
			self.assertEqual(r.status_code, 200)

		assert404(self, ping.url)

	def test_state(self):
		expected_state = {
                    "127.0.0.1": {
                        "/ping": {
                            "GET": [
                                {
                                    "data": {
                                        "message": "pong"
                                    },
                                    "status": 200,
                                    "single_use": True
                                }
                            ]
                        }
                    }
                }

		with requests.post(f'{get_url()}/private/configure', json=ping.request) as r:
			r.close()

		with requests.get(f'{get_url()}/private/state') as r:
			data = r.json().get('127.0.0.1')

			self.assertEqual(r.status_code, 200)
			self.assertEqual(len(data.get('/ping').get('GET')), 1)
			self.assertEqual(data.get('/ping').get('GET')[0].get('single_use'), True)
			self.assertEqual(data.get('/ping').get('GET')[0].get('data').get('message'), 'pong')

		with requests.get(f'{get_url()}{ping.url}') as r:
			r.close()

		with requests.get(f'{get_url()}/private/state') as r:
			data = r.json().get('127.0.0.1')

			self.assertEqual(r.status_code, 200)
			self.assertEqual(len(data.get('/ping').get('GET')), 0)


if __name__ == '__main__':
	unittest.main()
