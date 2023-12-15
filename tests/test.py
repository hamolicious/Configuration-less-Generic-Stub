import unittest
import requests
from tests.util import get_url, assert404, pretty_print_state
from tests.util.requests import ping, hello
import time


class TestAPI(unittest.TestCase):
	ip = None

	def setUp(self) -> None:
		need_priming = False
		with requests.get(f'{get_url()}/private/state') as r:
			if r.json() == {}:
				need_priming = True

		if need_priming:
			with requests.post(f'{get_url()}/private/configure', json=ping.request) as r:
				r.close()

		with requests.post(f'{get_url()}/private/reset', json={}) as r:
			r.close()

		if self.ip is None:
			with requests.get(f'{get_url()}/private/state') as r:
				data: dict = r.json()
				TestAPI.ip = list(data.keys())[0]

	def test_configure_ping(self) -> None:
		with requests.post(f'{get_url()}/private/configure', json=ping.request) as r:
			r.close()

		with requests.get(f'{get_url()}{ping.url}') as r:
			self.assertEqual(r.json().get('message'), 'pong')
			self.assertEqual(r.status_code, 200)

		assert404(self, ping.url)

	def test_configure_ping_queue(self) -> None:
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

	def test_state(self) -> None:
		with requests.post(f'{get_url()}/private/configure', json=ping.request) as r:
			r.close()

		with requests.get(f'{get_url()}/private/state') as r:
			data: dict = r.json()
			data = data.get(self.ip)

			self.assertEqual(r.status_code, 200)
			self.assertEqual(len(data.get('/ping').get('GET')), 1)
			self.assertEqual(data.get('/ping').get('GET')[0].get('single_use'), True)
			self.assertEqual(data.get('/ping').get('GET')[0].get('data').get('message'), 'pong')

		with requests.get(f'{get_url()}{ping.url}') as r:
			r.close()

		with requests.get(f'{get_url()}/private/state') as r:
			data = r.json().get(self.ip)

			self.assertEqual(r.status_code, 200)
			self.assertEqual(len(data.get('/ping').get('GET')), 0)

	def test_full_reset(self) -> None:
		with requests.post(f'{get_url()}/private/configure', json=ping.request) as r:
			r.close()

		with requests.post(f'{get_url()}/private/configure', json=ping.request) as r:
			r.close()

		with requests.post(f'{get_url()}/private/configure', json=hello.request) as r:
			r.close()

		with requests.post(f'{get_url()}/private/reset', json={}) as r:
			self.assertEqual(r.status_code, 204)

		with requests.get(f'{get_url()}/private/state') as r:
			data: dict = r.json()
			ip = list(data.keys())[0]

			self.assertEqual(r.status_code, 200)
			self.assertEqual(data.get(self.ip), {})

	def test_route_reset(self) -> None:
		with requests.post(f'{get_url()}/private/configure', json=ping.request) as r:
			r.close()

		with requests.post(f'{get_url()}/private/configure', json=ping.request) as r:
			r.close()

		with requests.post(f'{get_url()}/private/configure', json=hello.request) as r:
			r.close()

		with requests.post(f'{get_url()}/private/reset', json={ 'route': '/ping' }) as r:
			self.assertEqual(r.status_code, 204)

		with requests.get(f'{get_url()}/private/state') as r:
			data: dict = r.json()
			data = data.get(self.ip)

			self.assertEqual(r.status_code, 200)
			self.assertEqual(data.get('/ping'), {})
			self.assertNotEqual(data.get('/hello'), {})
			self.assertEqual(len(data.get('/hello').get('GET')), 1)

		with requests.get(f'{get_url()}{hello.url}') as r:
			self.assertEqual(r.status_code, 200)
			self.assertEqual(r.json().get('message'), 'world')

	def test_delay(self) -> None:
		delayed_ping_request = ping.request
		stored_data: dict = delayed_ping_request.get('data')[0]
		print(stored_data)
		stored_data['delay'] = 500
		print(delayed_ping_request)

		with requests.post(f'{get_url()}/private/configure', json=delayed_ping_request) as r:
			r.close()

		start_time = time.time()
		with requests.get(f'{get_url()}{ping.url}') as r:
			self.assertEqual(r.json().get('message'), 'pong')
			self.assertEqual(r.status_code, 200)
		end_time = time.time()

		self.assertGreaterEqual(end_time - start_time, 0.5)


if __name__ == '__main__':
	unittest.main()
