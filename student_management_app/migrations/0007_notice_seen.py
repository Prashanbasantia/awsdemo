# Generated by Django 3.0.4 on 2020-09-09 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0006_auto_20200907_2037'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='seen',
            field=models.BooleanField(default=False),
        ),
    ]
