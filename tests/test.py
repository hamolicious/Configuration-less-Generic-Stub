import unittest
import requests
from tests.util import assert404, pretty_print_state, send_request
from tests.util.requests import ping, hello
import time


class TestAPI(unittest.TestCase):
    ip = None

    def setUp(self) -> None:
        send_request('POST', '/private/configure', json=ping.request)
        send_request('POST', '/private/reset', json={})
        response, _ = send_request('GET', '/private/state')
        data: dict = response
        self.ip = list(data.keys())[0]

    def test_configure_ping(self) -> None:
        send_request('POST', '/private/configure', json=ping.request)

        response, status = send_request('GET', ping.url)
        self.assertEqual(response.get('message'), 'pong')
        self.assertEqual(status, 200)

        assert404(self, ping.url)

    def test_configure_ping_queue(self) -> None:
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

        send_request('POST', '/private/configure', json=ping.request)
        send_request('POST', '/private/configure', json=new_request)

        response, status = send_request('GET', ping.url)
        self.assertEqual(response.get('message'), 'pong')
        self.assertEqual(status, 200)

        response, status = send_request('GET', ping.url)
        self.assertEqual(response.get('message'), 'pong-again')
        self.assertEqual(status, 200)

        assert404(self, ping.url)

    def test_state(self) -> None:
        send_request('POST', '/private/configure', json=ping.request)

        response, status = send_request('GET', '/private/state')
        data: dict = response
        data = data.get(self.ip)

        self.assertEqual(status, 200)
        self.assertEqual(len(data.get('/ping').get('GET')), 1)
        self.assertEqual(data.get('/ping').get('GET')
                         [0].get('single_use'), True)
        self.assertEqual(data.get('/ping').get('GET')
                         [0].get('data').get('message'), 'pong')

        send_request('GET', ping.url)

        response, status = send_request('GET', '/private/state')
        data = response.get(self.ip)

        self.assertEqual(status, 200)
        self.assertEqual(len(data.get('/ping').get('GET')), 0)

    def test_full_reset(self) -> None:
        send_request('POST', '/private/configure', json=ping.request)
        send_request('POST', '/private/configure', json=ping.request)
        send_request('POST', '/private/configure', json=hello.request)

        _, status = send_request('POST', '/private/reset', json={})
        self.assertEqual(status, 204)

        response, status = send_request('GET', '/private/state')
        self.assertEqual(status, 200)
        self.assertEqual(response.get(self.ip), {})

        assert404(self, ping.url)

    def test_route_reset(self) -> None:
        send_request('POST', '/private/configure', json=ping.request)
        send_request('POST', '/private/configure', json=ping.request)
        send_request('POST', '/private/configure', json=hello.request)

        _, status = send_request(
            'POST', '/private/reset', json={'route': '/ping'})
        self.assertEqual(status, 204)

        response, status = send_request('GET', '/private/state')

        self.assertEqual(status, 200)
        self.assertEqual(response.get(self.ip).get('/ping'), {})
        self.assertNotEqual(response.get(self.ip).get('/hello'), {})
        self.assertEqual(
            len(response.get(self.ip).get('/hello').get('GET')), 1)

        response, status = send_request('GET', hello.url)
        self.assertEqual(status, 200)
        self.assertEqual(response.get('message'), 'world')

    def test_delay(self) -> None:
        delayed_ping_request = ping.request
        stored_data: dict = delayed_ping_request.get('data')[0]
        stored_data['delay'] = 500

        send_request('POST', '/private/configure', json=delayed_ping_request)

        start_time = time.time()
        response, status = send_request('GET', ping.url)
        self.assertEqual(response.get('message'), 'pong')
        self.assertEqual(status, 200)
        end_time = time.time()

        self.assertGreaterEqual(end_time - start_time, 0.5)

    def test_missing_route(self) -> None:
        req = {
            "method": "GET",
            "data": [
                {
                    "data": {
                        "message": "pong"
                    },
                    "status": 200,
                    "single_use": True,
                }
            ]
        }

        response, status = send_request('POST', '/private/configure', json=req)
        self.assertEqual(response.get('message'), '`route` field is required')
        self.assertEqual(status, 400)
        assert404(self, '/ping')

    def test_missing_method(self) -> None:
        req = {
            "route": "/ping",
            "data": [
                {
                    "data": {
                        "message": "pong"
                    },
                    "status": 200,
                    "single_use": True,
                }
            ]
        }

        response, status = send_request('POST', '/private/configure', json=req)
        self.assertEqual(response.get('message'), '`method` field is required')
        self.assertEqual(status, 400)
        assert404(self, '/ping')


if __name__ == '__main__':
    unittest.main()
