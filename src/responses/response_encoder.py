from typing import Any
from json import JSONEncoder
from .response import Response


class ResponseJSONEncoder(JSONEncoder):
	def default(self, obj: Any) -> dict:
		if isinstance(obj, Response):
			return {
				'data': obj.to_resp()[0],
				'status': obj.to_resp()[1],
				'single_use': obj.is_single_use(),
			}


		return super().default(obj)
