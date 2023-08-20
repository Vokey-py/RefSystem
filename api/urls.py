from django.urls import path
from .views import *

urlpatterns = [
    path('svc/', SendVerificationCodeView.as_view(), name='send-verification-code'),
    path('authWVC/', AuthenticateWithVerificationCodeView.as_view(),
         name='authenticate-with-verification-code'),
    path('logout/', LogoutApi.as_view(), name='logout-api'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/refs/', UserProfileRefsView.as_view(), name='user-profile'),
]
