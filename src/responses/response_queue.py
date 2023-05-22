from .response import Response
import json
from ..util import dict_safely_get_deep_value


class ResponseQueue:
	def __init__(self) -> None:
		self.__map = {}
		self.__queue: list[Response] = []

		with open('config.json', 'rb') as f:
			config = json.load(f)

		self.__default_response = Response.from_dict(
			config.get('not-conf-resp')
		)

	def __check_queue_exists(self, addr: str, route: str, method: str) -> bool:
		return not dict_safely_get_deep_value(self.__map, addr, route, method) is None

	def get_map(self) -> dict:
		return self.__map.copy()

	def enqueue(self, resp: Response, addr: str, route: str, method: str) -> None:

		if self.__map.get(addr) is None:
			self.__map[addr] = {}

		if self.__map[addr].get(route) is None:
			self.__map[addr][route] = {}

		if self.__map[addr][route].get(method) is None:
			self.__map[addr][route][method] = []

		lst = self.__map[addr][route][method]
		self.__map[addr][route][method] = lst + [resp]

	def dequeue(self, addr: str, route: str, method: str) -> Response:
		if self.__check_queue_exists(addr, route, method) is False:
			return self.__default_response

		if len(self.__map[addr][route][method]) == 0:
			return self.__default_response

		queue = self.__map[addr][route][method]

		if not queue[0].is_single_use():
			return queue[0]

		return queue.pop(0)
