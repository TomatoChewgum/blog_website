# 引入表单类
from django import forms
# 引入文章模型
from .models import ArticlePost, Category

# 写文章的表单类
class ArticlePostForm(forms.ModelForm):

    title = forms.CharField()  # 覆写了password字段 # 复写 User 的密码

    content = forms.Textarea()
    # category = forms.ChoiceField(
    #        # choices=Category.objects.values_list('id', 'name')
    #         widget = forms.RadioSelect()
    #     )
    # project = forms.ChoiceField(choices=Project.objects.filter(prj_mgr='').value_list('id', 'name'))
    # 使用上述代码会报can't assign must be a instance，所以要使用下行代码

    category = forms.ModelChoiceField( widget = forms.RadioSelect(),
                                       queryset=Category.objects.all())
    # tag = forms.CharField()
    def __init__(self, *args, **kwargs):
        super(ArticlePostForm, self).__init__(*args, **kwargs)
        self.fields['category'].choices = Category.objects.values_list('id', 'name')
    class Meta:
        model = ArticlePost  # 指明数据模型来源
        fields = ('title', 'category', 'content',)  # 定义表单包含的字段



# class CategoryAddForm(forms.ModelForm):
#
#     class Meta:
#         # 指明数据模型来源
#         model = Category
#         # 定义表单包含的字段
#         fields = ('category',)

