# Generated by Django 2.2.10 on 2020-05-13 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MealPlaner', '0005_auto_20200513_0652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dinner',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='lunch',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False),
        ),
    ]
