
from django.db import models
from django.contrib.auth.models import User
# timezone 用于处理时间相关事务。
from django.utils import timezone
from django.urls import reverse

class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=50, verbose_name="名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS,verbose_name="状态")
    is_nav = models.BooleanField(default=False, verbose_name="是否为导航")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = "分类"

    @classmethod
    def get_navs(cls):
        # categories = cls.objects.filter(status=cls.STATUS_NORMAL)
        # nav_categories = categories.filter(is_nav=True)
        # normal_categories = categories.filter(is_nav=False)
        # return{
        #     'navs': nav_categories,
        #     'categories':normal_categories,
        # }
        """ 重构上面的代码 因为上面生成了两个 QuerySet 对象，后续调用会产生两次I/O操作（查询数据库）"""
        categories = cls.objects.filter(status=cls.STATUS_NORMAL)
        nav_categories = []
        normal_categories = []
        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_categories.append(cate)  # 非导航分类
        return {
            'navs': nav_categories,
            'categories': normal_categories,
        }

class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=10, verbose_name="名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS, verbose_name="状态")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = "标签"
        ordering = ['-id']

class ArticlePost(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    title = models.CharField(max_length=100, verbose_name="标题")
    # 文章创建时间。参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    created = models.DateTimeField(default=timezone.now, verbose_name="创建时间")
    # 文章更新时间。参数 auto_now=True 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True)

    content = models.TextField(verbose_name="正文",help_text="正文必须为Markdown格式")
    # 用于存储将 Markdown文本转为 可以直接显示的html文本
    content_html = models.TextField(verbose_name="正文html代码",blank=True,editable=False)

    is_md = models.BooleanField(default=False, verbose_name="markdown语法")

    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS, verbose_name="状态")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="分类")
    tag = models.ManyToManyField(Tag,blank=True,verbose_name="标签")



    pv = models.PositiveIntegerField(default=0)     # 浏览量
    uv = models.PositiveIntegerField(default=0)     # 访客数


    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表明数据应该以倒序排列
        verbose_name = verbose_name_plural = "文章"
        ordering = ('-created',)

    # 函数 __str__ 定义当调用对象的 str() 方法时的返回值内容
    def __str__(self):
        # return self.title 将文章标题返回
        return self.title

    @classmethod
    # def latest_posts(cls):
    #     queryset = cls.objects.filter(status=cls.STATUS_NORMAL)
    #     return queryset
    def latest_posts(cls, with_related=True):
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL)
        # if with_related:
        #     queryset = queryset.select_related('owner', 'category')
        return queryset

        # 获取文章地址

    def get_absolute_url(self):
        return reverse('blog:article-detail', args=[self.id])