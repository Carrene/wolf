import os

from wolf import wolf

wolf.configure(files=os.environ.get('WOLF_CONFIG_FILE'))
wolf.initialize_models()


def cross_origin_helper_app(environ, start_response):
    def better_start_response(status, headers):
        headers.append(('Access-Control-Allow-Origin', os.environ.get('WOLF_TRUSTED_HOSTS', '*')))
        headers.append(('Access-Control-Allow-Headers', 'Content-Type, Authorization'))
        headers.append(
            ('Access-Control-Expose-Headers', 'X-Pagination-Count, X-Pagination-Skip, X-Pagination-Take, X-Identity')
        )
        headers.append(
            ('Access-Control-Allow-Methods', 'LOGIN, LIST, UNLOCK, DEACTIVATE, ACTIVATE, DELETE, EXTEND, GET')
        )
        headers.append(('Access-Control-Allow-Credentials', 'true'))
        start_response(status, headers)

    return wolf(environ, better_start_response)