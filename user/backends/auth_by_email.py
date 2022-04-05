from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    def authenticate(self, request=None, **kwargs):
        UserModel = get_user_model()
        try:
            email = kwargs['username']
            passw = kwargs['password']
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(passw):
                return user
        return None
