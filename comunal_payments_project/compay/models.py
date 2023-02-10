from django.db import models
# from django.urls import reverse
# from datetime import datetime


class Appartment(models.Model):
    NAME = 'Объекты'
    CT = [('counter', 'Счетчик'), ('tarif', 'Тариф')]
    name = models.CharField(max_length=50, unique=True, blank=False, verbose_name="Название объекта")
    adress = models.CharField(max_length=100, blank=True, verbose_name="Адрес объекта")
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
        verbose_name_plural = 'Обьекты'
        ordering = ['name']

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
    app = models.ForeignKey('Appartment', on_delete=models.CASCADE, verbose_name="Объект")

    class Meta:
        verbose_name = 'Конфигурация для расчета'
        verbose_name_plural = 'Конфигурации для расчета'
        ordering = ['id']

    def __str__(self):
        for k, v in self.LST:
            if k == self.item_name:
                name = v
        return str(self.app) + ' - ' + name + " (" + str(self.get_is_counter_display()) + ')'


class Tarif(models.Model):
    NAME = 'Тариф '
    TYPE = [('counter', 'Счетчик'), ('day', 'День'), ('night', 'Ночь'), ('tarif', 'Тариф'),
            ('discrete2', 'Тариф2'), ('discrete3', 'Тариф3')]
    DISCR = [('0-150', '(0...150)'), ('150-450', '(150..450)'), ('450+', '(450 и выше)'), ('', '')]

    value = models.FloatField(verbose_name='Тариф ', help_text='')
    type = models.CharField(choices=TYPE, default='flat', max_length=15, blank=False, verbose_name="Тип тарифа")
    el_counter_discrete = models.CharField(choices=DISCR, default='', max_length=12,
                                           blank=False, verbose_name="Зависит от потребления")
    from_value = models.PositiveSmallIntegerField(blank=True, default=0, verbose_name='От')
    to_value = models.PositiveSmallIntegerField(blank=True, default=1000000, verbose_name='До')
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    item = models.ForeignKey('Item', on_delete=models.CASCADE, verbose_name="Предмет расчета")

    def __str__(self):
        return self.NAME + ' ' + str(self.item)

    class Meta:
        verbose_name = 'Тариф для расчета'
        verbose_name_plural = 'Тарифы для расчета'
        ordering = ['-created']

    @classmethod
    def create(cls, type, item, value=0, from_value=0, to_value=1000000, el_counter_discrete=''):
        tarif = cls(type=type, item=item, value=value, from_value=from_value, to_value=to_value,
                    el_counter_discrete=el_counter_discrete)
        return tarif


class Info(models.Model):
    LST = [('electricity', 'Электричество'), ('water', 'Вода'), ('gas', 'Газ'), ('kv', 'Квартплата'),
           ('tbo', 'ТБО'), ('domofon', 'Домофон'), ('inet', 'Интернет'), ('other', 'Другой вид оплаты')]

    item = models.CharField(choices=LST, max_length=20, blank=False, verbose_name="Предмет")
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

    type = models.CharField(choices=TYPE, default='flat', max_length=15, blank=False, verbose_name="Тип счетчика")
    value = models.PositiveIntegerField(blank=False, verbose_name='Показания')
    previous = models.PositiveIntegerField(blank=True, default=0, verbose_name='Предыдущие показания')
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата ввода показаний")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    item = models.ForeignKey('Item', on_delete=models.CASCADE, verbose_name="Предмет расчета")

    class Meta:
        verbose_name = 'Показания счетчика'
        verbose_name_plural = 'Показания счетчиков'
        ordering = ['-created']

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


class ToPay(models.Model):
    NAME = 'Расчет для оплаты'

    value = models.FloatField(default=0, verbose_name=NAME)
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


class Payed(models.Model):
    NAME = 'Оплачено'

    value = models.FloatField(default=0, verbose_name=NAME)
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

    value = models.FloatField(default=0, verbose_name=NAME)
    month = models.CharField(max_length=2, choices=MONTHES, verbose_name='Месяц расчета')
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    item = models.ForeignKey('Item', on_delete=models.CASCADE, verbose_name="Предмет расчета")

    class Meta:
        verbose_name = 'Долг'
        verbose_name_plural = 'Долг'
        ordering = ['created']

    def __str__(self):
        return self.NAME + ' ' + str(self.item) + ' ' + str(self.month)
