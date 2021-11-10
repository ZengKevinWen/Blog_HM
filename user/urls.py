from django.urls import path
from user.views import *
urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
]



print("hello world ")
print("这里创建分支，并commit一次")
print('这里输出时，表示刚刚已经用master主分支commit一次了，现在再次调用dev--commit')


print("master提交的代码")