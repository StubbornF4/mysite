from django.shortcuts import render, redirect
from django.http import HttpResponse 
from .models import ArticlePost
from .forms import ArticlePostForm
from django.contrib.auth.decorators import login_required

#引入User模型
from django.contrib.auth.models import User
#引入分页模块
from django.core.paginator import Paginator
#使用markdown 对文本进行渲染
import markdown
#引入Q对象，用于联合查询
from django.db.models import Q
from comment.models import Comment

#文章列表
def article_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    #是否要搜索内容
    if search:
        #根据最新\最热进行排序
        if order == 'total_views':
            article_list = ArticlePost.objects.filter(
                #__两个下划线， icontains不区分大小写
                Q(title__icontains=search) | 
                Q(body__icontains=search)
            ).order_by('-total_views')
        else:
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
    else:
        #否则会搜索search = NONE
        search = ''
        if order == 'total_views':
            article_list = ArticlePost.objects.all().order_by('-total_views')
        else:
            article_list = ArticlePost.objects.all()


    paginator = Paginator(article_list,2)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    context = {'articles': articles,'order': order, 'search': search }

    return render(request, 'article/list.html', context) 

#文章详情
def article_detail(request,id):
    article = ArticlePost.objects.get(id=id)
    comments = Comment.objects.filter(article=id)

    #浏览量控制
    article.total_views += 1
    article.save(update_fields=['total_views'])

    md = markdown.Markdown(
        extensions=[
        #缩写表格等扩展
        'markdown.extensions.extra',
        #高亮扩展
        'markdown.extensions.codehilite',
        #目录扩展
        'markdown.extensions.toc'
        ]
    )
    article.body = md.convert(article.body)

    context = {'article': article, 'toc': md.toc, 'comments': comments, }

    return render(request,'article/detail.html',context)

def article_create(request):
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        #判断数据是否满足模型要求（Django内置方法）
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=request.user.id)
            new_article.save()
            return redirect('article:article_list')
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        article_post_form = ArticlePostForm()
        return render(request,'article/create.html',{ 'article_post_form': article_post_form })

@login_required(login_url='/userprofile/login/')
def article_safe_delete(request, id):
    article = ArticlePost.objects.get(id=id)
    if request.user != article.author:
        return HttpResponse('抱歉，您无权删除这篇文章。')
    if request.method == 'POST':        
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("ERROR")

#文章修改
@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    article = ArticlePost.objects.get(id=id)
    if request.user != article.author:
        return HttpResponse('抱歉，您无权修改这篇文章。')
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