APP=botofarm-service

test:
	$(POETRY) run pytest

up:
	docker compose up --build -d

down:
	docker compose down -v

