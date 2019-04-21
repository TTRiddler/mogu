from django.db import models


class ServiceType(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название')

    class Meta:
        verbose_name = 'Тип услуги'
        verbose_name_plural = 'Типы услуг'
        ordering = ['name']

    def __str__(self):
        return '%s' % self.name


class Service(models.Model):
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, verbose_name='Тип услуги', related_name='services')
    name = models.CharField(max_length=250, verbose_name='Название')

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['name']

    def __str__(self):
        return '%s' % self.name