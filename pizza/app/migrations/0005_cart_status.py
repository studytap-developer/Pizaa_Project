# Generated by Django 4.1 on 2023-12-22 10:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0004_cart_coupon"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="status",
            field=models.CharField(
                choices=[
                    ("placed", "Order Placed"),
                    ("in_transit", "In Transit"),
                    ("delivered", "Delivered"),
                ],
                default="placed",
                max_length=20,
            ),
        ),
    ]