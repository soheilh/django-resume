# Generated by Django 5.0.6 on 2024-07-01 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0004_author_linktype_remove_publication_publication_link_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
            ],
        ),
    ]
