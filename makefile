.PHONY: help run-unit-tests

help:
	@echo "available targets:"
	@echo "  make run-unit-tests   - run unit tests in backend/tests"

run-unit-tests:
	@echo "running unit-tests..."
	docker compose exec backend pytest tests