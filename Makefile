.PHONY: start test-locally

clean:
	@docker-compose down

build:
	@docker build -t hamolicious/configuration-less-generic-stub:1.0.0  .

start: build
	@docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

test: build
	@docker-compose -f docker-compose.yml -f docker-compose.test.yml up -d
	@python -m unittest discover tests/
