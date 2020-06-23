from django.shortcuts import render, redirect
from django.http import HttpResponse 
from .models import ArticlePost
from .forms import ArticlePostForm
# 引入User模型
from django.contrib.auth.models import User


#使用markdown 对文本进行渲染
import markdown

#文章列表
def article_list(request):
    articles = ArticlePost.objects.all()
    return render(request,'article/list.html',{'articles':articles})

#文章详情
def article_detail(request,id):
    article = ArticlePost.objects.get(id=id)

    article.body = markdown.markdown(article.body,
        extensions=[
        #缩写表格等扩展
        'markdown.extensions.extra',
        #高亮扩展
        'markdown.extensions.codehilite',
        ])
    return render(request,'article/detail.html',{'article':article})

def article_create(request):
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        #判断数据是否满足模型要求（Django内置方法）
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=1)
            new_article.save()
            return redirect('article:article_list')
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        article_post_form = ArticlePostForm()
        return render(request,'article/create.html',{ 'article_post_form': article_post_form })

def article_safe_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("ERROR")

#文章修改
def article_update(request, id):
    article = ArticlePost.objects.get(id=id)
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            return redirect("article:article_detail",id=id)
        else:
            return HttpResponse("表单内容有误，请重新填写")
    else:
        article_post_form = ArticlePostForm()
        return render(request, 'article/update.html', { 'article': article, 'article_post_form': article_post_form })