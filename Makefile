.PHONY: start test-locally


start:
	@docker-compose up --build -d

clean:
	@docker-compose down

test-locally:
	@python -m unittest discover tests/
