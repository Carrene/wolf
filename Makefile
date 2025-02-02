.PHONY: inplace build sdist wheel install develop clean test

inplace:
	python setup.py build_ext --inplace

build:
	python setup.py build

sdist:
	python setup.py sdist

wheel:
	python setup.py bdist_wheel

install:
	pip install .	

develop:
	pip install -e .

clean:
	python setup.py clean
	-rm wolf/*.c
	-rm wolf/*.so

test:
	pytest

