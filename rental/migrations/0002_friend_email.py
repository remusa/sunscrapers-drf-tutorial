# Generated by Django 3.0.3 on 2020-03-11 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='friend',
            name='email',
            field=models.EmailField(default='', max_length=254),
        ),
    ]