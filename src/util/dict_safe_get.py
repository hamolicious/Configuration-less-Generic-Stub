
def dict_safely_get_deep_value(obj, *args):
	for arg in args:
		obj = obj.get(arg)
		if obj is None:
			return None
	return obj
