# Generated by Django 4.2.20 on 2025-03-29 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0005_listener'),
    ]

    operations = [
        migrations.AddField(
            model_name='listener',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
