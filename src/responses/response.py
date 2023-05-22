from __future__ import annotations
from typing import Any


class Response:
	def __init__(self, data: Any, status: int, single_use:bool=True) -> None:
		self.__data = data
		self.__status = status
		self.__single_use = single_use

	@classmethod
	def from_dict(self, data: dict) -> Response:
		return Response(
			data.get('data'),
			data.get('status'),
			data.get('single_use', True),
		)

	def to_resp(self) -> tuple[dict, int]:
		return self.__data, self.__status

	def is_single_use(self) -> bool:
		return self.__single_use

