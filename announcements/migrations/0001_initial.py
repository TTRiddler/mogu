# Generated by Django 2.2 on 2019-04-22 08:11

import announcements.models
import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Название')),
                ('price', models.PositiveIntegerField(verbose_name='Цена')),
                ('posted', models.DateTimeField(auto_now_add=True, verbose_name='Размещено')),
                ('views', models.PositiveSmallIntegerField(default=0, verbose_name='Просмотры')),
                ('address', models.CharField(max_length=250, verbose_name='Адресс')),
                ('contact', models.CharField(max_length=250, verbose_name='Контактное лицо')),
                ('phone', models.CharField(max_length=250, verbose_name='Телефон')),
                ('desc', ckeditor.fields.RichTextField(verbose_name='Описание')),
                ('is_active', models.BooleanField(default=True, verbose_name='Показывать на сайте')),
            ],
            options={
                'verbose_name': 'Объявление',
                'verbose_name_plural': 'Объявления',
                'ordering': ['posted'],
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=announcements.models.Image.get_picture_url, verbose_name='Изображение')),
                ('is_main', models.BooleanField(default=False, verbose_name='Главное изображение')),
                ('announcement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='announcements.Announcement', verbose_name='Объявление')),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Изображения',
            },
        ),
    ]