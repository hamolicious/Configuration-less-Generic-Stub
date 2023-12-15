from .response import Response
import json
from ..util import dict_safely_get_deep_value


class ResponseQueue:
	def __init__(self) -> None:
		self.__map = {}
		self.__queue: list[Response] = []

		with open('/app/not-config.json', 'rb') as f:
			config = json.load(f)

		self.__default_response = Response.from_dict(
			config.get('not-configured-response')
		)

	def __check_queue_exists(self, id_: str, route: str, method: str) -> bool:
		return not dict_safely_get_deep_value(self.__map, id_, route, method) is None

	def get_map(self) -> dict:
		return self.__map.copy()

	def enqueue(self, resp: Response, id_: str, route: str, method: str) -> None:
		if self.__map.get(id_) is None:
			self.__map[id_] = {}

		if self.__map[id_].get(route) is None:
			self.__map[id_][route] = {}

		if self.__map[id_][route].get(method) is None:
			self.__map[id_][route][method] = []

		lst = self.__map[id_][route][method]
		self.__map[id_][route][method] = lst + [resp]

	def reset(self, id_: str, route: str) -> None:
		if route is None:
			self.__map[id_] = {}
		else:
			self.__map[id_][route] = {}

	def dequeue(self, id_: str, route: str, method: str) -> Response:
		if self.__check_queue_exists(id_, route, method) is False:
			return self.__default_response

		if len(self.__map[id_][route][method]) == 0:
			return self.__default_response

		queue = self.__map[id_][route][method]

		if not queue[0].is_single_use():
			return queue[0]

		return queue.pop(0)
