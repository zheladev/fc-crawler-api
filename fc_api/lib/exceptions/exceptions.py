from typing import List, Dict


class CustomException(Exception):
    def __init__(self, message: str, reason: str, errors: List = None,
                 data: Dict = None, status_code: int = 400):
        if errors is None:
            errors = []

        if data is None:
            data = {}

        self.message = message
        self.reason = reason
        self.data = data
        self.errors = errors
        self.status_code = status_code


class S3Exception(CustomException):
    def __init__(self, message: str, reason: str, errors=None, data=None):
        super().__init__(message, reason, errors, data, status_code=400)


class FileException(CustomException):
    def __init__(self, message: str, reason: str, errors=None, data=None):
        super().__init__(message, reason, errors, data, status_code=400)


class ResourceNotFound(CustomException):
    def __init__(self, message: str, reason: str, errors=None, data=None):
        super().__init__(message, reason, errors, data, status_code=404)


class PermissionDenied(CustomException):
    def __init__(self, message: str, reason: str, errors=None, data=None):
        super().__init__(message, reason, errors, data, status_code=401)


class ResourceAlreadyExists(CustomException):
    def __init__(self, message: str, reason: str, errors=None, data=None):
        super().__init__(message, reason, errors, data, status_code=409)


class MissingParametersException(CustomException):
    def __init__(self, message: str, reason: str, errors=None, data=None):
        super().__init__(message, reason, errors, data, status_code=400)
