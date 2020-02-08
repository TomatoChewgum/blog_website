from django.contrib import admin

# Register your models here.
from .models import ArticlePost,Tag,Category

# 注册ArticlePost到admin中
admin.site.register(ArticlePost)

admin.site.register(Tag)

admin.site.register(Category)