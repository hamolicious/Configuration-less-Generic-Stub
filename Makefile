.PHONY: start test-locally


start:
	@docker-compose up --build -d

test-locally:
	@python -m unittest discover tests/
