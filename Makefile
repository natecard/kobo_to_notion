lint: 
	ruff check .

lint fix:
	ruff check . --fix

test:
	pytest -v