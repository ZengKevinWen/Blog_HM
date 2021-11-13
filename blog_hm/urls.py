"""blog_hm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.shortcuts import HttpResponse,render
import logging
# 创建日志器
logger = logging.getLogger('django')
def loggings(request):
    return render(request,'index.html')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(('user.urls','user'),namespace='user')),
    path('',include(("blog.urls",'blog'),namespace="blog")),
]


# # 设置图片获取的同一url ------------------------------------------------------- 在html中修改了图片的路径  这里就可以不用设置同一图片的url  但是面对企业或者大型项目有什么约束
# from django.conf import settings
# from django.conf.urls.static import static   # 其实这个写法我不怎么理解  先记住写法
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)