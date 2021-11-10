from django.shortcuts import HttpResponse
from django.utils.deprecation import MiddlewareMixin

# 自定义一个中间件(本质就是一个类)(仿照csrf_token)------------------csrf_token中间件下有4个方法 process_request  process_view  process_render_temeplates  process_response  process_Exceptions

class MyMiddleWare(MiddlewareMixin):
    # 看视屏中时加上__init__初始化方法没有继承任何类---但是在运行时报错没有发现该类，然后继承MiddlewareMixin类(就可以除掉__init__方法)  下面是看视屏中的写法
    # def __init__(self,request):# 这份后面的参数是根据中间件所依靠的基类所写然后在这里抄上去的 不写的话有错误(但是参数默认为None所有传不传无所谓，但是传了不报错)
    #     # 查看什么时候调用  调用一次
    #     print("__init__")


    # 如 def process_request(self, request):--------------------------------csrf_token中process_request
    # 这个仿写csrt_Token中间件下的process_request  参数（self,request）固定写法-----------------------该方法感觉在url匹配之后请求的(自己在debug中调试中发现，但是视屏说是在url之前)
    def process_request(self,request):
        print("process_request")


    # 仿写csrf_token中间件下的process_view方法  参数(self,request,函数,函数接受的列表值(自己理解),函数接受的字典值(自己理解))-----同时该方法在url到view中执行
    # 如 def process_view(self, request, callback, callback_args, callback_kwargs):--------------------------------csrf_token中process_view
    def process_view(self,request,view_func,*view_args,**view_kwargs):
        print("prcoess_view")

    # 仿写csrf_token中间件下的process_response方法  固定参数如下print是自己加的！！！！！！
    # def process_response(self, request, response)::--------------------------------csrf_token中process_response
    def process_response(self,request,response):
        print("Test-自定义(仿写csrf_token)中间件")
        return response

# 同时把该方法的路径增加到MIDDLEWARE下------就是一个中间件了