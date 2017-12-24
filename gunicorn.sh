#! /bin/bash


# Use it for benchmark
# ab -n2000 -c5 -T"application/json;utf8" -p code.json -m VERIFY http://localhost:8081/apiv1/tokens/1/codes

gunicorn --env "WOLF_TRUSTED_HOSTS=http://localhost:8080" --workers 1 --reload --bind :8081 wsgi:app
