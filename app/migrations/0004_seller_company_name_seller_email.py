# Generated by Django 4.0.5 on 2023-08-23 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_seller'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='company_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='seller',
            name='email',
            field=models.EmailField(default=' ', max_length=254),
            preserve_default=False,
        ),
    ]