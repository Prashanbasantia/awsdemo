# Generated by Django 3.0.4 on 2020-09-07 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0004_auto_20200907_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentresult',
            name='prac_secured_mark',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='studentresult',
            name='prac_total_mark',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]