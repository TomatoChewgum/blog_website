from django.urls import path

from userprofile.views import user_login, user_logout, user_register, user_delete, profile_edit
# 正在部署的应用的名称
app_name = 'userprofile'

urlpatterns = [
    # path函数将url映射到视图
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', user_register, name='register'),
    path('delete/<int:user_id>/', user_delete, name='delete'),
    path('edit/<int:user_id>/', profile_edit, name='edit'),
]