from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.cache import cache
from .models import *
from .forms import *

menu = [{"title": "Главная страница", 'url_name': 'home'}, {"title": "Добавить объект", 'url_name': 'add_app'}, ]
LST = ['electricity', 'water', 'gas']
msgs = []


def index(request):
    global msgs
    clean_msgs()

    apps = Appartment.objects.all()
    if apps.count() > 0:
        obj = ''
    else:
        obj = 'Пока тут нет объектов. Добавьте свой'
    context = {'title': 'Главная страница', 'menu': menu, 'msgs': msgs, 'apps': apps, 'obj': obj}
    return render(request, 'compay/index.html', context)


def app(request, app_selected):
    global msgs
    clean_msgs()
    create_items_for_app(app_selected)

    items = Item.objects.filter(app_id=app_selected)
    ap = items.first().app

    submenu = [{"title": "Конфигурация", 'url_name': 'config_app', 'app_selected': app_selected},
               {"title": "Ввести счетчики", 'url_name': 'enter_counters', 'app_selected': app_selected},
               {"title": "Посмотреть счетчики", 'url_name': 'counters', 'app_selected': app_selected}]

    context = {'title': 'Страница объекта: ', 'menu': menu, 'submenu': submenu, 'msgs': msgs,
               'ap': ap, 'items': items, 'app_selected': app_selected}
    return render(request, 'compay/app.html', context)


def add_app(request):
    global msgs
    clean_msgs()

    if request.method == 'POST':
        form = AppartmentForm(request.POST)
        if form.is_valid():
            a = form.save()
            create_items_for_app(app_selected=a.pk)  # Создаются предметы оплаты по конфигурции объекта
            return redirect('home')
        else:
            msgs.append(dict(key='Error', text='Ошибка ввода данных', description='Error'))
            form = AppartmentForm()
            context = {'title': 'Создайте новый объект:', 'menu': menu, 'msgs': msgs, 'form': form}
            return render(request, 'compay/add_app.html', context)
    else:
        form = AppartmentForm()
        context = {'title': 'Создайте новый объект:', 'menu': menu, 'msgs': msgs, 'form': form}
        return render(request, 'compay/add_app.html', context)


def item(request, app_selected, item_selected):
    item = Item.objects.get(id=item_selected)

    if not item:
        item = 'Нет записей'

    submenu = [{"title": "Ввести показания", 'url_name': 'config_app_item'},
               {"title": "Тариф", 'url_name': 'config_app_item'},
               {"title": "История начислений", 'url_name': 'config_app_item'},
               {"title": "Конфигурация", 'url_name': 'config_app_item'}]

    context = {'title': '', 'menu': menu, 'msgs': msgs, 'item': item,
               'app_selected': app_selected, 'submenu': submenu}
    return render(request, 'compay/item.html', context)


def config_app(request, app_selected):
    global msgs
    clean_msgs()
    create_items_for_app(app_selected)

    ap = Appartment.objects.get(pk=app_selected)

    if request.method == 'POST':
        form = AppartmentEditForm(request.POST, instance=ap)
        if form.is_valid():
            a = form.save()
            create_items_for_app(app_selected=a.pk)  # Создаются предметы оплаты по конфигурции объекта
            return redirect('app', app_selected)
        else:
            msgs.append(dict(key='Error', text='Ошибка ввода данных', description='Error'))
            form = AppartmentEditForm(request.POST, instance=ap)
            context = {'title': 'Проверьте конфигурацию объекта', 'menu': menu, 'msgs': msgs, 'form': form}
            return render(request, 'compay/config_app.html', context)
    else:
        form = AppartmentEditForm(instance=ap)
        context = {'title': 'Проверьте конфигурацию объекта', 'menu': menu, 'msgs': msgs, 'form': form,
                   'app_selected': app_selected}
        return render(request, 'compay/config_app.html', context)


def config_app_item(request, app_selected, item_selected):
    global msgs
    clean_msgs()

    item = Item.objects.get(pk=item_selected)

    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            clean_msgs('config_item')
            return redirect('app', app_selected)
    else:
        form = ItemForm(instance=item)

    context = {'title': 'Введите конфигурацию для расчета оплаты:', 'menu': menu, 'msgs': msgs,
               'app_selected': app_selected, 'form': form, 'item': item}
    return render(request, 'compay/config_app_item.html', context)


def enter_counters(request, app_selected):
    global msgs, LST
    clean_msgs()
    counter_list = []

    ap = Appartment.objects.get(pk=app_selected)

    for field, value in ap.__dict__.items():

        if field in LST:

            if value:

                it = Item.objects.filter(app_id=app_selected).get(item_name=field)
                if it.is_counter:

                    if it.day_night:

                        counter_day = Counter.create(type='day', value=0, item=it)
                        counter_night = Counter.create(type='night', value=0, item=it)
                        counter_list.append(counter_day)
                        counter_list.append(counter_night)
                    else:
                        counter = Counter.create(type='flat', value=0, item=it)
                        counter_list.append(counter)

    if request.method == "POST":
        form_list = []
        i = 1
        valid = False
        for counter in counter_list:
            form = CounterForm(request.POST, instance=counter, prefix=str(i))
            i += 1
            if form.is_valid():
                valid = True
                form_list.append(form)
        if valid:
            for form in form_list:
                form.save()
            return redirect('counters', app_selected)
        else:
            msgs.append(dict(key=str(ap)+' Error', text='Ошибка ввода данных!',
                             description='Error'))
    else:
        form_list = []
        i = 1
        for counter in counter_list:
            label = ' ' + str(counter.item) + ' ' + counter.get_type_display() + ':'
            form = CounterForm(instance=counter, prefix=str(i))
            i += 1
            form.label_suffix = label
            form_list.append(form)

    context = {'title': 'Введите показания счетчиков: ', 'menu': menu, 'msgs': msgs,
               'ap': ap, 'app_selected': app_selected, 'form_list': form_list}
    return render(request, 'compay/enter_counters.html', context)


def counters(request, app_selected):
    global msgs, LST
    clean_msgs()
    counter_list = []

    ap = Appartment.objects.get(pk=app_selected)
    items = Item.objects.filter(app_id=app_selected)
    for item in items:
        counters = Counter.objects.filter(item=item.pk).order_by('-created', 'type')[:4]

        if len(counters) > 1: # Заполняем поле предыдущих показаний
            if len(counters) > 3:
                    c4 = counters[3]
                    c3 = counters[1]
                    c2 = counters[2]
                    c1 = counters[0]
                    c1.previous = c2.value
                    c3.previous = c4.value
                    c1.save()
                    c3.save()
            else:
                c2 = counters[1]
                c1 = counters[0]
                c1.previous = c2.value
                c1.save()

        for counter in counters:
            counter_list.append(counter)

    context = {'title': 'Показания счетчиков: ', 'menu': menu, 'msgs': msgs,
               'ap': ap, 'app_selected': app_selected, 'counter_list': counter_list}
    return render(request, 'compay/counters.html', context)

def create_items_for_app(app_selected):
    global msgs
    clean_msgs()

    lst_template = ['electricity', 'water', 'gas', 'kv', 'tbo', 'domofon', 'inet', 'other']
    lst = []
    ap = Appartment.objects.get(id=app_selected)
    items = Item.objects.filter(app_id=app_selected)

    # Убираем неиспользуемые для оплаты предметы из списка LST для конкретного объекта:
    fields = ap.__dict__
    for field, value in fields.items():
        if field in lst_template:
            if value:
                lst.append(field)

    if not items:
        # Cоздаем пустой предмет для конфигурации:
        for el in lst:
            a = Item(item_name=el, app_id=app_selected)
            a.save()
        msgs.append(dict(key=str(ap), text='Вам необходимо задать конфигурацию для каждого вида оплаты',
                         description='config_item'))

    else:  # Проверяем есть ли отсутствующие предметы
        for el in lst:
            exist = False
            for item in items:
                if item.item_name == el:
                    exist = True
            if not exist:  # Добавляет отсутствующие предметы
                a = Item(item_name=el, app_id=app_selected)
                a.save()
                msgs.append(dict(key=a, text='Вам необходимо задать конфигурацию', description='config_item'))


def clean_msgs(msg_to_clean=None):
    global msgs
    msgs_clean_list = ['Error']
    msgs_clean_list.append(msg_to_clean)

    for msg in msgs:
        if msg['description'] in msgs_clean_list:
            msgs.remove(msg)
