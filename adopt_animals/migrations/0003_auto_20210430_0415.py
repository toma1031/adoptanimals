# Generated by Django 2.2.17 on 2021-04-30 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adopt_animals', '0002_auto_20210428_0511'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='photo2',
            field=models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Photo2'),
        ),
        migrations.AddField(
            model_name='post',
            name='photo3',
            field=models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Photo3'),
        ),
        migrations.AddField(
            model_name='post',
            name='photo4',
            field=models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Photo4'),
        ),
        migrations.AddField(
            model_name='post',
            name='photo5',
            field=models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Photo5'),
        ),
        migrations.AlterField(
            model_name='post',
            name='photo',
            field=models.ImageField(upload_to='images/', verbose_name='Photo'),
        ),
    ]
