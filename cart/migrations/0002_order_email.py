# Generated by Django 3.0.5 on 2020-07-09 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.EmailField(default=' default@gmail.com', max_length=100),
        ),
    ]
