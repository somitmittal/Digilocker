from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import DigilockerAuthView, DigilockerVerifyUserView

urlpatterns = [
    url(r'^start_auth/$', DigilockerAuthView.as_view(), name='digilocker_auth_url'),
    url(r'^verify_user/$', DigilockerVerifyUserView.as_view(), name='digilocker_verify_user_url'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
