from django.db import models
from django.contrib.auth.models import AbstractUser
from announcements.models import Announcement


class User(AbstractUser):
    patronymic = models.CharField(max_length=250, blank=True, null=True, verbose_name='Отчество')
    phone = models.CharField(null=True, blank=True, unique=True, max_length=250, verbose_name='Телефон')

    def get_picture_url(self, filename):
        ext = filename.split('.')[-1]
        filename = '%s.%s' % (self.id, ext)
        return 'images/profiles/%s' % filename

    photo = models.ImageField(null=True, blank=True, upload_to=get_picture_url, verbose_name='Фото')


class FavoriteAn(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, verbose_name='Объявление', related_name='favorites')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='favorites')

    class Meta:
        verbose_name = 'Связь'
        verbose_name_plural = 'Список избранных'
    
    def __str__(self):
        return '%s - %s %s' % (self.announcement.name, self.user.last_name, self.user.first_name)