# 引入表单类
from django import forms
# 引入 User 模型
from django.contrib.auth.models import User

from .models import Profile

# 登录表单，继承了 forms.Form 类
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

# 注册用户表单
class UserRegisterForm(forms.ModelForm):

    password = forms.CharField()  # 覆写了password字段 # 复写 User 的密码
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email')

    # 对两次输入的密码是否一致进行检查
    def clean_password2(self):  # def clean_[字段]这种写法Django会自动调用，来对单个字段的数据进行验证清洗
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError("密码输入不一致,请重试。")

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'icon', 'bio')

