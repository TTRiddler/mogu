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


class MessageType(models.Model):
    name = models.CharField(unique=True, max_length=250, verbose_name='Название')

    class Meta:
        verbose_name = 'Тип сообщения'
        verbose_name_plural = 'Типы сообщений'
    
    def __str__(self):
        return '%s' % self.name


class Message(models.Model):
    message_type = models.ForeignKey(MessageType, on_delete=models.CASCADE, verbose_name='Тип сообщения', related_name='messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='author_messages')
    about = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='О ком', related_name='about_messages')
    text = models.TextField(verbose_name='Текст')
    is_active = models.BooleanField(default=False, verbose_name='Прошло модерацию')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
    
    def __str__(self):
        return '%s %s для %s %s' % (self.author.last_name, self.author.first_name, self.about.last_name, self.about.first_name)


class MessageImage(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение', related_name='images')

    def get_picture_url(self, filename):
        return 'images/messages/%s/%s' % (self.message.author.username, filename)

    image = models.ImageField(upload_to=get_picture_url, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return "%s" % self.id