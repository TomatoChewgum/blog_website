# 引入表单类
from django import forms
# 引入文章模型
from .models import Valentinephoto

# 写文章的表单类
class ValentinephotoPostForm(forms.ModelForm):

    class Meta:
        model = Valentinephoto
        fields = ('name', 'photo', 'words')


# class CategoryAddForm(forms.ModelForm):
#
#     class Meta:
#         # 指明数据模型来源
#         model = Category
#         # 定义表单包含的字段
#         fields = ('category',)

