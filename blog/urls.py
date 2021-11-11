from django.urls import path
from blog.views import *
urlpatterns = [
    path('index/',IndexView.as_view(),name='index')
]