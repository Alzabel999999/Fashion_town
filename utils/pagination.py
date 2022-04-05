from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict
from rest_framework.utils.urls import replace_query_param


class CustomPagination(PageNumberPagination):

    def get_page_size(self, request):
        page_size = request.GET.get('page_size', 30)
        return page_size

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('last', self.get_last()),
            ('results', data)
        ]))

    def get_last(self):
        last = self.page.paginator.num_pages
        url = self.request.build_absolute_uri()
        if last > 1:
            return replace_query_param(url, self.page_query_param, last)
        return None
