"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('article/', include('article.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static


import notifications.urls

""" 配置 RSS 和 sitemap 的urls"""
from django.contrib.sitemaps import views as sitemap_views

urlpatterns = [

    # path('',post_list, name='index'),
    # re_path("category/(?P<category_id>\d+)/", post_list, name='category-list'),
    # re_path('tag/(?P<tag_id>\d+)/', post_list, name='tag-list'),
    # re_path('post/(?P<post_id>\d+).html',post_detail, name='post-detail'),

    # path('', PostListView.as_view(), name='index'),
    path('', include('blog.urls', namespace='index')),
    path('admin/', admin.site.urls),
    path('article/', include('blog.urls', namespace='blog')),
    path('userprofile/', include('userprofile.urls', namespace='userprofile')),
    path('password-reset/', include('password_reset.urls')),
    path('comment/', include('comment.urls', namespace='comment')),


    path('inbox/notifications/', include('notifications.urls', namespace='notifications')),

    path('520/', include('valentine.urls', namespace='valentine')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

