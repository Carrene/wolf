import os

from wolf import wolf

wolf.configure(files=os.environ.get('WOLF_CONFIG_FILE'))
wolf.initialize_models()


def cross_origin_helper_app(environ, start_response):
    def better_start_response(status, headers):
        headers.append(('Access-Control-Allow-Origin', os.environ.get('WOLF_TRUSTED_HOSTS', '*')))
        start_response(status, headers)

    return wolf(environ, better_start_response)


app = cross_origin_helper_app
