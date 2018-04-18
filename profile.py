#! /usr/bin/env python3
import cProfile
cProfile.run('./gunicorn -w1 --bind unix:/tmp/wsgi.s wsgi:app')


