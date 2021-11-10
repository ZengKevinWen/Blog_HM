from django.shortcuts import render,HttpResponse
from django.views import View
# Create your views here.

# 测试自定义中间件(仿写csrf_token)
def test_middleware(request):
    return HttpResponse("测试csrf_token自定义中间件成功")


class RegisterView(View):
    def get(self,request):
        return render(request,'register.html')

class LoginView(View):
    def get(self,request):
        return render(request,'login.html')