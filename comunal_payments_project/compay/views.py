import datetime

from django.shortcuts import render, redirect

from .forms import *

menu = [{"title": "Главная страница", 'url_name': 'home'}, {"title": "Добавить объект", 'url_name': 'add_app'}, ]
LST = ['electricity', 'water', 'gas']
msgs = []
date = datetime.date.today()
month = date.month

# DONE
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


# DONE
def app(request, app_selected):
    global msgs, month
    clean_msgs()
    create_items_for_app(app_selected)

    date = datetime.date.today()
    month = date.month

    if request.method == 'GET':
        try:
            c = request.GET['count']
        except:
            c = None
        if c:
            summary = check_and_calculation(app_selected, month)
        else:
            summary = '0'
    else:
        summary = '0'

    items = Item.objects.filter(app_id=app_selected)
    ap = items.first().app

    info_list = Info.objects.filter(app=ap).order_by('-created')[:4]
    if len(info_list) == 0:
        info_list = ['Сейчас тут нет справочной информации', 'Вы можете заполнить её в разделе Инфо']

    submenu = [{"title": "Посмотреть счетчики", 'url_name': 'counters', 'app_selected': app_selected},
               {"title": "Посмотреть тарифы", 'url_name': 'tarifs', 'app_selected': app_selected},
               {"title": "Ввести счетчики", 'url_name': 'enter_counters', 'app_selected': app_selected},
               {"title": "Ввести тарифы", 'url_name': 'enter_tarifs', 'app_selected': app_selected},
               {"title": "    Инфо    ", 'url_name': 'info', 'app_selected': app_selected},
               {"title": "Конфигурация", 'url_name': 'config_app', 'app_selected': app_selected}]  # !!!HERE!!!!

    context = {'title': 'Страница объекта: ', 'menu': menu, 'submenu': submenu, 'msgs': msgs, 'date': date,
               'month': month, 'ap': ap, 'items': items, 'app_selected': app_selected, 'info_list': info_list,
               'summary': summary}
    return render(request, 'compay/app.html', context)


# DONE
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


# HERE !!!
def item(request, app_selected, item_selected):
    clean_msgs()
    item = Item.objects.get(id=item_selected)
    counters = Counter.objects.filter(item=item_selected).order_by('-created')[:5]

    # ДОБАВИТЬ ОПЛАТЫ НАЧИСЛЕНИЯ ДОЛГИ И ТАРИФЫ

    if not counters:
        obj = 'Нет записей'
        submenu = [{"title": "Редактировать инфо", 'url_name': 'enter_info'}]
    elif item.is_counter in ['counter', 'day', 'night']:
        obj = ''
        submenu = [{"title": "Ввести показания", 'url_name': 'counter'},
                   {"title": "Изменить тариф", 'url_name': 'tarif'},
                   {"title": "Редактировать инфо", 'url_name': 'enter_info'}]
    else:
        submenu = [{"title": "Редактировать инфо", 'url_name': 'enter_info'}]

    context = {'title': 'Показания для: ', 'menu': menu, 'msgs': msgs, 'item': item, 'obj': obj,
               'app_selected': app_selected, 'submenu': submenu, 'counter_list': counters}
    return render(request, 'compay/item.html', context)


def calculation(request, app_selected, month_selected):
    pass


# DONE
def info(request, app_selected):
    clean_msgs()

    ap = Appartment.objects.get(id=app_selected)

    info_list = Info.objects.filter(app=ap)

    if not info:
        obj = 'Нет записей'
    else:
        obj = ''

    context = {'title': 'Информация для расчетов по: ', 'menu': menu, 'msgs': msgs, 'ap': ap, 'obj': obj,
               'app_selected': app_selected, 'info_list': info_list}
    return render(request, 'compay/info.html', context)


# DONE
def enter_info(request, app_selected, item_selected):
    clean_msgs()

    ap = Appartment.objects.get(id=app_selected)
    item = Item.objects.get(id=item_selected)

    try:
        info = Info.objects.filter(item=item.item_name, app=ap)[0]
    except:
        info = None

    if not info:
        info = Info(item=item.item_name, app=ap)

    if request.method == 'POST':
        form = InfoForm(request.POST, instance=info)
        if form.is_valid():
            form.save()
            return redirect('app', app_selected)
        else:
            msgs.append(dict(key=str(item) + ' Error', text='Ошибка ввода данных!',
                             description='Error'))
            return redirect('enter_info', app_selected, item_selected)
    else:
        form = InfoForm(instance=info)

    context = {'title': 'Заполните информацию для: ', 'menu': menu, 'msgs': msgs, 'item': item,
               'app_selected': app_selected, 'submenu': None, 'form': form}
    return render(request, 'compay/enter_info.html', context)


# DONE
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
            context = {'title': 'Проверьте конфигурацию объекта', 'menu': menu, 'msgs': msgs, 'ap': ap, 'form': form}
            return render(request, 'compay/config_app.html', context)
    else:
        form = AppartmentEditForm(instance=ap)
        context = {'title': 'Проверьте конфигурацию объекта: ', 'menu': menu, 'msgs': msgs, 'ap': ap, 'form': form,
                   'app_selected': app_selected}
        return render(request, 'compay/config_app.html', context)


# DONE
def enter_tarifs(request, app_selected):
    global msgs
    clean_msgs('config_item')
    clean_msgs('Calculation-Tarif')

    TYPES = ['counter', 'day', 'night', 'tarif']
    LST = ['electricity', 'water', 'gas', 'kv', 'domofon', 'inet', 'tbo', 'other']
    tarif_list = []

    ap = Appartment.objects.get(pk=app_selected)

    for field, value in ap.__dict__.items():
        if field in LST:
            if value:
                items = Item.objects.filter(app_id=app_selected, item_name=field)
                for it in items:
                    if it.is_counter in TYPES:
                        if it.item_name == 'electricity':
                            if ap.el_counter_discrete:
                                tarif1 = Tarif.objects.filter(item=it, type=it.is_counter, el_counter_discrete='0-150'
                                                              ).order_by('-created').first()
                                if not tarif1:
                                    tarif1 = Tarif.create(type=it.is_counter, el_counter_discrete='0-150', value=0,
                                                          item=it, from_value=0, to_value=150)
                                tarif_list.append(tarif1)
                                tarif2 = Tarif.objects.filter(item=it, type=it.is_counter, el_counter_discrete='150-450'
                                                              ).order_by('-created').first()
                                if not tarif2:
                                    tarif2 = Tarif.create(type=it.is_counter, el_counter_discrete='150-450', value=0,
                                                          item=it, from_value=150, to_value=450)
                                tarif_list.append(tarif2)
                                tarif3 = Tarif.objects.filter(item=it, type=it.is_counter, el_counter_discrete='450+'
                                                              ).order_by('-created').first()
                                if not tarif3:
                                    tarif3 = Tarif.create(type=it.is_counter, el_counter_discrete='450+', value=0,
                                                          item=it, from_value=450, to_value=1000000)
                                tarif_list.append(tarif3)
                            else:
                                tarif4 = Tarif.objects.filter(item=it, type=it.is_counter, el_counter_discrete=''
                                                              ).order_by('-created').first()
                                if not tarif4:
                                    tarif4 = Tarif.create(type=it.is_counter, value=0, item=it)
                                tarif_list.append(tarif4)
                        else:
                            tarif = Tarif.objects.filter(item=it, type=it.is_counter).order_by('-created').first()
                            if not tarif:
                                tarif = Tarif.create(type=it.is_counter, value=0, item=it)
                            tarif_list.append(tarif)

    if request.method == "POST":
        form_list = []
        i = 1
        valid = False
        for tarif in tarif_list:
            form = TarifForm(request.POST, instance=tarif, prefix=str(i))
            i += 1
            if form.is_valid():
                valid = True
                form_list.append(form)
        if valid:
            for form in form_list:
                form.save()
            return redirect('app', app_selected)
        else:
            msgs.append(dict(key=str(ap) + ' Error', text='Ошибка ввода данных!',
                             description='Error'))
            return redirect('enter_tarifs', app_selected)
    else:
        form_list = []
        i = 1
        for tarif in tarif_list:
            label = ' ' + str(tarif.item) + ': '
            form = TarifForm(instance=tarif, prefix=str(i))
            i += 1
            if tarif.to_value == 150:
                label += '(0..150)'
            elif tarif.to_value == 450:
                label += '(150..450)'
            elif tarif.from_value == 450:
                label += '(450 и выше)'
            form.label_suffix = label
            form_list.append(form)

    context = {'title': 'Введите значения тарифов: ', 'menu': menu, 'msgs': msgs,
               'ap': ap, 'app_selected': app_selected, 'form_list': form_list}
    return render(request, 'compay/enter_tarifs.html', context)


# Убрать submenu
def tarifs(request, app_selected):
    global msgs, LST
    clean_msgs()
    tarif_list = []

    submenu = [{"title": "Ввести показания", 'url_name': 'counter'},
               {"title": "Изменить тариф", 'url_name': 'tarif'},
               {"title": "История начислений", 'url_name': 'counter'}]

    ap = Appartment.objects.get(pk=app_selected)
    items = Item.objects.filter(app_id=app_selected)
    for item in items:
        tarifs = Tarif.objects.filter(item=item.pk).order_by('-created')[:1]

        for tarif in tarifs:
            tarif_list.append(tarif)

    context = {'title': 'Тарифы для: ', 'menu': menu, 'submenu': submenu, 'msgs': msgs,
               'ap': ap, 'app_selected': app_selected, 'tarif_list': tarif_list}
    return render(request, 'compay/tarifs.html', context)


# DONE
def tarif(request, app_selected, item_selected):
    global msgs, LST
    clean_msgs()
    tarif2 = None

    item = Item.objects.get(pk=item_selected)
    tarifs = Tarif.objects.filter(item=item_selected).order_by('-created')[:3]

    if not tarifs:
        obj = 'Пока тут нет записей'
    elif tarifs[0].el_counter_discrete != '':
        tarif3 = Tarif.create(item=tarifs[0].item, type=tarifs[0].type,
                              value=tarifs[0].value, from_value=tarifs[0].from_value,
                              to_value=tarifs[0].to_value, el_counter_discrete=tarifs[0].el_counter_discrete)
        tarif2 = Tarif.create(item=tarifs[1].item, type=tarifs[1].type,
                              value=tarifs[1].value, from_value=tarifs[1].from_value,
                              to_value=tarifs[1].to_value, el_counter_discrete=tarifs[1].el_counter_discrete)
        tarif = Tarif.create(item=tarifs[2].item, type=tarifs[2].type,
                             value=tarifs[2].value, from_value=tarifs[2].from_value,
                             to_value=tarifs[2].to_value, el_counter_discrete=tarifs[2].el_counter_discrete)
        obj = ''
    else:
        obj = ''
        tarif = Tarif.create(item=tarifs[0].item, type=tarifs[0].type,
                             value=tarifs[0].value, from_value=tarifs[0].from_value,
                             to_value=tarifs[0].to_value, el_counter_discrete='')
    form_list = []
    if request.method == 'POST':
        form = TarifForm(request.POST, instance=tarif, prefix=1)
        if tarif2:
            form2 = TarifForm(request.POST, instance=tarif2, prefix=2)
            form3 = TarifForm(request.POST, instance=tarif3, prefix=3)
            if form2.is_valid() and form3.is_valid() and form.is_valid():
                form.save()
                form2.save()
                form3.save()
                return redirect('tarifs', app_selected)
            else:
                msgs.append(dict(key=str(item) + ' Error', text='Ошибка ввода данных!',
                                 description='Error'))
        elif form.is_valid():
            form.save()
            return redirect('tarifs', app_selected)
        else:
            msgs.append(dict(key=str(item) + ' Error', text='Ошибка ввода данных!',
                             description='Error'))
    else:
        form = TarifForm(instance=tarif, prefix=1)
        form.label_suffix = tarif.get_el_counter_discrete_display()
        form_list.append(form)
        if tarif2:
            form2 = TarifForm(instance=tarif2, prefix=2)
            form2.label_suffix = tarif2.get_el_counter_discrete_display()
            form_list.append(form2)
            form3 = TarifForm(instance=tarif3, prefix=3)
            form3.label_suffix = tarif3.get_el_counter_discrete_display()
            form_list.append(form3)

    context = {'title': 'Тариф для: ', 'menu': menu, 'msgs': msgs, 'obj': obj,
               'item': item, 'app_selected': app_selected, 'item_selected': item_selected,
               'tarif_list': tarifs, 'form_list': form_list}
    return render(request, 'compay/tarif.html', context)


# DONE
def enter_counters(request, app_selected):
    global msgs, LST
    clean_msgs('config_item')
    clean_msgs('Calculation-Counter')

    TYPES = ['counter', 'day', 'night']
    counter_list = []

    ap = Appartment.objects.get(pk=app_selected)

    for field, value in ap.__dict__.items():
        if field in LST:
            if value:
                items = Item.objects.filter(app_id=app_selected).filter(item_name=field)
                for it in items:
                    if it.is_counter in TYPES:
                        counter = Counter.objects.filter(item=it, type=it.is_counter).order_by('-created').first()
                        if not counter:
                            counter = Counter.create(type=it.is_counter, value=0, item=it)
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
            msgs.append(dict(key=str(ap) + ' Error', text='Ошибка ввода данных!',
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


# Убрать submenu
def counters(request, app_selected):
    global msgs, LST
    clean_msgs()
    counter_list = []

    submenu = [{"title": "Ввести показания", 'url_name': 'counter'},
               {"title": "Изменить тариф", 'url_name': 'tarif'},
               {"title": "История начислений", 'url_name': 'counter'}]

    ap = Appartment.objects.get(pk=app_selected)
    items = Item.objects.filter(app_id=app_selected)
    for item in items:
        counters = Counter.objects.filter(item=item.pk).order_by('-created')[:2]

        if len(counters) > 1:  # Заполняем поле предыдущих показаний
            c2 = counters[1]
            c1 = counters[0]
            c1.previous = c2.value
            c1.save()

        for counter in counters:
            counter_list.append(counter)

    context = {'title': 'Показания счетчиков: ', 'menu': menu, 'submenu': submenu, 'msgs': msgs,
               'ap': ap, 'app_selected': app_selected, 'counter_list': counter_list}
    return render(request, 'compay/counters.html', context)


def counter(request, app_selected, item_selected):
    global msgs, LST
    TYPES = ['counter', 'day', 'night']
    clean_msgs()

    item = Item.objects.get(pk=item_selected)
    counters = Counter.objects.filter(item=item_selected).order_by('-created')[:2]

    if not counters:
        obj = 'Пока тут нет записей'
    else:
        obj = ''

    counter = Counter.create(item=counters[0].item, type=counters[0].type,
                             value=counters[0].value, previous=counters[0].value)

    if request.method == 'POST':
        form = CounterForm(request.POST, instance=counter)
        if form.is_valid():
            form.save()
            return redirect('app', app_selected)
        else:
            msgs.append(dict(key=str(item) + ' Error', text='Ошибка ввода данных!',
                             description='Error'))
    else:
        form = CounterForm(instance=counter)

    context = {'title': 'Показания счетчиков: ', 'menu': menu, 'msgs': msgs, 'obj': obj,
               'item': item, 'app_selected': app_selected, 'item_selected': item_selected,
               'counter_list': counters, 'form': form}
    return render(request, 'compay/counter.html', context)


def topay(request, app_selected):
    global msgs, LST, month
    clean_msgs()
    topay_list = []

    submenu = [{"title": "Ввести показания", 'url_name': 'counter'},
               {"title": "Изменить тариф", 'url_name': 'tarif'},
               {"title": "История начислений", 'url_name': 'counter'}]

    ap = Appartment.objects.get(pk=app_selected)
    items = Item.objects.filter(app_id=app_selected)

    for it in items:
        topay = ToPay.objects.filter(item=it.pk, month=month)[0]
        topay_list.append(topay)

    context = {'title': 'Расчет для оплаты по: : ', 'menu': menu, 'submenu': submenu, 'msgs': msgs,
               'ap': ap, 'app_selected': app_selected, 'topay_list': topay_list}
    return render(request, 'compay/topay.html', context)


def create_items_for_app(app_selected):
    global msgs
    clean_msgs()

    lst_template = ['electricity', 'water', 'gas', 'kv', 'tbo', 'domofon', 'inet', 'other']
    lst = []
    ap = Appartment.objects.get(id=app_selected)
    items = Item.objects.filter(app_id=app_selected)

    # Добавляем используемые для оплаты предметы в список для конкретного объекта:
    fields = ap.__dict__
    for field, value in fields.items():
        if field in lst_template:
            if value:
                lst.append(field)

    conf = {'electricity': 'el_is_counter', 'water': 'wat_is_counter', 'gas': 'gas_is_counter'}
    if not items:
        # Cоздаем пустой предмет для конфигурации:
        for el in lst:
            a = Item(item_name=el, app_id=app_selected)
            if el in conf.keys():
                if el == 'electricity':
                    if ap.el_night:
                        a.is_counter = 'total'
                        b = Item(item_name=el, app_id=app_selected, is_counter='day')
                        c = Item(item_name=el, app_id=app_selected, is_counter='night')
                        a.save()
                        b.save()
                        c.save()
                    else:
                        a.is_counter = ap.__dict__[conf[el]]
                        a.save()
                else:
                    a.is_counter = ap.__dict__[conf[el]]
                    a.save()
            else:
                a.save()

        msgs.append(dict(key=str(ap), text='Вам необходимо задать начальные показания счетчиков',
                         description='config_item'))

    else:  # Проверяем есть ли отсутствующие предметы
        for el in lst:
            exist = False
            for item in items:
                if item.item_name == el:
                    exist = True
            if not exist:  # Добавляет отсутствующие предметы
                a = Item(item_name=el, app_id=app_selected)
                if el in conf.keys():
                    if el == 'electricity':
                        if ap.el_night:
                            a.is_counter = 'total'
                            b = Item(item_name=el, app_id=app_selected, is_counter='day')
                            c = Item(item_name=el, app_id=app_selected, is_counter='night')
                            a.save()
                            b.save()
                            c.save()
                            msgs.append(dict(key=str(b) + '/' + str(c), text='Вам необходимо задать начальные '
                                                                             'показания счетчиков',
                                             description='config_item'))
                        else:
                            a.is_counter = ap.__dict__[conf[el]]
                            a.save()
                            if a.is_counter == 'counter':
                                msgs.append(dict(key=a, text='Вам необходимо задать начальные '
                                                             'показания счетчиков', description='config_item'))
                    else:
                        a.is_counter = ap.__dict__[conf[el]]
                        a.save()
                        if a.is_counter == 'counter':
                            msgs.append(dict(key=a, text='Вам необходимо задать начальные '
                                                         'показания счетчиков', description='config_item'))
                else:
                    a.save()


def check_and_calculation(app_selected, month_selected):
    global msgs
    lst_template = ['electricity', 'water', 'gas', 'kv', 'tbo', 'domofon', 'inet', 'other']
    lst = []
    summary = 0
    ap = Appartment.objects.get(id=app_selected)
    items = Item.objects.filter(app=ap)

    # Добавляем используемые для оплаты предметы в список для конкретного объекта:
    fields = ap.__dict__
    for field, value in fields.items():
        if field in lst_template:
            if value:
                lst.append(field)

    topay_night = topay_day = 0
    for el in lst:  # Проверка введены ли тарифы и счетчики
        for item in items:
            if item.item_name == el and item.is_counter != 'total':
                ok = True
                tarifs = Tarif.objects.filter(item=item.id).order_by('-created')[:3]
                tarif = tarifs.first()
                if not tarif:
                    msg_add(key=item, text='Не задан тариф для расчёта', description='Calculation-Tarif')
                    ok = False
                if item.is_counter in ['day', 'night', 'counter']:
                    counter = Counter.objects.filter(item=item, created__month=month_selected).order_by(
                        '-created').first()
                    if not counter:
                        msg_add(key=item, text=f'Не введены показания счетчика',
                                description='Calculation-Counter')
                    else:
                        if ok:
                            if tarif.el_counter_discrete == '':
                                sum = tarif.value * (counter.value - counter.previous)
                                sum_str = '('+str(counter.value)+' - '+str(counter.previous)+') *'+str(tarif.value)+' = '+str(sum)
                                try:
                                    topay = ToPay.objects.filter(item=item, month=month_selected).first()
                                    topay.value = sum
                                    topay.calculation = sum_str
                                except:
                                    topay = ToPay(value=sum, month=month_selected, item=item, calculation=sum_str)
                                    # Добавить примечание с данными
                                topay.save()
                                summary += topay.value
                                if item.item_name == 'electricity' and item.is_counter == 'day':
                                    topay_day = topay.value
                                elif item.item_name == 'electricity' and item.is_counter == 'night':
                                    topay_night = topay.value
                            else:
                                for t in tarifs:
                                    if t.from_value == 0:
                                        t0_150 = t.value
                                    elif t.from_value == 150:
                                        t150_600 = t.value
                                    elif t.from_value == 600:
                                        t600 = t.value
                                dif = counter.value - counter.previous
                                if dif > 150:
                                    if dif > 600:
                                        sum = 150 * t0_150 + 450 * t150_600 + (dif - 600) * t600
                                        sum_str = '150 * '+str(t0_150)+' + 450 * '*str(t150_600)+' + ('+str(counter.value)+' - ' + str(counter.previous)+' - 600) * ' + str(t600)+' = '+str(sum)
                                    else:
                                        sum = 150 * t0_150 + (dif - 150) * t150_600
                                        sum_str = '150 * '+str(t0_150)+' + ('+str(counter.value)+' - '+ str(counter.previous)+' - 150) * ' + str(t150_600)+' = '+str(sum)
                                else:
                                    sum = dif * t0_150
                                    sum_str = '(' + str(counter.value)+' - '+str(counter.previous)+') * ' + str(t0_150)+' = '+str(sum)
                                try:
                                    topay = ToPay.objects.filter(item=item, month=month_selected).first()
                                    topay.value = sum
                                    topay.calculation = sum_str
                                except:
                                    topay = ToPay(value=sum, calculation=sum_str, month=month_selected, item=item)
                                    # Добавить примечание с данными
                                topay.save()
                                summary += topay.value
                                if item.item_name == 'electricity' and item.is_counter == 'day':
                                    topay_day = topay.value
                                elif item.item_name == 'electricity' and item.is_counter == 'night':
                                    topay_night = topay.value
                elif item.is_counter == 'tarif':
                    if ok:
                        try:
                            topay = ToPay.objects.filter(item=item, month=month_selected).first()
                            topay.value = tarif.value
                            topay.calculation = 'тариф - ' + str(tarif.value)
                        except:
                            topay = ToPay(value=tarif.value, calculation=('тариф - ' + str(tarif.value)), month=month_selected, item=item)
                        topay.save()
                        summary += topay.value

    if 'electricity' in lst:
        for item in items:
            if item.item_name == 'electricity':
                if item.is_counter == 'total':
                    try:
                        topay = ToPay.objects.filter(item=item, month=month_selected).first()
                        topay.value = (topay_night + topay_day)
                        topay.calculation = 'день-' + str(topay_day) + ' + ночь-' + str(topay_night)+' = '+str(topay_night + topay_day)
                    except:
                        topay = ToPay(value=(topay_night + topay_day), calculation=('день-'+ str(topay_day) + ' + ночь-'+ str(topay_night)+' = '+str(topay_night + topay_day)), month=month_selected, item=item)
                    topay.save()

    return summary


def clean_msgs(msg_to_clean=None):
    global msgs
    msgs_clean_list = ['Error']
    msgs_clean_list.append(msg_to_clean)

    for msg in msgs:
        if msg['description'] in msgs_clean_list:
            msgs.remove(msg)


def msg_add(key, text, description):
    global msgs

    ok = True
    for msg in msgs:
        if msg['key'] == key and msg['description'] == description:
            ok = False
    if ok:
        msgs.append(dict(key=key, text=text, description=description))
