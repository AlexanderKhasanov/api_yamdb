from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

app_name = 'users'

urlpatterns = [
    path(
        'v1/auth/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
]
