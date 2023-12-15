from __future__ import annotations
from typing import Any
import time


class Response:
	def __init__(self, data: Any, status: int, single_use:bool=True, delay:int=-1) -> None:
		self.__data = data
		self.__status = status
		self.__single_use = single_use
		self.__delay = delay

	@classmethod
	def from_dict(self, data: dict) -> Response:
		return Response(
			data=data.get('data'),
			status=data.get('status'),
			single_use=data.get('single_use', True),
			delay=data.get('delay', -1),
		)

	def execute_delay(self) -> bool:
		if self.__delay is -1:
			return False

		time.sleep(self.__delay / 1000)
		return True

	def to_resp(self) -> tuple[dict, int]:
		return self.__data, self.__status

	def is_single_use(self) -> bool:
		return self.__single_use

