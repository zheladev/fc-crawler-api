from pyramid.view import view_defaults, view_config

from fc_api.core.container import Repositories
from fc_api.lib.validation import validate_data, DataType
from fc_api.lib.validation_schemas.user import User as User_validator
from fc_api.repositories.user import UserRepository
from fc_api.views.serializer import serialize_user


@view_defaults(renderer='json')
class UserAPI:
    def __init__(self, request):
        self._request = request
        self._user_repository: UserRepository = Repositories.user()

    @view_config(route_name='users.detail', request_method='GET')
    def get(self):
        fc_id = self._request.matchdict['fc_id']
        user = self._user_repository.get(fc_id)
        return serialize_user(user)

    @view_config(route_name='users', request_method='GET')
    @validate_data(User_validator.receiver_param(),
                   data_type=DataType.URL_PARAM.value)
    def list(self):
        params = self._request.validated_url_params
        users = self._user_repository.list(**params)

        return [serialize_user(user) for user in users]
