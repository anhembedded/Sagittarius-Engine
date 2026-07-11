.PHONY: serve build clean

serve:
	.venv/bin/python -m mkdocs serve

build:
	.venv/bin/python -m mkdocs build --strict

clean:
	rm -rf site
