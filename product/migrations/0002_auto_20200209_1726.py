# Generated by Django 3.0 on 2020-02-09 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Category'),
        ),
    ]
