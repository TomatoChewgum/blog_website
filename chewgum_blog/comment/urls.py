from django.urls import path


from .views import post_comment
# 正在部署的应用的名称
app_name = 'comment'

urlpatterns = [
    # path函数将url映射到视图
    path('post-comment/<int:article_id>/', post_comment, name='post-comment'),
    path('post-comment/<int:article_id>/<int:parent_comment_id>', post_comment, name='comment_reply'),
]