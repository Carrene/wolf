
.PHONY: clean all dist

all:
	python setup.py build_ext --inplace

clean:
	python setup.py clean
	rm wolf/*.c
	rm wolf/*.so

dist:
	python setup.py sdist bdist_wheel
