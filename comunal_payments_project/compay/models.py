from django.db import models
# from django.urls import reverse
# from datetime import datetime


class Appartment(models.Model):
    NAME = 'Объекты'
    name = models.CharField(max_length=50, unique=True , blank=False, verbose_name="Название объекта")
    adress = models.CharField(max_length=100, blank=True, verbose_name="Адрес объекта")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    electricity = models.BooleanField(default=False, verbose_name="Электричество")
    water = models.BooleanField(default=False, verbose_name="Вода")
    gas = models.BooleanField(default=False, verbose_name="Газ")
    kv = models.BooleanField(default=False, verbose_name="Квартплата")
    tbo = models.BooleanField(default=False, verbose_name="ТБО")
    domofon = models.BooleanField(default=False, verbose_name="Домофон")
    inet = models.BooleanField(default=False, verbose_name="Интернет")
    other = models.BooleanField(default=False, verbose_name="Другой платеж")

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Обьекты'
        ordering = ['name']

    def __str__(self):
        return self.name


class Item(models.Model):
    LST = [('electricity', 'Электричество'), ('water', 'Вода'), ('gas', 'Газ'), ('kv', 'Квартплата'),
           ('tbo', 'ТБО'), ('domofon', 'Домофон'), ('inet', 'Интернет'), ('other', 'Другой вид оплаты')]
    CT = [('counter', 'Счетчик'), ('tarif', 'Тариф')]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_counter == 'tarif':
            self.day_night = False
            self.discrete_tarif = False

    item_name = models.CharField(choices=LST, max_length=50, blank=False, verbose_name="Предмет расчета")
    is_counter = models.CharField(choices=CT, max_length=50, default='tarif', blank=False, verbose_name="Расчет по")
    day_night = models.BooleanField(default=False, verbose_name="Счетчик день-ночь (Да/Нет)")
    discrete_tarif = models.BooleanField(default=False, verbose_name="Тариф зависит от потребления (Да/Нет)")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    app = models.ForeignKey('Appartment', on_delete=models.CASCADE, verbose_name="Объект")

    class Meta:
        verbose_name = 'Конфигурация для расчета'
        verbose_name_plural = 'Конфигурации для расчета'
        ordering = ['item_name']

    def __str__(self):
        for k, v in self.LST:
            if k == self.item_name:
                name = v
        return str(self.app) + ' - ' + name


class Tarif(models.Model):
    NAME = 'Тариф '
    TYPE = [('flat', 'Однотарифный'), ('day', 'День'), ('night', 'Ночь'), ('discrete1', 'Тариф1'),
            ('discrete2', 'Тариф2'), ('discrete3', 'Тариф3')]

    value = models.FloatField(verbose_name='Значение')
    type = models.CharField(choices=TYPE, default='flat', max_length=15, blank=False, verbose_name="Тип тарифа")
    active = models.BooleanField(default=True, verbose_name="Действующий тариф")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    item = models.ForeignKey('Item', on_delete=models.CASCADE, verbose_name="Предмет расчета")

    def __str__(self):
        return self.NAME + ' ' + str(self.item) + ' ' + str(self.type)

    class Meta:
        verbose_name = 'Тариф для расчета'
        verbose_name_plural = 'Тарифы для расчета'
        ordering = ['active']


class DiscreteConfiguration(models.Model):
    NAME = 'Конфигурация дискретного тарифа '
    frm = models.PositiveSmallIntegerField(verbose_name='От')
    to = models.PositiveSmallIntegerField(verbose_name='До')
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    tarif = models.ForeignKey('Tarif', on_delete=models.CASCADE, verbose_name="Тариф")

    def __str__(self):
        return self.NAME + ' ' + str(self.tarif)

    class Meta:
        verbose_name = 'Дискретный тариф для расчета'
        verbose_name_plural = 'Дискретные тарифы для расчета'
        ordering = ['created']


class Info(models.Model):
    item_provider = models.CharField(max_length=50, blank=False, verbose_name="Название организации")
    item_user_number = models.CharField(max_length=50, blank=True, verbose_name="Лицевой счет")
    item_comment = models.TextField(blank=True, verbose_name="Дополнительная информация")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    app = models.ForeignKey('Appartment', on_delete=models.PROTECT, verbose_name="Объект")
    item = models.ForeignKey('Item', on_delete=models.CASCADE, verbose_name="Предмет расчета")

    def __str__(self):
        return str(self.item_provider) + ' ' + str(self.app)

    class Meta:
        verbose_name = 'Информация для расчетов'
        verbose_name_plural = 'Информация для расчетов'
        ordering = ['created']


class Counter(models.Model):
    NAME = 'Показания счетчика'
    LST = [('electricity', 'Электричество'), ('water', 'Вода'), ('gas', 'Газ')]
    TYPE = [('flat', 'Однотарифный'), ('day', 'День'), ('night', 'Ночь')]

    type = models.CharField(choices=TYPE, default='flat', max_length=15, blank=False, verbose_name="Тип счетчика")
    value = models.PositiveIntegerField(blank=False, verbose_name='Показания')
    previous = models.PositiveIntegerField(blank=True, default=0, verbose_name='Предыдущие показания')
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата ввода показаний")
    item = models.ForeignKey('Item', on_delete=models.CASCADE, verbose_name="Предмет расчета")

    class Meta:
        verbose_name = 'Показания счетчика'
        verbose_name_plural = 'Показания счетчиков'
        ordering = ['created']

    def __str__(self):
        # for k, v in self.TYPE:
        #     if k == self.type:
        #         type_str = v
        return str(self.item) + ' ' + str(self.get_type_display())

    @classmethod
    def create(cls, type, value, item):
        counter = cls(type=type, item=item, value=0)
        return counter



MONTHES = [('1', 'Январь'), ('2', 'Февраль'), ('3', 'Март'),
           ('4', 'Апрель'), ('5', 'Май'), ('6', 'Июнь'),
           ('7', 'Июль'), ('8', 'Август'), ('9', 'Сентябрь'),
           ('10', 'Октябрь'), ('11', 'Ноябрь'), ('12', 'Декабрь'), ]


class ToPay(models.Model):
    NAME = 'Расчет для оплаты'

    value = models.FloatField(verbose_name=NAME)
    month = models.CharField(max_length=2, choices=MONTHES, verbose_name='Месяц расчета')
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    item = models.ForeignKey('Item', on_delete=models.CASCADE, verbose_name="Предмет расчета")

    class Meta:
        verbose_name = 'Расчетная сумма для оплаты'
        verbose_name_plural = 'Расчеты для оплаты'
        ordering = ['created']

    def __str__(self):
        return self.NAME + ' ' + str(self.item) + ' ' + str(self.month)


class Payed(models.Model):
    NAME = 'Оплачено'

    value = models.FloatField(verbose_name=NAME)
    month = models.CharField(max_length=2, choices=MONTHES, verbose_name='Месяц расчета')
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    item = models.ForeignKey('Item', on_delete=models.CASCADE, verbose_name="Предмет расчета")

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'
        ordering = ['created']

    def __str__(self):
        return self.NAME + ' ' + str(self.item) + ' ' + str(self.month)


class Debts(models.Model):
    NAME = 'Долг'

    value = models.FloatField(verbose_name=NAME)
    month = models.CharField(max_length=2, choices=MONTHES, verbose_name='Месяц расчета')
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    item = models.ForeignKey('Item', on_delete=models.CASCADE, verbose_name="Предмет расчета")

    class Meta:
        verbose_name = 'Долг'
        verbose_name_plural = 'Долги'
        ordering = ['created']

    def __str__(self):
        return self.NAME + ' ' + str(self.item) + ' ' + str(self.month)
