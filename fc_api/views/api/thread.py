from pyramid.view import view_defaults, view_config

from fc_api.core.container import Repositories
from fc_api.lib.validation import DataType, validate_data
from fc_api.lib.validation_schemas.thread import Thread as Thread_validator
from fc_api.models import Thread
from fc_api.repositories.thread import ThreadRepository
from fc_api.views.serializer import serialize_thread


@view_defaults(renderer='json')
class ThreadAPI:
    def __init__(self, request):
        self._request = request
        self._thread_repository: ThreadRepository = Repositories.thread()

    @view_config(route_name='threads.detail', request_method='GET')
    def get(self):
        fc_id = self._request.matchdict['fc_id']
        thread: Thread = self._thread_repository.get(fc_id)

        return serialize_thread(thread)

    @view_config(route_name='threads', request_method='GET')
    @validate_data(Thread_validator.receiver_param(),
                   data_type=DataType.URL_PARAM.value)
    def list(self):
        params = self._request.validated_url_params
        threads = self._thread_repository.list(**params)

        return [serialize_thread(thread) for thread in threads]
