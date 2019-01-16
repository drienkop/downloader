init:
	pip install -r requirements.txt

flake8:
	flake8

run:
	python downloader.py 3198389