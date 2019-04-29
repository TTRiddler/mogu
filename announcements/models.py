import datetime

from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField
from services.models import Service


class City(models.Model):
    name = models.CharField(max_length=250, verbose_name='Город')

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['name']

    def __str__(self):
        return '%s' % self.name


class Announcement(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор', related_name='announcements')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Услуга', related_name='announcements')
    price = models.PositiveIntegerField(verbose_name='Цена')
    posted = models.DateTimeField(auto_now_add=True, verbose_name='Размещено')
    can_edit = models.DateTimeField(verbose_name='Возможно редактирование до', null=True)
    views = models.PositiveSmallIntegerField(verbose_name='Просмотры', default=0)
    views_today = models.PositiveSmallIntegerField(verbose_name='Просмотры сегодня', default=0)
    today = models.DateField(verbose_name='Сегодня', auto_now_add=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Город', related_name='announcements')
    address = models.CharField(max_length=250, verbose_name='Адресс')
    contact = models.CharField(max_length=250, verbose_name='Контактное лицо')
    phone = models.CharField(max_length=250, verbose_name='Телефон')
    desc = RichTextField(verbose_name='Описание')
    is_active = models.BooleanField(default=True, verbose_name='Активное')

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-posted']

    def get_main_image(self):
        return self.images.first()

    def save(self, *args, **kwargs):
        self.can_edit = self.posted + datetime.timedelta(days=1)
        super(Announcement, self).save(*args, **kwargs)

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