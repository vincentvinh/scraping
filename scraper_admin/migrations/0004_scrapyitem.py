# Generated by Django 3.0.7 on 2020-07-01 04:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_admin', '0003_auto_20200629_1144'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScrapyItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.CharField(max_length=100, null=True)),
                ('data', models.TextField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
