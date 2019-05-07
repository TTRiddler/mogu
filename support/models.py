from django.db import models


class SupportMessage(models.Model):
    name = models.CharField(max_length=250, verbose_name='Имя пользователя')
    email = models.EmailField(max_length=250, verbose_name='Почта')
    message = models.TextField(verbose_name='Сообщение')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'
    
    def __str__(self):
        return '%s - %s' % (self.name, self.email)