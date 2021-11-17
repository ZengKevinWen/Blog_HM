from django.urls import path
from blog.views import *
urlpatterns = [
    path('index/',IndexView.as_view(),name='index'),
    path("write/",WreitView.as_view(),name='write'),
    path('detail/',DetailView.as_view(),name='detail')
]