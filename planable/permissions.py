from rest_framework import permissions, status
from rest_framework.exceptions import APIException


class GenericAPIException(APIException):
    """
    raises API exceptions with custom messages and custom status codes
    """

    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "error"

    def __init__(self, detail, status_code=None):
        self.detail = detail
        if status_code is not None:
            self.status_code = status_code


class IsAccountOwner(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        raise GenericAPIException(
            {
                "status": False,
                "code": 400,
                "message": "User not authenticated!",
                "result": status.HTTP_400_BAD_REQUEST,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )