# Generated by Django 3.0.7 on 2020-12-30 16:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20201230_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='productmodel',
            name='productCategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Category'),
        ),
    ]