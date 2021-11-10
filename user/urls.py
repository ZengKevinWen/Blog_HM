from django.urls import path
from user.views import *
urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('test_middleware/',test_middleware,),
]



