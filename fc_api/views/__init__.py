from pyramid.view import view_config


@view_config(route_name='api.health',
             renderer='json',
             request_method='GET')
def get_health(request):
    """
    Returns an empty 200 response to check the health of the service.

    :param request: the Pyramid request object
    :return: JSON response with trackable string
    """
    return {"platform": "FC Archive API"}
