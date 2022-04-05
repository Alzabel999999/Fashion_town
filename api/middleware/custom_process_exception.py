from django.http import Http404
from django.utils.deprecation import MiddlewareMixin


class CustomProcessException(MiddlewareMixin):

    def process_exception(self, request, exception):
        if exception:
            raise Http404
