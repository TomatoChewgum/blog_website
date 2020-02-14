from django.urls import path

from blog.views import ArticleListView,ArticleDetailView,article_create,article_delete,article_update
# 正在部署的应用的名称
app_name = 'blog'

urlpatterns = [
    # path函数将url映射到视图
    path('', ArticleListView.as_view(), name='index'),
    path('article-list/', ArticleListView.as_view(), name='article-list'),
    path('article-detail/<int:article_id>/', ArticleDetailView.as_view(), name='article-detail'),
    path('article-create/', article_create, name='article-create'),
    path('article-delete/<int:article_id>/', article_delete, name='article-delete'),
    path('article-update/<int:article_id>/', article_update, name='article-update'),
]