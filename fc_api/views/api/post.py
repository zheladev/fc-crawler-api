from pyramid.view import view_defaults, view_config

from fc_api.core.container import Repositories
from fc_api.lib.validation import validate_data, DataType
from fc_api.lib.validation_schemas.post import Post
from fc_api.repositories.post import PostRepository
from fc_api.views.serializer import serialize_post


@view_defaults(renderer='json')
class PostAPI:
    def __init__(self, request):
        self._request = request
        self._post_repository: PostRepository = Repositories.post()

    @view_config(route_name='posts.detail', request_method='GET')
    def get(self):
        fc_id = self._request.matchdict['fc_id']
        post = self._post_repository.get(fc_id)
        return serialize_post(post)

    @view_config(route_name='posts', request_method='GET')
    @validate_data(Post.receiver_param(),
                   data_type=DataType.URL_PARAM.value)
    def list(self):
        params = self._request.validated_url_params
        posts = self._post_repository.list(**params)

        return [serialize_post(post) for post in posts]
