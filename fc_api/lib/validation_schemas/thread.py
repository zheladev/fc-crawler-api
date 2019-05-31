from cerberus import Validator

from fc_api.lib.validation_schemas.helper import validate_date_string, \
    validate_int_string


class Thread(object):

    @staticmethod
    def receiver_param():
        schema = {
            'user_fc_id': {'validator': validate_int_string,
                           'required': False,
                           'empty': False},
            'start_date': {'validator': validate_date_string,
                           'required': False},
            'end_date': {'validator': validate_date_string,
                         'required': False},
            'offset': {'validator': validate_int_string,
                       'required': False,
                       'empty': False},
            'limit': {'validator': validate_int_string,
                      'required': False,
                      'empty': False},
        }

        return Validator(schema, purge_unknown=True)
