from django.conf import settings
from django.http import JsonResponse

from sentry_sdk import capture_exception


class CaptureExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # print("custom middleware before next middleware/view")
        # # Code to be executed for each request before
        # # the view (and later middleware) are called.

        # response = self.get_response(request)

        # # Code to be executed for each response after the view is called
        # print("custom middleware after response or previous middleware")

        # return response

        return self.get_response(request)

    def process_exception(self, request, exception):
        if exception:
            capture_exception(exception)
            return JsonResponse(
                {"success": False, "message": str(exception)}, status=500
            )