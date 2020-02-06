# Generated by Django 3.0.3 on 2020-02-06 09:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramuser',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='telegramuser',
            name='full_name',
            field=models.CharField(default='', max_length=255, verbose_name='Name'),
        ),
        migrations.AddField(
            model_name='telegramuser',
            name='language',
            field=models.CharField(default='ru', max_length=5, verbose_name='Язык'),
        ),
    ]
