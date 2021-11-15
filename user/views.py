import re
from random import randint
from django.shortcuts import render,HttpResponse,redirect,reverse
from django.http import HttpResponseBadRequest,JsonResponse # 好像只可以从这里导入
from pymysql import DatabaseError   # 这个是错误类  是在创建User对象失败的应该报该类里面的错误——————————————————————————-记住

from  libs.captcha.captcha import captcha
from  django_redis import get_redis_connection # 创建redis连接的库与方法
from django.views import View
# Create your views here.
import logging
# 创建日志器
from user.models import User

loggings = logging.getLogger("django")

# 测试自定义中间件(仿写csrf_token)
def test_middleware(request):
    return HttpResponse("测试csrf_token自定义中间件成功")

# 注册模型类
class RegisterView(View):
    def get(self,request):
        return render(request,'register.html')

    def post(self,request):
        # 获取参数并判断是否都True
        mobile = request.POST.get("mobile")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        sms_code = request.POST.get("sms_code")
        if not re.match(r'^1[3-9]\d{9}$', str(mobile)):
            return HttpResponseBadRequest("请输入正确手机号")
        if not all([mobile, password, password2, sms_code]):
            return HttpResponseBadRequest("缺少参数")
        if password2 != password:
            return HttpResponseBadRequest("2次密码不对")
        # 判断短信验证码是否正确------------------------------没有设置验证码功能
        # 从redis中获取数据并与验证码比对
        # redis_conn = get_redis_connection("default")
        # sms_code_server = redis_conn.get("sms:%s" % mobile) # 二进制文件转化为字符串s
        # try:
        #     redis_conn.delete("sms:%s" % mobile)
        # except Exception as e:
        #     loggings.error(e)
        # if not sms_code_server:
        #     return HttpResponseBadRequest("验证码过期")
        # if sms_code_server.decode() != sms_code:
        #     return HttpResponseBadRequest("验证码错误")
        # 导入User类创建对象并在try except中
        try:
            User.objects.create_user(username=mobile,password=password2,mobile=mobile)
        except DatabaseError as e:
            loggings.error(e)
            return HttpResponseBadRequest("注册用户失败")
        # 返回 login页面
        return redirect(reverse("user:login"))


from django.contrib.auth import authenticate  # 用户认证方法
from django.contrib.auth import login  # 用户状态保持
# 登录模型类
class LoginView(View):
    def get(self,request):
        return render(request,'login.html',status=201)
    def post(self,request):
        mobile = request.POST.get("mobile")
        password = request.POST.get("password")
        active = request.POST.get("remember")  # 是否记住密码
        if not all([password,mobile]):
            return HttpResponseBadRequest("缺少参数")
        if not re.match(r'^1[3-9]\d{9}$',mobile):
            return HttpResponseBadRequest("请输入正确手机号")
        if not re.match(r'^[0-9a-zA-Z]{8,20}$',password):
            return HttpResponseBadRequest("请安要求输入密码")
        # 使用django提供的方法 authenticate方法进行用户认证  ----该方法是密码与用户名来认证 到model下的User中可以把username该为mobile认证，同时返回值为None 或者User对象
        # 不过该方法有个很大的缺陷  如在创建对象时用 对象.object.create_user(必要字段参数)该方法创建的对象密码是加密的  然后调用authenticate方法来验证是先会对mysql中的密码进行解密 在匹配前段传来的数据
        # 如果你是通过创建对象然后save方法进行数据保存的话，密码是不加密的  调用authencate方法时一样会先解密，但是这个解出来的密码跟前段输入的不匹配 所以会一直返回None 导致后端有数据  就是验证失败
        user = authenticate(mobile=mobile,password=password) # -----------------------这里等一下要把username改为手机号码验证      USERNAME_FIELD = 'mobile'
        if user is None:
            return HttpResponseBadRequest("用户名或者密码错误")
        # 实现状态保持
        login(request,user)  # 在实现状态保持时，会实现session相关的技术--------------------也不是很明白
        # 根据active是否记住下次自动登录
        if active == 'on':                 # 在实现状态保持后，可以设置关闭浏览器后session的保存时间
            request.session.set_expiry(None)    # 关闭浏览器后记住session信息  None默认为2周  如果是通过logout退出就不一样了  全部删除
        else:
            request.session.set_expiry(0)  # 关闭浏览器不记住session信息
        # 与center关联    -----------重点  按道理来说前端传来的是POST请求 在这里与LoginRequiredMixin类连用时，也传来了GET方法 next参数就在GET里面 注意
        # 同时在request中还可以传递FILES类型 User用户对象 很历害 自己刚刚学习，多重复看之前的代码
        next = request.POST
        next2 = request.GET
        ne = next.get("next")
        ne2 = next2.get("next")
        if ne2 == '/center/':
            resp = redirect(reverse('user:center'))
        elif ne2 == '/write/':
            resp = redirect(reverse('blog:write'))
        elif ne2 == '/index/':
            resp = redirect(reverse('blog:index'))
        else:
            resp = redirect(reverse('blog:index'))
        # 设置cookies技术
        resp.set_cookie('is_login',True,max_age=3600)   # 时间为永久 max_age = ~~~
        resp.set_cookie('username',user.username,max_age=3600*1)
        return resp

# 退出登录
from django.contrib.auth import  logout
class LogoutView(View):
    def get(self,request):
        #1 退出登录 logout(request)方法 可以清楚所有session数据(包括那些定时间的session数据  跟叉掉浏览器不一样  这个是web点击退出)
        logout(request)
        # 2 清楚cookies数据
        resp = redirect(reverse('user:login'))
        resp.delete_cookie('username')
        resp.delete_cookie('is_login')
        return resp


# 忘记密码模型类
class ForgetPasswordView(View):
    def get(self,request):
        return render(request,'forget_password.html')
    def post(self,request):
        # 获取参数并判断  手机号 密码  图片验证码(在图片验证码模型类中判断 成功----获得短信验证码)
        mobile = request.POST.get("mobile")
        password = request.POST.get('password')
        password2 = request.POST.get("password2")
        sms_code = request.POST.get("sms_code")
        if not all([mobile,password,password2,sms_code]):
            return JsonResponse({"error":'缺少必要参数'})
        if not re.match(r'^1[3-9]\d{9}$',mobile):
            return HttpResponseBadRequest("手机号码错误")
        if not re.match(r'^[0-9a-zA-Z]{8,20}$',password2):
            return HttpResponseBadRequest("密码错误")
        if  password2 != password:
            return HttpResponseBadRequest("密码不相同")
        # 从这里开始验证短信验证码
                # redis_conn = get_redis_connection('default')
                # sms_code_server = redis_conn.get("sms:%s"%mobile)
                # try:
                #     redis_conn.delete("sms:%s"%mobile)
                # except Exception as e:
                #     loggings.error(e)
                #     print(e)
                # if not sms_code_server | sms_code_server.decode()!= sms_code :         #这种写法自己在尝试　　不知道错没错
                #     return HttpResponseBadRequest("短信验证码过期或短信验证码错误")
        # 修改密码  通过django自带的方法来修改密码  这样还是会加密  还是可以通过authenticate方法认证
        # set_password(密码)---设置密码   check_password(密码)-----校验密码
        # 先获取对象
        try:
            user = User.objects.get(mobile=mobile)
        except Exception as e:
            # 如果没有找到则创建用户
            user = User.objects.create_user(mobile=mobile,username=mobile,password=password)
            return redirect(reverse('user:login'))
        user.set_password(password)  # 密码加密！！！
        user.save()   # 注意  修改密码时要进行save操作
        # 返回登录页面
        return redirect(reverse('user:login'))


# 验证码模型类
class ImagecodeView(View):
    # 创建图片验证码
    def get(self,request):
        #1 从前端获取uuid参数
        uuid = request.GET.get("uuid")
        #2 判断uuid是否存在
        if not uuid:
            return HttpResponseBadRequest("uuid没有收到")
        #3 通过libs包下的captcha.captcha文件下captcha对象的generate_captcha()方法 生成图片二进制文件和验证码(text, out.getvalue())------------这个细节看！！！！！！
        # 注意写法不需要带参数
        text,img_binary = captcha.generate_captcha()
        # 把验证码存入redis中用于注册验证
            # 连接redis数据库
        redis_conn = get_redis_connection('default')
            # 设置验证码时长  这里没有关闭连接，下次创建管道方式
        redis_conn.setex('img:%s'%uuid,300,text)
        # 返回图片二进制文件  同时告诉html是二进制文件---------------------------这个注意写法
        return HttpResponse(img_binary,content_type="image/jpeg")

# 短信验证码模型类---------------因为在hm中用到vue技术。然后还不会该，所以先不用smscode
from ronglian_sms_sdk import SmsSDK
class SmscodeView(View):
    def get(self,request):
        # 发送段信验证码
        #----------------------------------------------------------------------------------------
        # accId ='8a216da87c304531017c6a4cebe50718'
        # accToken ='9d9886d1765643a392e81261601d27a3'  # 这个东西是变动的
        # appId = '8a216da87c304531017c6a4cece3071f'
        # # 创建SDK
        # sdk = SmsSDK(accId,accToken,appId)
        # # 模板 手机号 信息列表--------发送短信
        # resp = sdk.sendMessage('1','15773998780,13762711904',('3838438','5'))
        # return HttpResponse("发送成功")
        #——————————————————————————————————————————————————————————————————————————————————————
        # 通过前端函数把参数传过来
        # 获取参数 mobile uuid img_scs 并判断是否齐全
        image_code= request.GET.get('image_code')
        uuid = request.GET.get('uuid')  # 从redis中获取image_code
        mobile = request.GET.get('mobile')
        if not all([uuid,image_code,mobile]):
            return HttpResponseBadRequest("缺少参数")
        if re.match(r'^1[3-9]\d{9}$',mobile):
            return  HttpResponseBadRequest("请确定手机号正确")
        # 比较图片验证码 --redis中获取
        redis_conn = get_redis_connection('default')
        # 获取的是二进制文件 等一下要转换
        image_code_server = redis_conn.get("img:%s" % uuid)
        try:
            redis_conn.delete('img:%s'%uuid)
        except Exception as e:
            loggings.error(e)
            print(e)
        if not image_code_server:
            return JsonResponse({"error":"图片验证码过期"})
        # lower()转小写
        if  image_code_server.decode().lower()  != image_code.lower():
            return JsonResponse({"error":'验证码错误'})
        # 发送短信验证码
        sms_code = '%06d' % randint(0, 999999)
        # 将验证码输出在控制台，以方便调试
        loggings.info(sms_code)
        # 保存短信验证码到redis中，并设置有效期
        redis_conn.setex('sms:%s' % mobile, 300, sms_code)
        # 开始发送短信，在最上面 然后HTTP返回
        pass

# 个人中心模型类
from django.contrib.auth.mixins import LoginRequiredMixin  # 判断用户是否进行登录 如登录就可以查看center  没有就跳转到login 设置该方法的跳转路径
class CenterView(LoginRequiredMixin,View):
    def get(self,request):
        user = request.user
        print(user)
        context = {
            'user':user
        }
        return render(request,'center.html',context=context)

    def post(self,request):
        #获取参数   # 这里用了一个新的书写方式 注意 获取request中POST方法传值中的参数  和 获取FILES(传输文件都用这种获取如 文本 照片 )中 user(用户认证对象)
        re = request.POST
        username = re.get("username")
        desc = re.get("desc")
        avatar = request.FILES.get("avatar")
        # phone = request.POST.get("phone") # 因为前端中  phone下使用到了disabled标签(表示客户端不可以修改里面的内容) ---所以导入value中的值没有改变  如果通过phone传值就为None 所以要通过user
        user = request.user
        if not username:
            return HttpResponseBadRequest("用户名不能为空")
        # 存入mysql
        try:
            user.username = username
            user.avatar = avatar
            user.user_desc = desc
            user.save()
        except DatabaseError as e:
            loggings.error(e)
            return HttpResponseBadRequest("修改信息失败")
        # 修改cookie信息(按道理来说这里修改了用户的username 前面是设置了cookies但是这里修改了username时，并没有显示新的username而重新退出登录时，则显示更新后的username)
        # 为什么了-----因为cookie是存储在前端中的 在设置cookies时从服务器拿数据变成了固定的值，之后就该cookies跟服务器没有关联，当修改服务器中的用户信息时，更cookie没有关系，所以想要重新修改cookies必须重新设置cookis
        resp = redirect(reverse('user:center'))
        resp.set_cookie('username',user.username)
        return resp