# Generated by Django 2.2.10 on 2020-05-13 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MealPlaner', '0006_auto_20200513_0655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False),
        ),
    ]