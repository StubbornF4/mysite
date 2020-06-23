from django import forms
from django.contrib.auth.models import User

#forms.Form需要手动配置每个字段，它适用于不与数据库进行直接交互的功能
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

