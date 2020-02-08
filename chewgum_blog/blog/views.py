from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView,ListView,TemplateView
import markdown
from .models import  ArticlePost, Tag, Category
import mistune # markdown 第三方库

# 引入redirect重定向模块
from django.shortcuts import render, redirect
# 引入HttpResponse
from django.http import HttpResponse
# 引入刚才定义的ArticlePostForm表单类
from .forms import ArticlePostForm
# 引入User模型
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
import re

from comment.models import Comment
from comment.forms import CommentForm
# def article_list(request):
#     # 修改变量名称（articles -> article_list）
#     article_list = ArticlePost.objects.all()
#
#     # 每页显示 1 篇文章
#     paginator = Paginator(article_list, 1)
#     # 获取 url 中的页码
#     page = request.GET.get('page')
#     # 将导航对象相应的页码内容返回给 articles
#     articles = paginator.get_page(page)
#
#     context = {'articles': articles }
#     return render(request, 'article/list.html', context)

class ArticleListView(ListView):
    model = ArticlePost
    paginate_by = 10  # 把每页的数量设置为1
    context_object_name = 'article_list' # 如果不设置此项，在模板中需要使用object_list 变量
    template_name = 'article/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('search')
        order = self.request.GET.get('order')
        if search == None:
            search = ''
            if order == 'pv_order':
                context.update({
                    'order': order,'search': search,
                })
            else:
                order = 'normal'
                context.update({
                    'order': order,'search': search,
                })
        else:
            if order == 'pv_order':
                context.update({
                    'order': order, 'search': search,
                })
            else:
                order = 'normal'
                context.update({
                    'order': order, 'search': search,
                })

        return context

    def get_queryset(self):
        """ 重写 queryset ,根据分类过滤 """
        # queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search == None:
            if self.request.GET.get('order') == 'pv_order':
                return ArticlePost.objects.all().order_by('-pv') # 逆序
            else:
                return ArticlePost.latest_posts() #.objects.all() #queryset.latest_posts()
        elif search != None:
            if self.request.GET.get('order') == 'pv_order':
                return ArticlePost.objects.filter(Q(title__icontains=search) | Q(content__icontains=search)).order_by('-pv')
            else:
                return ArticlePost.objects.filter(Q(title__icontains=search) | Q(content__icontains=search))



class ArticleDetailView(DetailView):
    queryset = ArticlePost.latest_posts()
    model = ArticlePost
    template_name = 'article/detail.html'
    context_object_name = 'article'
    pk_url_kwarg = 'article_id'
    md = markdown.Markdown(
         extensions=[
             # 包含 缩写、表格等常用扩展
             'markdown.extensions.extra',
             # 语法高亮扩展
             'markdown.extensions.codehilite',
             'markdown.extensions.toc',
         ])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_id = self.kwargs.get('article_id')
        comments = Comment.objects.filter(article=article_id)
        comment_form = CommentForm()
        context.update({
            'toc': self.md.toc,
            'comments': comments,
            'comment_form': comment_form,
        })
        return context

    def get_object(self, queryset=queryset):
        obj = super(ArticleDetailView, self).get_object()
        # obj = super().get_object(queryset=queryset)
        # obj.content = markdown.markdown(obj.content,
        #                          extensions=[
        #                              # 包含 缩写、表格等常用扩展
        #                              'markdown.extensions.extra',
        #                              # 语法高亮扩展
        #                              'markdown.extensions.codehilite',
        #                              'markdown.extensions.toc',
        #                          ])
        # obj.content = mistune.markdown(obj.content)
        obj.content = self.md.convert(obj.content)
        obj.pv += 1
        obj.save(update_fields=['pv'])
        return obj


@login_required(login_url='/userprofile/login/')
def article_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)

        # print(article_post_form)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中


            new_article = article_post_form.save(commit=False)
            # 指定数据库中 id=1 的用户为作者
            # 如果你进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户的id
            # new_article.author = User.objects.get(id=1)
            new_article.author = User.objects.get(id=request.user.id)
            # 将新文章保存到数据库中
            new_article.save()

            tags = request.POST['tag']

            if tags:
                tags = re.split(",|;|；|，", tags.strip())

                for tag_name in tags:
                    if tag_name == '':
                        continue
                    print("tag_name",tag_name)

                    try:
                        tag_obj = Tag.objects.get(name=tag_name, owner=User.objects.get(id=request.user.id))
                    except Tag.DoesNotExist:
                        tag_obj = Tag(name=tag_name, owner=User.objects.get(id=request.user.id))
                        tag_obj.save()


                    #tag_obj, created= Tag.objects.get_or_create(name=tag_name, owner=User.objects.get(id=request.user.id))
                    # 数据库保存文章和文章标签的对应关系

                    new_article.tag.add(tag_obj)
                    print("@@@@@@@@@@@@@@@@@@@@")
            article_post_form.save_m2m()  # 保存 tags 的多对多关系
            # 完成后返回到文章列表
            return redirect("blog:article-list")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文
        context = {'article_post_form': article_post_form,
                   'category_list': Category.objects.all(),  #.filter(owner=request.user)

                   }
        # 返回模板
        # print(context)
        return render(request, 'article/create.html', context)

# 删文章
def article_delete(request, article_id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=article_id)
        article.delete()
        return redirect("blog:article-list")
    else:
        return HttpResponse("仅允许post请求")

    # article = ArticlePost.objects.get(id=article_id)
    # article.delete()
    # return redirect("blog:article-list")

# 更新文章
@login_required(login_url='/userprofile/login/') # 提醒用户登录
def article_update(request, article_id):
    """
    更新文章的视图函数
    通过POST方法提交表单，更新titile、body字段
    GET方法进入初始表单页面
    """
    # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(id=article_id)
    # 过滤非作者的用户
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")
    # 判断用户是否为 POST 提交表单数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        print(article_post_form)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存新写入的 title、body 数据并保存
            article.title = request.POST['title']
            article.category = Category.objects.get(id=request.POST['category'])
            article.content = request.POST['content']

            tags = request.POST['tag']
            article.tag.clear()
            if tags:
                tags = re.split(",|;|；|，", tags.strip())

                for tag_name in tags:
                    if tag_name == '':
                        continue
                    print("tag_name", tag_name)

                    try:
                        tag_obj = Tag.objects.get(name=tag_name, owner=User.objects.get(id=request.user.id))
                    except Tag.DoesNotExist:
                        tag_obj = Tag(name=tag_name, owner=User.objects.get(id=request.user.id))
                        tag_obj.save()

                    # tag_obj, created= Tag.objects.get_or_create(name=tag_name, owner=User.objects.get(id=request.user.id))
                    # 数据库保存文章和文章标签的对应关系

                    article.tag.add(tag_obj)
            article.save()


            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("blog:article-detail", article_id=article_id)
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    # 如果用户 GET 请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm(initial={'category': article.category.id})
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        tag_list = article.tag.all()
        tag_str = ''
        for tag in tag_list:
            tag_str += tag.name + ';'
        context = {'article': article,
                   'article_post_form': article_post_form,
                   'category_list': Category.objects.all(),
                   'tag_list': tag_str,
                   }
        # 将响应返回到模板中
        return render(request, 'article/update.html', context)