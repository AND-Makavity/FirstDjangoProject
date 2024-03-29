# Generated by Django 4.1.5 on 2023-04-20 13:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Appartment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=50, unique=True, verbose_name="Название объекта"
                    ),
                ),
                (
                    "adress",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="Адрес объекта"
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "electricity",
                    models.BooleanField(default=False, verbose_name="Электричество"),
                ),
                (
                    "el_is_counter",
                    models.CharField(
                        choices=[("counter", "Счетчик"), ("tarif", "Тариф")],
                        default="tarif",
                        max_length=50,
                        verbose_name="Расчет по",
                    ),
                ),
                (
                    "el_counter_discrete",
                    models.BooleanField(
                        default=False,
                        verbose_name="Тариф зависит от потребления (Да/Нет)",
                    ),
                ),
                (
                    "el_night",
                    models.BooleanField(
                        default=False, verbose_name="Счетчик день-ночь (Да/Нет)"
                    ),
                ),
                ("water", models.BooleanField(default=False, verbose_name="Вода")),
                (
                    "wat_is_counter",
                    models.CharField(
                        choices=[("counter", "Счетчик"), ("tarif", "Тариф")],
                        default="tarif",
                        max_length=50,
                        verbose_name="Расчет по",
                    ),
                ),
                ("gas", models.BooleanField(default=False, verbose_name="Газ")),
                (
                    "gas_is_counter",
                    models.CharField(
                        choices=[("counter", "Счетчик"), ("tarif", "Тариф")],
                        default="tarif",
                        max_length=50,
                        verbose_name="Расчет по",
                    ),
                ),
                ("kv", models.BooleanField(default=False, verbose_name="Квартплата")),
                ("tbo", models.BooleanField(default=False, verbose_name="ТБО")),
                ("domofon", models.BooleanField(default=False, verbose_name="Домофон")),
                ("inet", models.BooleanField(default=False, verbose_name="Интернет")),
                (
                    "other",
                    models.BooleanField(default=False, verbose_name="Другой платеж"),
                ),
                (
                    "belong",
                    models.ForeignKey(
                        default="admin",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Принадлежит",
                    ),
                ),
            ],
            options={
                "verbose_name": "Объект",
                "verbose_name_plural": "Объекты",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "item_name",
                    models.CharField(
                        choices=[
                            ("electricity", "Электричество"),
                            ("water", "Вода"),
                            ("gas", "Газ"),
                            ("kv", "Квартплата"),
                            ("tbo", "ТБО"),
                            ("domofon", "Домофон"),
                            ("inet", "Интернет"),
                            ("other", "Другой вид оплаты"),
                        ],
                        max_length=50,
                        verbose_name="Предмет расчета",
                    ),
                ),
                (
                    "is_counter",
                    models.CharField(
                        choices=[
                            ("counter", "Счетчик"),
                            ("tarif", "Тариф"),
                            ("day", "Счетчик День"),
                            ("night", "Счетчик Ночь"),
                            ("total", "Итого"),
                        ],
                        default="tarif",
                        max_length=50,
                        verbose_name="Расчет",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                ("active", models.BooleanField(default=True, verbose_name="Активный")),
                (
                    "app",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="compay.appartment",
                        verbose_name="Объект",
                    ),
                ),
            ],
            options={
                "verbose_name": "Конфигурация объекта",
                "verbose_name_plural": "Конфигурации объектов",
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="Tarif",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", models.FloatField(verbose_name="Тариф ")),
                (
                    "unit",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("руб", "руб"),
                            ("руб/м3", "руб/м3"),
                            ("руб/кВт", "руб/кВт"),
                            ("руб/тыс.м3", "руб/тыс.м3"),
                        ],
                        default="руб",
                        max_length=15,
                        verbose_name="Ед.изм.",
                    ),
                ),
                (
                    "type",
                    models.CharField(
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
                (
                    "el_counter_discrete",
                    models.CharField(
                        choices=[
                            ("0-150", "(0...150)"),
                            ("150-600", "(150..600)"),
                            ("600+", "(600 и выше)"),
                            ("", ""),
                        ],
                        default="",
                        max_length=12,
                        verbose_name="Зависит от потребления",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="compay.item",
                        verbose_name="Предмет расчета",
                    ),
                ),
            ],
            options={
                "verbose_name": "Тариф",
                "verbose_name_plural": "Тарифы",
                "ordering": ["-created"],
            },
        ),
        migrations.CreateModel(
            name="PaySummary",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("topay", models.FloatField(default=0, verbose_name="К оплате")),
                ("payed", models.FloatField(default=0, verbose_name="Оплачено")),
                ("debt", models.FloatField(default=0, verbose_name="Долг по месяцу")),
                (
                    "debt_summary",
                    models.FloatField(default=0, verbose_name="Долг итоговый"),
                ),
                (
                    "debt_sum_before",
                    models.FloatField(default=0, verbose_name="Долг предыдущий"),
                ),
                (
                    "unit",
                    models.CharField(
                        blank=True,
                        choices=[("руб", "руб")],
                        default="руб",
                        max_length=15,
                        verbose_name="Ед.изм.",
                    ),
                ),
                (
                    "month",
                    models.CharField(
                        choices=[
                            ("1", "Январь"),
                            ("2", "Февраль"),
                            ("3", "Март"),
                            ("4", "Апрель"),
                            ("5", "Май"),
                            ("6", "Июнь"),
                            ("7", "Июль"),
                            ("8", "Август"),
                            ("9", "Сентябрь"),
                            ("10", "Октябрь"),
                            ("11", "Ноябрь"),
                            ("12", "Декабрь"),
                        ],
                        max_length=2,
                        verbose_name="Месяц расчета",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "updated",
                    models.DateTimeField(auto_now=True, verbose_name="Дата изменения"),
                ),
                ("comment", models.TextField(blank=True, verbose_name="Заметки")),
                (
                    "app",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="compay.appartment",
                        verbose_name="Имя объекта",
                    ),
                ),
            ],
            options={
                "verbose_name": "Суммарный расчет",
                "verbose_name_plural": "Суммарный расчет",
                "ordering": ["created"],
            },
        ),
        migrations.CreateModel(
            name="Pay",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("topay", models.FloatField(default=0, verbose_name="К оплате")),
                ("payed", models.FloatField(default=0, verbose_name="Оплачено")),
                ("debt", models.FloatField(default=0, verbose_name="Долг")),
                (
                    "unit",
                    models.CharField(
                        blank=True,
                        choices=[("руб", "руб")],
                        default="руб",
                        max_length=15,
                        verbose_name="Ед.изм.",
                    ),
                ),
                (
                    "month",
                    models.CharField(
                        choices=[
                            ("1", "Январь"),
                            ("2", "Февраль"),
                            ("3", "Март"),
                            ("4", "Апрель"),
                            ("5", "Май"),
                            ("6", "Июнь"),
                            ("7", "Июль"),
                            ("8", "Август"),
                            ("9", "Сентябрь"),
                            ("10", "Октябрь"),
                            ("11", "Ноябрь"),
                            ("12", "Декабрь"),
                        ],
                        max_length=2,
                        verbose_name="Месяц расчета",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "updated",
                    models.DateTimeField(auto_now=True, verbose_name="Дата изменения"),
                ),
                (
                    "calculation",
                    models.CharField(blank=True, max_length=250, verbose_name="Расчёт"),
                ),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="compay.item",
                        verbose_name="Предмет расчета",
                    ),
                ),
            ],
            options={
                "verbose_name": "Расчетная сумма для оплаты",
                "verbose_name_plural": "Расчеты для оплаты",
                "ordering": ["created"],
            },
        ),
        migrations.CreateModel(
            name="Info",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "item_provider",
                    models.CharField(
                        blank=True, max_length=50, verbose_name="Название организации"
                    ),
                ),
                (
                    "item_user_number",
                    models.CharField(
                        blank=True, max_length=50, verbose_name="Лицевой счет"
                    ),
                ),
                (
                    "item_comment",
                    models.TextField(
                        blank=True, verbose_name="Дополнительная информация"
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "app",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="compay.appartment",
                        verbose_name="Объект",
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="compay.item",
                        verbose_name="Предмет",
                    ),
                ),
            ],
            options={
                "verbose_name": "Информация для расчетов",
                "verbose_name_plural": "Информация для расчетов",
                "ordering": ["created"],
            },
        ),
        migrations.CreateModel(
            name="Counter",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("counter", "Однотарифный"),
                            ("day", "День"),
                            ("night", "Ночь"),
                        ],
                        default="flat",
                        max_length=15,
                        verbose_name="Тип счетчика",
                    ),
                ),
                ("value", models.PositiveIntegerField(verbose_name="Показания")),
                (
                    "unit",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("ед.", "ед."),
                            ("м3", "м3"),
                            ("тыс.м3", "тыс.м3"),
                            ("кВт", "кВт"),
                        ],
                        default="ед.",
                        max_length=15,
                        verbose_name="Ед.изм.",
                    ),
                ),
                (
                    "previous",
                    models.PositiveIntegerField(
                        blank=True, default=0, verbose_name="Предыдущие показания"
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата ввода показаний"
                    ),
                ),
                (
                    "updated",
                    models.DateTimeField(auto_now=True, verbose_name="Дата изменения"),
                ),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="compay.item",
                        verbose_name="Предмет расчета",
                    ),
                ),
            ],
            options={
                "verbose_name": "Показания счетчика",
                "verbose_name_plural": "Показания счетчиков",
                "ordering": ["-created"],
            },
        ),
    ]
