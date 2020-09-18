# Generated by Django 3.0.4 on 2020-09-11 05:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0010_delete_otp'),
    ]

    operations = [
        migrations.CreateModel(
            name='Otp',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('otp_code', models.IntegerField()),
                ('student_id', models.CharField(max_length=6)),
                ('top_create', models.DateField(verbose_name=datetime.datetime(2020, 9, 11, 10, 52, 36, 557634))),
                ('is_expier', models.BooleanField(default=False)),
            ],
        ),
    ]