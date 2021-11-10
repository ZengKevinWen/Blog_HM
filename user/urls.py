from django.urls import path
from user.views import *
urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
]


print("master提交的代码")