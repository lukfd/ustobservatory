init:
	@eval python -m venv venv

build:
	python3 -m pip install .

clean:
	rm -rf build
	rm -rf dist