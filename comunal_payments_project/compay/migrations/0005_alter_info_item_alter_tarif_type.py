# Generated by Django 4.1.5 on 2023-03-31 19:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("compay", "0004_counter_unit_pay_unit_paysummary_unit_tarif_unit"),
    ]

    operations = [
        migrations.AlterField(
            model_name="info",
            name="item",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="compay.item",
                verbose_name="Предмет",
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
                ],
                default="flat",
                max_length=15,
                verbose_name="Тип тарифа",
            ),
        ),
    ]
