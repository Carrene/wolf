
.PHONY: clean all

all: 
	python setup.py build_ext --inplace

clean:
	python setup.py clean
	rm wolf/*.so
	rm wolf/*.c

