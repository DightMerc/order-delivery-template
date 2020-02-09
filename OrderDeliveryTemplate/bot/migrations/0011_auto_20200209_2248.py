# Generated by Django 2.2.3 on 2020-02-09 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0010_auto_20200208_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Номер телефона'),
        ),
        migrations.AlterField(
            model_name='order',
            name='time',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Время'),
        ),
    ]
