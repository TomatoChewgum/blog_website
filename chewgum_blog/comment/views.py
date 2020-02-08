from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt

from blog.models import ArticlePost

from .models import Comment
from .forms import CommentForm



# 文章评论
@xframe_options_exempt
@login_required(login_url='/userprofile/login/')
def post_comment(request, article_id, parent_comment_id=None):

    # Model.objects.get()会返回Error 500（服务器内部错误）
    # article = ArticlePost.objects.get(id=article_id)

    # get_object_or_404()会返回Error 404
    article = get_object_or_404(ArticlePost, id=article_id)

    # 处理 POST 请求
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user

            if parent_comment_id:

                parent_comment = Comment.objects.get(id=parent_comment_id)
                # 若回复层级超过二级，则转换为二级
                new_comment.parent_id = parent_comment.get_root().id
                # 被回复人
                new_comment.reply_to = parent_comment.user
                new_comment.save()
                return HttpResponse('200 OK')

            new_comment.save()
            # redirect  返回到一个适当的url中：即用户发送评论后，重新定向到文章详情页面
            # 当其参数是一个Model对象时，会自动调用这个Model对象的get_absolute_url()方法
            return redirect(article)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 处理错误请求
    elif request.method == 'GET':
        comment_form = CommentForm()
        context = {
            'comment_form': comment_form,
            'article_id': article_id,
            'parent_comment_id': parent_comment_id,
        }
        return render(request, 'comment/reply.html', context)
        # 处理其他请求
    else:
        return HttpResponse("仅接受GET/POST请求。")