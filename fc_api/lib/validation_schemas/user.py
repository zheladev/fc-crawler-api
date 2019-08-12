from cerberus import Validator

from fc_api.lib.validation_schemas.helper import validate_date_string, \
    validate_int_string


class User(object):

    @staticmethod
    def receiver_param():
        schema = {
            'fc_id': {'validator': validate_int_string,
                           'required': False,
                           'empty': False},
            'name': {'validator': validate_date_string,
                           'required': False},
            'status': {'validator': validate_date_string,
                         'required': False},
            'created_at': {'validator': validate_int_string,
                       'required': False,
                       'empty': False},
            'limit': {'validator': validate_int_string,
                      'required': False,
                      'empty': False},
            'offset': {'validator': validate_int_string,
                    'required': False}
        }

        return Validator(schema, purge_unknown=True)
