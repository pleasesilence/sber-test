.PHONY: help run-unit-tests

help:
	@echo "available targets:"
	@echo "  make run-unit-tests   - run unit tests in backend/tests"

run-unit-tests:
	@echo "running unit-tests..."
	cd backend && pytest tests/ -v