
.PHONY: clean all

all: clean
	python setup.py build_ext --inplace

clean:
	python setup.py clean
	rm wolf/*.so
	rm wolf/*.c

