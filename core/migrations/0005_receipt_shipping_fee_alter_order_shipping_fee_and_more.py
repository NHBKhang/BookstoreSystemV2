# Generated by Django 5.0.3 on 2024-03-28 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_transaction_order_orderdetails_receipt_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='shipping_fee',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_fee',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='order',
            name='tax_fee',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='tax_fee',
            field=models.IntegerField(default=0),
        ),
    ]