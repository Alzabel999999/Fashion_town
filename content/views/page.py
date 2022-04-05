from django.http import Http404
from django.utils.translation import activate
from rest_framework import views
from rest_framework.response import Response
from garpix_page.models import Page
from garpix_catalog.models import Category, Product, LivePhotoAlbum
from garpix_order.models import Order
from ..models import News
from user.models import User
from ..contexts.common import common_context
from django.conf import settings
import json
import traceback


def get_instance_by_slug(slug):
    model_list = [Page, Category, Product, LivePhotoAlbum, News, Order]
    for m in model_list:
        instance = m.objects.filter(slug=slug).first()
        if instance:
            return instance
    return None


class PageView(views.APIView):

    def get_object(self, slug):
        obj = get_instance_by_slug(slug)
        if obj:
            return obj
        else:
            return Page.objects.filter(page_type=settings.PAGE_TYPE_404).first()

    def get(self, request, slugs):
        language = "ru"
        if 'HTTP_ACCEPT_LANGUAGE' in request.META:
            language = request.META['HTTP_ACCEPT_LANGUAGE']
        activate(language)

        slug_list = slugs.split('/')
        slug = slug_list.pop(-1)
        page = self.get_object(slug)

        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.pk)
        else:
            user = None

        #try:
        context = page.get_context(object=page, request=request, user=user)
        #except Exception as e:
            #print('error', str(e))
            #traceback.print_tb(e.__traceback__)
            #page = Page.objects.filter(page_type=settings.PAGE_TYPE_500).first()
            #context = page.get_context(object=page, request=request, user=user)

        data = {
            'type': page.page_type,
            'init_state': context,
        }
        return Response(data)
