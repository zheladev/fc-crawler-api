from typing import List

from pyramid.config import Configurator
from pyramid.events import NewRequest

ALLOWED_ORIGINS: List[str] = []


def add_cors_headers_response_callback(event):
    def cors_headers(request, response):

        allowed_origin = _get_allowed_origin_from(
            request.headers.get('Origin'))

        response.headers.update({
            'Access-Control-Allow-Origin': allowed_origin
        })

        if request.method == 'OPTIONS':
            response.headers.update({
                'Access-Control-Allow-Methods':
                    'POST, GET, DELETE, PUT, OPTIONS, PATCH',
                'Access-Control-Allow-Headers':
                    'Origin, Content-Type, X-Requested-With, Authorization',
                'Access-Control-Max-Age': '86400'
            })
            response.status_code = 200
            return response

    event.request.add_response_callback(cors_headers)


def _get_allowed_origin_from(origin_header_value):
    """
    Returns the allowed origin value from the origin header value.
    - If the allowed_origins registry property is *, sets it
    - If the origin header contains the value from the allowed_origins
        registry property, echoes it
    - If the allowed origin is not in the registry property, return empty
        string which results in the denial of the request.

    :param origin_header_value: the value extracted from the Origin header
    :return: the allowed origin value
    """
    if "*" in ALLOWED_ORIGINS:
        allowed_origin = "*"
    elif origin_header_value in ALLOWED_ORIGINS:
        allowed_origin = origin_header_value
    else:
        allowed_origin = ''
    return allowed_origin


def includeme(config: Configurator):
    settings = config.get_settings()
    for origin in settings["allowed_origins"].split(','):
        ALLOWED_ORIGINS.append(origin)
    config.add_subscriber(add_cors_headers_response_callback, NewRequest)
