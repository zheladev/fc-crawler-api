import json
from typing import NamedTuple, Union
from uuid import UUID

from pyramid.httpexceptions import HTTPException
from pyramid.request import Request
from pyramid.response import Response
from pyramid.view import view_config, forbidden_view_config


class ResourceNotFound(Exception):
    """
    Indicates that a resource was not found with the given params.
    """

    def __init__(self, resource_id: Union[str, UUID]):
        self.resource_id = resource_id


@view_config(context=HTTPException, renderer="json")  # noqa: C901
def http_exception_renderer(exc: HTTPException, request: Request):
    """
    Renders an error JSON from the given HTTPException.

    :param exc: the exception
    :param request: the request
    :return: a formatted JSON error response
    """
    status_code, error = exc.status.split(" ", 1)
    if int(status_code) in [301, 302, 303, 307, 308]:
        return exc

    request.response.status_code = int(status_code)

    strd_error = {
        'reason': error
    }

    if exc.detail:
        if isinstance(exc.detail, dict):
            strd_error["reason"] = exc.detail.get("reason", error)
            strd_error["message"] = exc.detail.get("message", None)
            strd_error["data"] = exc.detail.get("data", {})
            strd_error["errors"] = exc.detail.get("errors", [])
        elif isinstance(exc.detail, ErrorDetails):
            strd_error = exc.detail.to_dict()
        else:
            strd_error["message"] = str(exc)

    return strd_error


@view_config(context=ResourceNotFound, renderer="json")
def resource_not_found_renderer(exc: ResourceNotFound, request: Request):
    """
    Renders an error JSON from the given ResourceNotFound exception.

    :param exc: the exception
    :param request: the request
    :return: a formatted JSON error response
    """
    request.response.status_code = 404

    return ErrorDetails(
        reason="resource_not_found",
        message=f"resource with id '{exc.resource_id}' was not found"
    ).to_dict()


@forbidden_view_config(renderer='json')
def forbidden_view(request: Request):
    """
    Returns a formatted JSON response to the client if the response would be a
    403. The purpose of the implementation of the forbidden view is to
    differentiate between a 403 and a 401 response, because pyramid doesn't
    do that for us.

    :param request: the request
    :return: the error response
    """

    if hasattr(request, 'user') and request.user is not None:
        status = 403
        response = ErrorDetails("forbidden", "you don't have permissions to "
                                             "perform this action")
    else:
        status = 401
        response = ErrorDetails("unauthorized", "you have to be authenticated "
                                                "first")

    return Response(json.dumps(response.to_dict()), status,
                    content_type='application/json',
                    charset='utf-8')


class ErrorDetails(NamedTuple):
    """
    A dataclass which holds common exception information.

    Attrs:
        - reason:      a string which uniquely identifies the type of the error
        - message:     a human readable message about the details of the error
        - data:        any other information related to this error
    """
    reason: str
    message: str
    data: dict = dict()

    def to_dict(self):
        return {
            "reason": self.reason,
            "message": self.message,
            "data": self.data
        }
