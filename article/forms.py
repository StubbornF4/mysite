#引入表单类
from django import forms
from .models import ArticlePost

class ArticlePostForm(forms.ModelForm):
    class Meta:
        #数据模型来源
        model = ArticlePost
        #包含的字段
        fields = ('title', 'body', 'tags')