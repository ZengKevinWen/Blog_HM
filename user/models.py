from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
# 用户模型类
class User(AbstractUser):
    # 手机号   这里有点问题(手机号毕竟是11位，不多不少，这里不会定义--就算前段排除了---感觉代码还是不够严谨)
    mobile = models.CharField(unique=True,blank=False,max_length=20)
    # 头像  uoload_to=相对路径(不可以用绝对路径)
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/',blank=True)
    # 用户描述
    user_desc = models.TextField(blank=True)
    class Meta:
        db_table = 'db_user'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.mobile