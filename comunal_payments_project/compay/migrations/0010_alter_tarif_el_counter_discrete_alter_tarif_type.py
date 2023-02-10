# Generated by Django 4.1.5 on 2023-02-06 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("compay", "0009_alter_counter_options_alter_item_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tarif",
            name="el_counter_discrete",
            field=models.CharField(
                choices=[
                    ("0-150", "(0...150)"),
                    ("150-450", "(150..450)"),
                    ("450+", "(450 и выше)"),
                    ("", ""),
                ],
                default="",
                max_length=12,
                verbose_name="Зависит от потребления",
            ),
        ),
        migrations.AlterField(
            model_name="tarif",
            name="type",
            field=models.CharField(
                choices=[
                    ("counter", "Счетчик"),
                    ("day", "День"),
                    ("night", "Ночь"),
                    ("tarif", "Тариф"),
                    ("discrete2", "Тариф2"),
                    ("discrete3", "Тариф3"),
                ],
                default="flat",
                max_length=15,
                verbose_name="Тип тарифа",
            ),
        ),
    ]
