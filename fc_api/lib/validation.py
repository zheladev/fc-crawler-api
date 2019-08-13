import functools
from enum import Enum
from json.decoder import JSONDecodeError

from pyramid.httpexceptions import HTTPBadRequest


class DataType(Enum):
    JSON_BODY = 'json'
    URL_PARAM = 'url_params'
    URL_DICT = 'url_matchdict'


def check_int(s):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()


def convert_ints(d):
    d = d
    for k, v in d.items():
        if check_int(v):
            d[k] = int(v)
    return d


def validate_data(schema, data_type=DataType.JSON_BODY.value):  # noqa: C901
    def get_data_from_request(request, data_type):
        """
        Fetches the data from the request object

        :param request: pyramid request
        :param data_type: type of data that need to be fetched
        :return: request data
        """
        data = None

        if data_type == DataType.JSON_BODY.value:
            try:
                data = request.json_body
            except JSONDecodeError:
                data = dict(request.POST)

        elif data_type == DataType.URL_PARAM.value:
            data = convert_ints(dict(request.GET))

        elif data_type == DataType.URL_DICT.value:
            data = dict(request.matchdict)

        if data is None:
            raise HTTPBadRequest('No data was provided')

        return data

    def wrap(f):
        @functools.wraps(f)
        def wrapper(api):
            request = api._request

            data = get_data_from_request(request, data_type)
            validated = schema.validate(data)

            if data and not validated:
                raise HTTPBadRequest(format_error_message(schema.errors))
            if data_type == DataType.JSON_BODY.value:
                request.validated_data = schema.document
            elif data_type == DataType.URL_PARAM.value:
                request.validated_url_params = schema.document
            elif data_type == DataType.URL_DICT.value:
                request.validated_url_id = schema.document
            return f(api)

        return wrapper

    return wrap


def format_error_message(errors):
    """
    Format errors to more human readable text
    """
    reply = "Found the following errors: "
    fields = []

    def parse_error(errors_, error_string=''):
        for error in errors_:

            if isinstance(error, dict):
                parsed_errors = []
                for key, value in error.items():

                    parsed_error = parse_error(value, error_string)
                    if not isinstance(key, int):
                        parsed_error = '{}: {}'.format(key, parsed_error)

                    parsed_errors.append(parsed_error)
                error = ', '.join(parsed_errors)
            error_string += error

        return error_string

    for field, error_fields in errors.items():
        fields.append('{}: {}'.format(field, parse_error(error_fields)))

    reply += '; '.join(fields)

    return reply
