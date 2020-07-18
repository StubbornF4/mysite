from django.db import models
# 导入内建的User模型。
from django.contrib.auth.models import User
# timezone 用于处理时间相关事务。
from django.utils import timezone

#博客文章数据类型
class ArticlePost(models.Model):
    #删除方式 级联删除。作者删除，文章也删除
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title =  models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    total_views = models.PositiveIntegerField(default=0)


    #内部类 Class Meta用于给model 定义元数据
    class Meta:
        ordering = ('-created',)

    #调用对象的str（）方法时的返回值内容
    def __str__(self):
        return self.title

