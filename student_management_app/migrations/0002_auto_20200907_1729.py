# Generated by Django 3.0.4 on 2020-09-07 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='neetapply',
            name='grad_board',
            field=models.CharField(blank=True, default='None', max_length=255),
        ),
        migrations.AlterField(
            model_name='neetapply',
            name='grad_fullmark',
            field=models.CharField(blank=True, default='None', max_length=255),
        ),
        migrations.AlterField(
            model_name='neetapply',
            name='grad_passed',
            field=models.CharField(blank=True, default='None', max_length=255),
        ),
        migrations.AlterField(
            model_name='neetapply',
            name='grad_percent',
            field=models.CharField(blank=True, default='None', max_length=255),
        ),
        migrations.AlterField(
            model_name='neetapply',
            name='grad_school',
            field=models.CharField(blank=True, default='None', max_length=255),
        ),
        migrations.AlterField(
            model_name='neetapply',
            name='grad_securedmark',
            field=models.CharField(blank=True, default='None', max_length=255),
        ),
        migrations.AlterField(
            model_name='neetapply',
            name='grad_year',
            field=models.CharField(blank=True, default='None', max_length=255),
        ),
    ]
