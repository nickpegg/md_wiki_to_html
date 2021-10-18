all: test

fmt:
	poetry run black md_wiki_to_html tests

test:
	poetry run mypy md_wiki_to_html tests
	poetry run pytest
