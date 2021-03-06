# Generated by Django 3.0.7 on 2020-12-30 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_cart_category_productmodel_products'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productmodel',
            name='productCategory',
        ),
        migrations.AddField(
            model_name='products',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.CustomUser', verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='paymentDone',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='paymentMethod',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='productDescription',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='productName',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='productPrice',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='stars',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
