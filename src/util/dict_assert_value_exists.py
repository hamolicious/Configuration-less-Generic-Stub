from ..exceptions import API_Error


def dict_assert_value_exists(dict_: dict, value, message_if_none: str):
	if dict_.get(value, None) is None:
		raise API_Error({
			'message': message_if_none,
			'status': 400,
	})
