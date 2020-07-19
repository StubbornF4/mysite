from django.db import models
# 导入内建的User模型。
from django.contrib.auth.models import User
# timezone 用于处理时间相关事务。
from django.utils import timezone
from django.urls import reverse

class ArticleColumn(models.Model):
    title = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


#博客文章数据类型
class ArticlePost(models.Model):
    #删除方式 级联删除。作者删除，文章也删除
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title =  models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    total_views = models.PositiveIntegerField(default=0)
    column = models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'
    )


    #内部类 Class Meta用于给model 定义元数据
    class Meta:
        ordering = ('-created',)

    #调用对象的str（）方法时的返回值内容
    def __str__(self):
        return self.title

    #获取文章地址(用于重定向)
    def get_absolute_url(self):
        return reverse('article:article_detail',args=[self.id])

