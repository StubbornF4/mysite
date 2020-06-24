from django.db import models
from django.contrib.auth.models import User
#引入内置信号
from django.db.models.signals import post_save
#引入信号接收器的接收器
from django.dispatch import receiver


#用户信息扩展
class Profile(models.Model):
    #与User模型构成一对一的关系
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatar/%Y%m%d', blank=True)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f'user {self.user.username}'

'''

Django包含一个“信号调度程序”:它可以在框架中的某些位置发生操作时，通知其他应用程序。
简而言之，信号允许某些发送者通知一组接收器已经发生了某个动作。
当许多代码可能对同一事件感兴趣时，信号就特别有用。

这里引入的post_save就是一个内置信号，它可以在模型调用save()方法后发出信号。
有了信号之后还需要定义接收器，告诉Django应该把信号发给谁。装饰器receiver就起到接收器的作用。
每当User有更新时，就发送一个信号启动post_save相关的函数。
'''
""" #信号接收函数，每当新建User实例时自动调用
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

#信号接收函数，每当更新User实例时自动调用
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save() """
