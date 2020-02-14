from django.urls import path


from .views import valentine_view,photo_upload

# 正在部署的应用的名称
app_name = 'valentine'

urlpatterns = [
    # path函数将url映射到视图
    path('', valentine_view, name='520'),
    path('upload/', photo_upload, name='upload'),
]