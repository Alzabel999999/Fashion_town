from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect, HttpResponseGone
from garpix_page.models import Page
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView, RedirectView


class ConfirmAPI(APIView):

    def post(self, request, format=None):
        status = None
        try:
            activation_key = request.data.get('activation_key')
            user = get_user_model().objects.get(email_confirmation_key=activation_key)
            status = user.confirm_email(activation_key)
        except Exception:
            status = False
        return Response({'status': status})


class ConfirmEmailView(RedirectView):

    def get(self, request, *args, **kwargs):
        url = self.get_redirect_url(*args, **kwargs)
        if url:
            try:
                activation_key = kwargs.get('activation_key')
                user = get_user_model().objects.filter(email_confirmation_key=activation_key).first()
                user.confirm_email(activation_key)
            except:
                return HttpResponseRedirect(url)
            return HttpResponseRedirect(url)
        else:
            return HttpResponseGone()

    def get_redirect_url(self, *args, **kwargs):
        url = settings.SITE_URL + '/' + Page.objects.filter(page_type=settings.PAGE_TYPE_AUTH).first().slug
        return url

