# Generated by Django 3.0.7 on 2021-01-08 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_customuser_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='ordered',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]