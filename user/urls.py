from django.urls import path
from user.views import *
urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
]



print("hello world ")
print("这里创建分支，并commit一次")