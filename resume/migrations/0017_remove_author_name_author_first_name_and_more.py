# Generated by Django 5.0.6 on 2024-07-05 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0016_rename_end_education_end_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='name',
        ),
        migrations.AddField(
            model_name='author',
            name='first_name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='author',
            name='last_name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
