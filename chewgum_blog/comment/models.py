from django.db import models
from django.contrib.auth.models import User
from blog.models import ArticlePost
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
# 博文的评论

# 若要获取某一篇文章的所有评论
""" 方法一：
        django 默认每个主表的对象都有一个是外键的属性，可以通过它来查询到所有属于主表的子表的信息。
    这个属性的名称默认是以子表的名称小写加上_set()来表示，默认返回的是一个querydict对象，你可以继续的根据情况来查询等操作。
    
    article = ArticlePost.objects.get(id=1)
    article.comment_set.all() # 查询到所有属于主表的子表的信息
"""

""" 方法二：
    article = ArticlePost.objects.get(id=1)
    article.comments.all() # 设置 related_name = 'comments'
"""

# class Comment(models.Model):
#     article = models.ForeignKey(
#         ArticlePost,
#         on_delete=models.CASCADE,
#         related_name='comments'  # 在定义主表的外键的时候，给这个外键定义好一个名称 related_name
#     )
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='comments'
#     )
#     content = RichTextField(verbose_name='评论内容')
#     created = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         ordering = ('created',)
#
#     def __str__(self):
#         return self.content[:20]

class Comment(MPTTModel):
    article = models.ForeignKey(
        ArticlePost,
        on_delete=models.CASCADE,
        related_name='comments'  # 在定义主表的外键的时候，给这个外键定义好一个名称 related_name
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = RichTextField(verbose_name='评论内容')
    created = models.DateTimeField(auto_now_add=True)

    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    # 新增，记录二级评论回复给谁, str
    reply_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replyers'
    )

    class MPTTMeta:
        order_insertion_by = ['created']

    def __str__(self):
        return self.content[:20]