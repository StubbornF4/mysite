from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .forms import UserLoginForm

'''

首先以GET的方式访问数据，填写数据。
提交数据，以POST再次访问，重定向至article_list
'''
def user_login(request):
    if request.method == 'POST':
        data = request.POST
        print()
        print(data)
        print()
        #form 用于验证数据是否有效
        user_login_form = UserLoginForm(data=data)
        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            #检验用户名，密码是否符合某个数据，符合的话则返回user
            user = authenticate(username=data['username'],password=data['password'])
            if user:
                login(request,user)
                return redirect("article:article_list")
            else:
                return HttpResponse("账号密码错误，请重新输入")
        else:
            return HttpResponse("输入数据有误")
    elif request.method =='GET':
        user_login_form = UserLoginForm()
        return render(request,'userprofile/login.html',{'form': user_login_form})
    else:
        return HttpResponse("请使用GET或POST请求数据")

def user_logout(request):
    logout(request)
    return redirect('article:article_list')
        


