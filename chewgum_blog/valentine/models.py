from django.db import models

# Create your models here.

class Valentinephoto(models.Model):
    '''
    模型包含Title、文件、创建时间等
    '''
    name = models.CharField(max_length=100, blank=False, verbose_name='图片名称')
    photo = models.ImageField(upload_to='valentinephoto/%Y%m%d/')
    words = models.CharField(max_length=255, blank=False, verbose_name='介绍')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name