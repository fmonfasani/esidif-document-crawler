install:
	pip install -e ".[dev]"
	playwright install chromium

test:
	pytest

audit:
	python -m esidif_crawler audit

crawl:
	python -m esidif_crawler crawl --download

manifest:
	python -m esidif_crawler export
