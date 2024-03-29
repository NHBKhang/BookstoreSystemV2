# Generated by Django 5.0.3 on 2024-03-29 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_receipt_shipping_fee_alter_order_shipping_fee_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shipping_fee',
            field=models.IntegerField(default=1000),
        ),
        migrations.AlterField(
            model_name='order',
            name='tax_fee',
            field=models.IntegerField(default=1000),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='shipping_fee',
            field=models.IntegerField(default=1000),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='tax_fee',
            field=models.IntegerField(default=1000),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_id',
            field=models.BigIntegerField(),
        ),
    ]
