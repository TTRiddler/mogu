from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    patronymic = models.CharField(max_length=250, blank=True, null=True, verbose_name='Отчество')
    phone = models.CharField(null=True, blank=True, unique=True, max_length=250, verbose_name='Телефон')

    def get_picture_url(self, filename):
        ext = filename.split('.')[-1]
        filename = '%s.%s' % (self.id, ext)
        return 'images/profiles/%s' % filename

    photo = models.ImageField(null=True, blank=True, upload_to=get_picture_url, verbose_name='Фото')