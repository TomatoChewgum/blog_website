from django.shortcuts import render, redirect
# 引入HttpResponse
from django.http import HttpResponse

from django.core.serializers import serialize

from .models import Valentinephoto
from .forms import ValentinephotoPostForm

def valentine_view(request):

   if request.method == 'GET':
        photo_list = Valentinephoto.objects.all()

        photo_dict = serialize('json', photo_list, fields=['name', 'photo', 'words'])
        return render(request, 'valentine/520.html', {
            'photo_dict': photo_dict
        })



def photo_upload(request):
    if request.method == 'POST':
        photo_form = ValentinephotoPostForm(request.POST, request.FILES)
        if photo_form.is_valid():
            photo_form.save()
            return redirect("valentine:upload")
        else:
            return HttpResponse("注册表单输入有误。请重新输入~")

    elif request.method == 'GET':
        photo_list = Valentinephoto.objects.all()
        return render(request, 'valentine/upload.html', {
            'photo_list': photo_list
        })