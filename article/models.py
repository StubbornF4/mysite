from django.db import models
# 导入内建的User模型。
from django.contrib.auth.models import User
# timezone 用于处理时间相关事务。
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
from PIL import Image

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
    tags = TaggableManager(blank=True)
    avatar = models.ImageField(upload_to='article/%Y%m%d/', blank=True)
    
    #内部类 Class Meta用于给model 定义元数据
    class Meta:
        ordering = ('-created',)

    #调用对象的str（）方法时的返回值内容
    def __str__(self):
        return self.title

    #获取文章地址(用于重定向)
    def get_absolute_url(self):
        return reverse('article:article_detail',args=[self.id])

    #保存时处理图片
    def save(self, *args, **kwargs):
        #调用原来的save功能
        article = super(ArticlePost, self).save(*args, **kwargs)

        #not kwargs.get('update_fields')，排除改变total_views时候的save
        if self.avatar and not kwargs.get('update_fields'):
            image = Image.open(self.avatar)
            (x, y ) = image.size
            new_x = 400
            new_y = int(new_x * (y / x))
            resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            resized_image.save(self.avatar.path)

        return article