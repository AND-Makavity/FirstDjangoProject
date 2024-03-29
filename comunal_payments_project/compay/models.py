from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# from django.urls import reverse
# from datetime import datetime


class Appartment(models.Model):
    NAME = 'Объекты'
    CT = [('counter', 'Счетчик'), ('tarif', 'Тариф')]
    name = models.CharField(max_length=50, unique=True, blank=False, verbose_name="Название объекта")
    adress = models.CharField(max_length=100, blank=True, verbose_name="Адрес объекта")
    belong = models.ForeignKey(settings.AUTH_USER_MODEL, default='admin', on_delete=models.CASCADE, verbose_name="Принадлежит")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    electricity = models.BooleanField(default=False, verbose_name="Электричество")
    el_is_counter = models.CharField(choices=CT, max_length=50, default='tarif', blank=False, verbose_name="Расчет по")
    el_counter_discrete = models.BooleanField(default=False, verbose_name="Тариф зависит от потребления (Да/Нет)")
    el_night = models.BooleanField(default=False, verbose_name="Счетчик день-ночь (Да/Нет)")
    water = models.BooleanField(default=False, verbose_name="Вода")
    wat_is_counter = models.CharField(choices=CT, max_length=50, default='tarif', blank=False, verbose_name="Расчет по")
    gas = models.BooleanField(default=False, verbose_name="Газ")
    gas_is_counter = models.CharField(choices=CT, max_length=50, default='tarif', blank=False, verbose_name="Расчет по")
    kv = models.BooleanField(default=False, verbose_name="Квартплата")
    tbo = models.BooleanField(default=False, verbose_name="ТБО")
    domofon = models.BooleanField(default=False, verbose_name="Домофон")
    inet = models.BooleanField(default=False, verbose_name="Интернет")
    other = models.BooleanField(default=False, verbose_name="Другой платеж")

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'
        ordering = ['name']

    def __init__(self, *args, **kwargs):    # Новый блок кода! Инит с условием!
        super(Appartment, self).__init__(*args, **kwargs)
        if self.el_is_counter == 'tarif':
            self.el_night = False
            self.el_counter_discrete = False  # Конец нового блока кода! Инит с условием!

    def __str__(self):
        return self.name


class Item(models.Model):
    LST = [('electricity', 'Электричество'), ('water', 'Вода'), ('gas', 'Газ'), ('kv', 'Квартплата'),
           ('tbo', 'ТБО'), ('domofon', 'Домофон'), ('inet', 'Интернет'), ('other', 'Другой вид оплаты')]
    CT = [('counter', 'Счетчик'), ('tarif', 'Тариф'), ('day', 'Счетчик День'),
          ('night', 'Счетчик Ночь'), ('total', 'Итого')]

    item_name = models.CharField(choices=LST, max_length=50, blank=False, verbose_name="Предмет расчета")
    is_counter = models.CharField(choices=CT, max_length=50, default='tarif', blank=False, verbose_name="Расчет")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    active = models.BooleanField(default=True, verbose_name="Активный")
    app = models.ForeignKey('Appartment', on_delete=models.CASCADE, verbose_name="Объект")

    class Meta:
        verbose_name = 'Конфигурация объекта'
        verbose_name_plural = 'Конфигурации объектов'
        ordering = ['id']

    def __str__(self):
        for k, v in self.LST:
            if k == self.item_name:
                name = v
        return str(self.app) + ' - ' + name + " (" + str(self.get_is_counter_display()) + ')'


# type??? default=flat???
class Tarif(models.Model):
    NAME = 'Тариф '
    TYPE = [('counter', 'Счетчик'), ('day', 'День'), ('night', 'Ночь'), ('tarif', 'Тариф')]
    DISCR = [('0-150', '(0...150)'), ('150-600', '(150..600)'), ('600+', '(600 и выше)'), ('', '')]
    TARIF_UNITS = [('руб', 'руб'), ('руб/м3', 'руб/м3'), ('руб/кВт', 'руб/кВт'), ('руб/тыс.м3', 'руб/тыс.м3')]
    value = models.FloatField(verbose_name='Тариф ', help_text='')
    unit = models.CharField(choices=TARIF_UNITS, default='руб', max_length=15, blank=True, verbose_name="Ед.изм.")
    type = models.CharField(choices=TYPE, default='flat', max_length=15, blank=False, verbose_name="Тип тарифа")
    el_counter_discrete = models.CharField(choices=DISCR, default='', max_length=12,
                                           blank=False, verbose_name="Зависит от потребления")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    item = models.ForeignKey('Item', on_delete=models.CASCADE, verbose_name="Предмет расчета")

    def __init__(self, *args, **kwargs):
        super(Tarif, self).__init__(*args, **kwargs)
        if 'Вода' in str(self.item).split() and self.type in ['counter']:
            self.unit = 'руб/м3'
        elif 'Электричество' in str(self.item).split() and self.type in ['counter', 'day', 'night']:
            self.unit = 'руб/кВт'
        elif 'Газ' in str(self.item).split() and self.type in ['counter']:
            self.unit = 'руб/тыс.м3'
        else:
            self.unit = 'руб'

    def __str__(self):
        return self.NAME + ' ' + str(self.item)

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'
        ordering = ['-created']

    @classmethod
    def create(cls, type, item, value=0, from_value=0, to_value=1000000, el_counter_discrete=''):
        tarif = cls(type=type, item=item, value=value, el_counter_discrete=el_counter_discrete)
        return tarif


class Info(models.Model):
    LST = [('electricity', 'Электричество'), ('water', 'Вода'), ('gas', 'Газ'), ('kv', 'Квартплата'),
           ('tbo', 'ТБО'), ('domofon', 'Домофон'), ('inet', 'Интернет'), ('other', 'Другой вид оплаты')]

    item = models.ForeignKey('Item', on_delete=models.PROTECT, verbose_name="Предмет")
    item_provider = models.CharField(max_length=50, blank=True, verbose_name="Название организации")
    item_user_number = models.CharField(max_length=50, blank=True, verbose_name="Лицевой счет")
    item_comment = models.TextField(blank=True, verbose_name="Дополнительная информация")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    app = models.ForeignKey('Appartment', on_delete=models.PROTECT, verbose_name="Объект")


    def __str__(self):
        return str(self.item_provider) + ' ' + str(self.app)

    class Meta:
        verbose_name = 'Информация для расчетов'
        verbose_name_plural = 'Информация для расчетов'
        ordering = ['created']


class Counter(models.Model):
    NAME = 'Показания счетчика'
    LST = [('electricity', 'Электричество'), ('water', 'Вода'), ('gas', 'Газ')]
    TYPE = [('counter', 'Однотарифный'), ('day', 'День'), ('night', 'Ночь')]
    COUNTER_UNITS = [('ед.', 'ед.'), ('м3', 'м3'), ('тыс.м3', 'тыс.м3'), ('кВт', 'кВт')]

    type = models.CharField(choices=TYPE, default='flat', max_length=15, blank=False, verbose_name="Тип счетчика")
    value = models.PositiveIntegerField(blank=False, verbose_name='Показания')
    unit = models.CharField(choices=COUNTER_UNITS, default='ед.', max_length=15, blank=True, verbose_name="Ед.изм.")
    previous = models.PositiveIntegerField(blank=True, default=0, verbose_name='Предыдущие показания')
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата ввода показаний")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    item = models.ForeignKey('Item', on_delete=models.CASCADE, verbose_name="Предмет расчета")

    class Meta:
        verbose_name = 'Показания счетчика'
        verbose_name_plural = 'Показания счетчиков'
        ordering = ['-created']

    def __init__(self, *args, **kwargs):
        super(Counter, self).__init__(*args, **kwargs)
        if 'Вода' in str(self.item).split():
            self.unit = 'м3'
        elif 'Электричество' in str(self.item).split():
            self.unit = 'кВт'
        elif 'Газ' in str(self.item).split():
            self.unit = 'тыс.м3'
        if self.value < self.previous:
            self.value = self.previous

    def __str__(self):
        return str(self.item)

    @classmethod
    def create(cls, type, item, value=0, previous=0):
        counter = cls(type=type, item=item, value=value, previous=previous)
        return counter


MONTHES = [('1', 'Январь'), ('2', 'Февраль'), ('3', 'Март'),
           ('4', 'Апрель'), ('5', 'Май'), ('6', 'Июнь'),
           ('7', 'Июль'), ('8', 'Август'), ('9', 'Сентябрь'),
           ('10', 'Октябрь'), ('11', 'Ноябрь'), ('12', 'Декабрь'), ]


class Pay(models.Model):
    NAME = 'Расчет оплаты'
    PAY_UNITS = [('руб', 'руб')]

    topay = models.FloatField(default=0, verbose_name='К оплате')
    payed = models.FloatField(default=0, verbose_name='Оплачено')
    debt = models.FloatField(default=0, verbose_name='Долг')
    unit = models.CharField(choices=PAY_UNITS, default='руб', max_length=15, blank=True, verbose_name="Ед.изм.")
    month = models.CharField(max_length=2, choices=MONTHES, verbose_name='Месяц расчета')
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    calculation = models.CharField(max_length=250, blank=True, verbose_name='Расчёт')
    item = models.ForeignKey('Item', on_delete=models.CASCADE, verbose_name="Предмет расчета")

    class Meta:
        verbose_name = 'Расчетная сумма для оплаты'
        verbose_name_plural = 'Расчеты для оплаты'
        ordering = ['created']

    def __str__(self):
        return self.NAME + ' ' + str(self.item) + ' ' + str(self.get_month_display())


class PaySummary(models.Model):
    NAME = 'Суммарный расчет'
    PAY_UNITS = [('руб', 'руб')]

    topay = models.FloatField(default=0, verbose_name='К оплате')
    payed = models.FloatField(default=0, verbose_name='Оплачено')
    debt = models.FloatField(default=0, verbose_name='Долг по месяцу')
    debt_summary = models.FloatField(default=0, verbose_name='Долг итоговый')
    debt_sum_before = models.FloatField(default=0, verbose_name='Долг предыдущий')
    unit = models.CharField(choices=PAY_UNITS, default='руб', max_length=15, blank=True, verbose_name="Ед.изм.")
    month = models.CharField(max_length=2, choices=MONTHES, verbose_name='Месяц расчета')
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    comment = models.TextField(blank=True, verbose_name='Заметки')
    app = models.ForeignKey('Appartment', on_delete=models.CASCADE, verbose_name="Имя объекта")

    class Meta:
        verbose_name = 'Суммарный расчет'
        verbose_name_plural = 'Суммарный расчет'
        ordering = ['created']

    def __str__(self):
        return self.NAME + ' ' + str(self.app) + ' ' + str(self.get_month_display())