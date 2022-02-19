all: fmt test

init:
	poetry install

clean:
	rm -r _output

fmt:
	poetry run black md_wiki_to_html tests

test:
	poetry run mypy md_wiki_to_html tests
	poetry run pytest

test_build:
	# Run a build on the test wiki
	poetry run md_wiki_to_html \
		--verbose \
		render \
		--source tests/example_wiki \
		--template tests/example_wiki/template.html
