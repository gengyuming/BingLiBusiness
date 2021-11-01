from django.http.response import JsonResponse
from rest_framework import status as response_status

from base import response_code


class BaseResponse(JsonResponse):
    def __init__(self, code=response_code.SUCCESS[0], message=response_code.SUCCESS[1], value=None, success=True,
                 status=response_status.HTTP_200_OK):
        if code != response_code.SUCCESS[0]:
            success = False
            status = 500
        response_data = dict(
            success=success,
            response_code=code,
            msg=message
        )
        if value is not None:
            response_data['value'] = value
        super().__init__(data=response_data, status=status)
