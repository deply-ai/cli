.PHONY: clean

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf deplyai_cli.egg-info/
build:
	python setup.py sdist bdist_wheel

upload: build
	python -m twine upload dist/*