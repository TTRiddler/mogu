from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from services.models import Service


class Announcement(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='announcements')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Услуга', related_name='announcements')
    price = models.PositiveIntegerField(verbose_name='Цена')
    posted = models.DateTimeField(auto_now_add=True, verbose_name='Размещено')
    views = models.PositiveSmallIntegerField(verbose_name='Просмотры', default=0)
    address = models.CharField(max_length=250, verbose_name='Адресс')
    contact = models.CharField(max_length=250, verbose_name='Контактное лицо')
    phone = models.CharField(max_length=250, verbose_name='Телефон')
    desc = RichTextField(verbose_name='Описание')
    is_active = models.BooleanField(default=True, verbose_name='Показывать на сайте')

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['posted']

    def __str__(self):
        return '%s - %s' % (self.name, self.author.username)


class Image(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, verbose_name='Объявление', related_name='images')

    def get_picture_url(self, filename):
        return 'images/announcements/%s/%s' % (self.announcement.author.username, filename)

    image = models.ImageField(upload_to=get_picture_url, verbose_name='Изображение')
    is_main = models.BooleanField(default=False, verbose_name='Главное изображение')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return "%s" % self.id