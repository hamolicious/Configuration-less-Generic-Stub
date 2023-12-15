from flask import Flask, request

def ip(app: Flask) -> str:
	with app.app_context():
		return request.remote_addr

