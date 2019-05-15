from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from announcements.models import Announcement


class StarColor(models.Model):
    name = models.CharField(unique=True, max_length=250, verbose_name='Цвет')
    color = models.CharField(max_length=250, verbose_name='Код цвета', default='#ffffff')

    class Meta:
        verbose_name = 'Цвет звезды'
        verbose_name_plural = 'Цвета звезд'
    
    def __str__(self):
        return '%s' % self.name


class User(AbstractUser):
    patronymic = models.CharField(max_length=250, blank=True, null=True, verbose_name='Отчество')
    phone = models.CharField(null=True, blank=True, unique=True, max_length=250, verbose_name='Телефон')
    is_verified = models.BooleanField(default=False, verbose_name='Пользователь подтвержден')
    star_color = models.ForeignKey(StarColor, on_delete=models.CASCADE, verbose_name='Цвет звезды', default=4, null=True, blank=True, related_name='users')
    thanks = models.PositiveIntegerField(default=0, verbose_name='Благодарности', blank=True, null=True)
    complaints = models.PositiveIntegerField(default=0, verbose_name='Жалобы', blank=True, null=True)
    claims = models.PositiveIntegerField(default=0, verbose_name='Претензии', blank=True, null=True)

    def get_picture_url(self, filename):
        ext = filename.split('.')[-1]
        filename = '%s.%s' % (self.id, ext)
        return 'images/profiles/%s' % filename
    
    photo = models.ImageField(null=True, blank=True, upload_to=get_picture_url, verbose_name='Фото')

    def save(self, *args, **kwargs):
        if self.is_verified and self.star_color == StarColor.objects.get(id=4):
            self.star_color = StarColor.objects.get(id=1)
        super(User, self).save(*args, **kwargs)


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
    
    def delete(self):
        self.about.save()
        super(Message, self).delete()
    
    def __str__(self):
        return '%s %s для %s %s' % (self.author.last_name, self.author.first_name, self.about.last_name, self.about.first_name)


@receiver(post_save, sender=Message)
def update_messages_save(sender, instance, **kwargs):
    thanks_type = MessageType.objects.get(name__icontains='Благодарность')
    complaints_type = MessageType.objects.get(name__icontains='Жалоба')
    claims_type = MessageType.objects.get(name__icontains='Претензия')

    thanks = Message.objects.filter(is_active=True, about=instance.about, message_type=thanks_type)
    complaints = Message.objects.filter(is_active=True, about=instance.about, message_type=complaints_type)
    claims = Message.objects.filter(is_active=True, about=instance.about, message_type=claims_type)

    instance.about.thanks = len(thanks)
    instance.about.complaints = len(complaints)
    instance.about.claims = len(claims)
    
    if instance.about.is_verified:
        instance.about.star_color = StarColor.objects.get(id=1)
    else:
        instance.about.star_color = StarColor.objects.get(id=4)
    if len(complaints) >= 3:
        instance.about.star_color = StarColor.objects.get(id=2)
    if len(claims) >= 1:
        instance.about.star_color = StarColor.objects.get(id=3)
    
    instance.about.save()


@receiver(post_delete, sender=Message)
def update_messages_delete(sender, instance, **kwargs):
    thanks_type = MessageType.objects.get(name__icontains='Благодарность')
    complaints_type = MessageType.objects.get(name__icontains='Жалоба')
    claims_type = MessageType.objects.get(name__icontains='Претензия')

    thanks = Message.objects.filter(is_active=True, about=instance.about, message_type=thanks_type)
    complaints = Message.objects.filter(is_active=True, about=instance.about, message_type=complaints_type)
    claims = Message.objects.filter(is_active=True, about=instance.about, message_type=claims_type)

    instance.about.thanks = len(thanks)
    instance.about.complaints = len(complaints)
    instance.about.claims = len(claims)

    if instance.about.is_verified:
        instance.about.star_color = StarColor.objects.get(id=1)
    else:
        instance.about.star_color = StarColor.objects.get(id=4)
    if len(complaints) >= 3:
        instance.about.star_color = StarColor.objects.get(id=2)
    if len(claims) >= 1:
        instance.about.star_color = StarColor.objects.get(id=3)

    instance.about.save()


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