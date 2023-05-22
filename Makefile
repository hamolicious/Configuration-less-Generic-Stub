.PHONY: start test-locally


start:
	@docker-compose up -d

clean:
	@docker-compose down

build:
	@docker build -t hamolicious/configuration-less-generic-stub:1.0.0  .

test-locally:
	@python -m unittest discover tests/
