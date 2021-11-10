from django.urls import path
from user.views import *
urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('',RegisterView.as_view(),name='rs'),
    path("user/",RegisterView.as_view())
]