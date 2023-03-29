import calendar

from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required

from .forms import *

menu = {"title": "Главная страница", 'url_name': 'home'}
LST = ['electricity', 'water', 'gas']
msgs = []
date = datetime.date.today()
month = date.month

@login_required
def index(request):
    global msgs, date, month
    clean_msgs('Calculation-Tarif')
    clean_msgs('Calculation-Counter')
    clean_msgs('config_item')
    clean_msgs('Pay-Enter')


    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        form = MonthForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
    else:
        form = MonthForm()

    apps = Appartment.objects.all()

    if apps.count() > 0:
        obj = ''
    else:
        obj = 'Пока тут нет объектов. Добавьте новый'

    pay_sum_dict = {'Месяц': calendar.month_name[date.month], 'Начислено': 0, 'Оплачено': 0, 'Долг': 0}
    for ap in apps:
        pay_sum = PaySummary.objects.filter(app=ap, month=date.month).first()
        if pay_sum:
            pay_sum_dict['Месяц'] = pay_sum.get_month_display
            pay_sum_dict['Начислено'] += round(pay_sum.topay, 1)
            pay_sum_dict['Оплачено'] += round(pay_sum.payed, 1)
            pay_sum_dict['Долг'] += round(pay_sum.debt, 1)
    pay_sum_dict['Начислено'] = str(pay_sum_dict['Начислено'])+' руб'
    pay_sum_dict['Оплачено'] = str(pay_sum_dict['Оплачено'])+' руб'
    pay_sum_dict['Долг'] = str(pay_sum_dict['Долг'])+' руб'

    context = {'title': 'Приложение для учета комунальных платежей', 'menu': menu, 'msgs': msgs, 'apps': apps,
               'obj': obj, 'form': form, 'date': date, 'pay_sum_dict': pay_sum_dict}
    return render(request, 'compay/index.html', context)


@login_required
def app(request, app_selected):
    global msgs, month, date
    clean_msgs('Pay-Enter')
    create_items_for_app(app_selected)

    obj = ''

    try:
        pay_sum = PaySummary.objects.filter(app=app_selected, month=date.month).first()
    except:
        pass
    if not pay_sum:
        pay_sum = PaySummary(app_id=app_selected, month=date.month)
        btn = 'Расчёт'
    else:
        btn = 'Пересчёт'

    if request.method == 'GET':
        try:
            c = request.GET['count']
        except:
            c = None
        if c:
            pay_sum.topay, pay_selected = check_and_calculation(app_selected, date.month)
            pay_sum.payed, pay_sum.debt = count_payed_and_debts(app_selected, date.month)
            pay_sum.save()
        else:
            pay_selected = 0
    else:
        pay_selected = 0


    items = Item.objects.filter(app_id=app_selected, active=True)
    ap = Appartment.objects.get(pk=app_selected)

    if not items:
        obj = f'В конфигурации для {ap.name} не выбраны виды оплаты'

    info_list = Info.objects.filter(app=ap).order_by('-created')[:4]
    if len(info_list) == 0:
        info_list = ['Сейчас тут нет справочной информации', 'Вы можете заполнить её в разделе Инфо']

    submenu = [{"title": "Посмотреть счетчики", 'url_name': 'counters', 'app_selected': app_selected},
               {"title": "Посмотреть тарифы", 'url_name': 'tarifs', 'app_selected': app_selected},
               {"title": "Ввести счетчики", 'url_name': 'enter_counters', 'app_selected': app_selected},
               {"title": "Ввести тарифы", 'url_name': 'enter_tarifs', 'app_selected': app_selected},
               {"title": "Расчёт оплаты", 'url_name': 'pay', 'app_selected': app_selected},
               {"title": "    Инфо    ", 'url_name': 'info', 'app_selected': app_selected},
               {"title": "Конфигурация", 'url_name': 'config_app', 'app_selected': app_selected}]

    context = {'title': 'Страница объекта: ', 'menu': menu, 'submenu': submenu, 'msgs': msgs, 'date': date,
               'ap': ap, 'obj': obj, 'items': items, 'app_selected': app_selected, 'pay_selected': pay_selected,
               'info_list': info_list, 'pay_sum': pay_sum, 'btn': btn}
    return render(request, 'compay/app.html', context)


@login_required
def add_app(request):
    global msgs, date
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
            context = {'title': 'Создайте новый объект:', 'menu': menu, 'msgs': msgs, 'form': form, 'date': date}
            return render(request, 'compay/add_app.html', context)
    else:
        form = AppartmentForm()
        context = {'title': 'Создайте новый объект:', 'menu': menu, 'msgs': msgs, 'form': form, 'date': date}
        return render(request, 'compay/add_app.html', context)


@login_required
def item(request, app_selected, item_selected):
    global msgs, date
    clean_msgs()
    item = Item.objects.get(id=item_selected)
    counters = Counter.objects.filter(item=item_selected).order_by('-created')[:5]

    # ДОБАВИТЬ ОПЛАТЫ НАЧИСЛЕНИЯ ДОЛГИ И ТАРИФЫ

    if not counters:
        obj = 'Нет записей'
        submenu = [{"title": "Ввести показания", 'url_name': 'counter'},
                   {"title": "Редактировать инфо", 'url_name': 'enter_info'}]
    elif item.is_counter in ['counter', 'day', 'night']:
        obj = ''
        submenu = [{"title": "Ввести показания", 'url_name': 'counter'},
                   {"title": "Изменить тариф", 'url_name': 'tarif'},
                   {"title": "Редактировать инфо", 'url_name': 'enter_info'}]
    else:
        obj = ''
        submenu = [{"title": "Редактировать инфо", 'url_name': 'enter_info'}]

    context = {'title': 'Показания для: ', 'menu': menu, 'msgs': msgs, 'item': item, 'obj': obj,
               'app_selected': app_selected, 'submenu': submenu, 'counter_list': counters, 'date': date}
    return render(request, 'compay/item.html', context)


@login_required
def pay_history(request, app_selected, item_selected=0):
    global msgs, date
    clean_msgs('Pay-Enter')
    lst = []

    ap = Appartment.objects.get(id=app_selected)
    items = Item.objects.filter(app_id=app_selected)

    pay_list = Pay.objects.filter(item=item_selected).order_by('-month')

    for item in items:
        if item.is_counter not in ['day', 'night']:
            lst.append(item)

    if not lst:
        obj = f'В конфигурации для {ap.name} не выбраны виды оплаты'
    else:
        if item_selected == 0:
            obj = 'Выберите вид оплаты из списка'
        elif not pay_list:
            obj = 'По этому виду оплаты пока нет записей в истории платежей'
        else:
            obj = ''

    context = {'title': 'История платежей по: ', 'menu': menu, 'msgs': msgs, 'ap': ap, 'obj': obj,
               'app_selected': app_selected, 'pay_list': pay_list, 'date': date, 'lst': lst}
    return render(request, 'compay/pay_history.html', context)


@login_required
def statistic(request, app_selected):
    global msgs, date
    clean_msgs('Pay-Enter')
    obj = ''

    ap = Appartment.objects.get(id=app_selected)
    pay_sum = PaySummary.objects.filter(app=ap).order_by('created')

    if not pay_sum:
        obj = 'Тут пока нет записей истории платежей'


    context = {'title': 'История платежей по: ', 'menu': menu, 'msgs': msgs, 'ap': ap, 'obj': obj,
               'app_selected': app_selected, 'pay_sum': pay_sum, 'date': date}
    return render(request, 'compay/statistic.html', context)


@login_required
def info(request, app_selected):
    global msgs, date
    clean_msgs()
    lst = []
    obj = ''

    ap = Appartment.objects.get(id=app_selected)
    items = Item.objects.filter(app_id=app_selected)

    info_list = Info.objects.filter(app=ap)

    if not info_list:
        obj = 'Сейчас тут нет записей с информацией, для добавления выберите ссылку ниже:'
    else:
        obj = ''

    for item in items:
        if item.is_counter not in ['day', 'night']:
            lst.append(item)

    if not lst:
        obj = f'В конфигурации для {ap.name} не выбраны виды оплаты'

    context = {'title': 'Информация для расчетов по: ', 'menu': menu, 'msgs': msgs, 'ap': ap, 'obj': obj,
               'app_selected': app_selected, 'info_list': info_list, 'date': date, 'lst': lst}
    return render(request, 'compay/info.html', context)


@login_required
def enter_info(request, app_selected, item_selected):
    global date
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
               'app_selected': app_selected, 'submenu': None, 'form': form, 'date': date}
    return render(request, 'compay/enter_info.html', context)


@login_required
def config_app(request, app_selected):
    global msgs, date
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
                   'app_selected': app_selected, 'date': date}
        return render(request, 'compay/config_app.html', context)


@login_required
def enter_tarifs(request, app_selected):
    global msgs, date
    clean_msgs('config_item')
    clean_msgs('Calculation-Tarif')

    TYPES = ['counter', 'day', 'night', 'tarif']
    LST = ['electricity', 'water', 'gas', 'kv', 'domofon', 'inet', 'tbo', 'other']
    tarif_list = []
    obj = ''

    ap = Appartment.objects.get(pk=app_selected)

    for field, value in ap.__dict__.items():
        if field in LST:
            if value:
                items = Item.objects.filter(app_id=app_selected, item_name=field, active=True)
                for it in items:
                    if it.is_counter in TYPES:
                        if it.item_name == 'electricity':
                            if ap.el_counter_discrete:
                                tarif1 = Tarif.objects.filter(item=it, type=it.is_counter, el_counter_discrete='0-150'
                                                              ).order_by('-created').first()
                                if not tarif1:
                                    tarif1 = Tarif.create(type=it.is_counter, el_counter_discrete='0-150', value=0,
                                                          item=it)
                                tarif_list.append(tarif1)
                                tarif2 = Tarif.objects.filter(item=it, type=it.is_counter, el_counter_discrete='150-600'
                                                              ).order_by('-created').first()
                                if not tarif2:
                                    tarif2 = Tarif.create(type=it.is_counter, el_counter_discrete='150-600', value=0,
                                                          item=it)
                                tarif_list.append(tarif2)
                                tarif3 = Tarif.objects.filter(item=it, type=it.is_counter, el_counter_discrete='600+'
                                                              ).order_by('-created').first()
                                if not tarif3:
                                    tarif3 = Tarif.create(type=it.is_counter, el_counter_discrete='600+', value=0,
                                                          item=it)
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
            if tarif.el_counter_discrete == '0-150':
                label += '(0..150)'
            elif tarif.el_counter_discrete == '150-600':
                label += '(150..600)'
            elif tarif.el_counter_discrete == '600+':
                label += '(600 и выше)'
            form.label_suffix = label
            form_list.append(form)

    if not form_list:
        obj = f'В конфигурации для {ap.name} не выбраны виды оплаты'

    context = {'title': 'Введите значения тарифов: ', 'menu': menu, 'obj': obj, 'msgs': msgs,
               'ap': ap, 'app_selected': app_selected, 'form_list': form_list, 'date': date}
    return render(request, 'compay/enter_tarifs.html', context)


@login_required
def tarifs(request, app_selected):
    global msgs, LST, date
    clean_msgs()
    tarif_list = []
    obj = ''

    submenu = []

    ap = Appartment.objects.get(pk=app_selected)
    items = Item.objects.filter(app_id=app_selected, active=True)
    for item in items:
        tarifs = Tarif.objects.filter(item=item.pk).order_by('-created')

        for tarif in tarifs:
            tarif_list.append(tarif)

    if not tarif_list:
        obj = 'Сейчас тут нет записей, перейдите в меню Ввести тарифы'

    context = {'title': 'Тарифы для: ', 'menu': menu, 'submenu': submenu, 'obj': obj, 'msgs': msgs,
               'ap': ap, 'app_selected': app_selected, 'tarif_list': tarif_list, 'date': date}
    return render(request, 'compay/tarifs.html', context)


@login_required
def tarif(request, app_selected, item_selected):
    global msgs, LST, date
    clean_msgs()
    tarif2 = None

    item = Item.objects.get(pk=item_selected)
    tarifs = Tarif.objects.filter(item=item_selected).order_by('-created')[:3]

    if not tarifs:
        obj = 'Пока тут нет записей'
    elif tarifs[0].el_counter_discrete != '':
        tarif3 = Tarif.create(item=tarifs[0].item, type=tarifs[0].type,
                              value=tarifs[0].value, el_counter_discrete=tarifs[0].el_counter_discrete)
        tarif2 = Tarif.create(item=tarifs[1].item, type=tarifs[1].type,
                              value=tarifs[1].value, el_counter_discrete=tarifs[1].el_counter_discrete)
        tarif = Tarif.create(item=tarifs[2].item, type=tarifs[2].type,
                             value=tarifs[2].value, el_counter_discrete=tarifs[2].el_counter_discrete)
        obj = ''
    else:
        obj = ''
        tarif = Tarif.create(item=tarifs[0].item, type=tarifs[0].type,
                             value=tarifs[0].value, el_counter_discrete='')
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
               'tarif_list': tarifs, 'form_list': form_list, 'date': date}
    return render(request, 'compay/tarif.html', context)


@login_required
def enter_counters(request, app_selected):
    global msgs, LST, month, date
    clean_msgs('config_item')
    clean_msgs('Calculation-Counter')

    TYPES = ['counter', 'day', 'night']
    counter_list = []
    obj = ''

    ap = Appartment.objects.get(pk=app_selected)

    for field, value in ap.__dict__.items():
        if field in LST:
            if value:
                items = Item.objects.filter(app_id=app_selected, active=True).filter(item_name=field)
                for it in items:
                    if it.is_counter in TYPES:
                        counter = Counter.objects.filter(item=it, type=it.is_counter).order_by('-created').first()
                        if not counter or counter.created.month != date.month:
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

    if not form_list:
        obj = f'В конфигурации для {ap.name} нет счетчиков для заполнения'

    context = {'title': 'Введите показания счетчиков: ', 'menu': menu, 'obj': obj, 'msgs': msgs,
               'ap': ap, 'app_selected': app_selected, 'form_list': form_list, 'date': date}
    return render(request, 'compay/enter_counters.html', context)


@login_required
def counters(request, app_selected):
    global msgs, LST, date
    clean_msgs()
    counter_list = []
    obj = ''

    submenu = []

    ap = Appartment.objects.get(pk=app_selected)
    items = Item.objects.filter(app_id=app_selected, active=True)
    for item in items:
        counters = Counter.objects.filter(item=item.pk).order_by('-created')[:2]

        if len(counters) == 1:  # Заполняем поле предыдущих показаний
            if counters[0].previous == 0:
                counters[0].previous = counters[0].value
                counters[0].save()
        elif len(counters) > 1:
            c2 = counters[1]
            c1 = counters[0]
            c1.previous = c2.value
            c1.save()

        for counter in counters:
            counter_list.append(counter)

    if not counter_list:
        obj = 'Сейчас тут нет записей'

    context = {'title': 'Показания счетчиков: ', 'menu': menu, 'submenu': submenu, 'obj': obj, 'msgs': msgs,
               'ap': ap, 'app_selected': app_selected, 'counter_list': counter_list, 'date': date}
    return render(request, 'compay/counters.html', context)


# ПРОВЕРИТЬ month == month!
@login_required
def counter(request, app_selected, item_selected):
    global msgs, LST, month, date
    clean_msgs()

    item = Item.objects.get(pk=item_selected)
    counters = Counter.objects.filter(item=item_selected).order_by('-created')[:2]

    if not counters:
        obj = 'Пока тут нет записей'
        counter = Counter(item=item, type=item.is_counter)
    else:
        obj = ''
        if counters[0].created.month == date.month:
            counter = counters[0]
        else:
            counter = Counter.create(item=counters[0].item, type=counters[0].type,
                                     value=counters[0].value, previous=counters[0].value)

    if request.method == 'POST':
        form = CounterForm(request.POST, instance=counter)
        if form.is_valid():
            form.save()
            return redirect('counters', app_selected)
        else:
            msgs.append(dict(key=str(item) + ' Error', text='Ошибка ввода данных!',
                             description='Error'))
    else:
        form = CounterForm(instance=counter)

    context = {'title': 'Показания счетчиков: ', 'menu': menu, 'msgs': msgs, 'obj': obj,
               'item': item, 'app_selected': app_selected, 'item_selected': item_selected,
               'counter_list': counters, 'form': form, 'date': date}
    return render(request, 'compay/counter.html', context)


@login_required
def pay(request, app_selected, pay_selected=0):
    global msgs, LST, month, date
    clean_msgs()
    pay_list = []
    obj = ''

    submenu = [{"title": "История расчетов", 'url_name': 'pay_history', 'app_selected': app_selected},
               {"title": "Итоговый отчет", 'url_name': 'statistic', 'app_selected': app_selected}]

    ap = Appartment.objects.get(pk=app_selected)
    items = Item.objects.filter(app_id=app_selected)

    # Новый блок кода! Список месяцев с расчетом оплат
    monthes_list = []
    for it in items:
        pay = Pay.objects.filter(item=it.pk)
        for one in pay:
            if calendar.month_name[int(one.month)] not in monthes_list:
                monthes_list.append(calendar.month_name[int(one.month)]) # Конец нового блока кода!

    for it in items:
        try:
            pay = Pay.objects.filter(item=it.pk, month=date.month).first()
            if pay:
                if not pay.item.is_counter in ['day', 'night']:
                    pay.debt = round((pay.topay - pay.payed), 2)
                else:
                    pay.debt = 0
                pay.save()
                pay_list.append(pay)
        except:
            pass

    if request.method == "POST":
        form = PayedForm(request.POST)
        if form.is_valid():
            try:
                pay = Pay.objects.get(pk=pay_selected)
                pay.payed = form.cleaned_data['payed']
                pay.debt = round((pay.topay - pay.payed), 2)
                pay.save()
                pay_selected = 0
                return redirect('pay', app_selected, pay_selected)
            except:
                pass
        else:
            pass
    else:
        try:
            pay = Pay.objects.get(pk=pay_selected)
            if pay.payed:
                form = PayedForm(initial={'payed': pay.payed})
            else:
                form = PayedForm(initial={'payed': pay.topay})
        except:
            form = PayedForm()

    total = dict(topay=0, payed=0, debt=0)
    if not pay_list:
        obj = 'Сейчас тут нет записей'
    else:
        for pay in pay_list:
            if not pay.item.is_counter in ['day', 'night']:
                total['topay'] += round(pay.topay, 2)
                total['payed'] += round(pay.payed, 2)
                total['debt'] += round(pay.debt, 2)
        if pay_selected == 0:
            msg_add(ap, 'Для ввода оплаты нажмите на наименование вида оплаты в таблице', 'Pay-Enter')
        else:
            clean_msgs('Pay-Enter')

    context = {'title': 'Расчет для оплаты по: ', 'menu': menu, 'submenu': submenu, 'obj': obj, 'msgs': msgs,
               'ap': ap, 'app_selected': app_selected, 'pay_selected': pay_selected, 'pay_list': pay_list,
               'total': total, 'date': date, 'monthes_list': monthes_list, 'form': form}
    return render(request, 'compay/pay.html', context)


# Новый блок кода проверки конфигурации
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
                        msgs.append(dict(key=str(b) + '/' + str(c), text='Вам необходимо задать начальные '
                                                                         'показания счетчиков',
                                         description='config_item'))
                    else:
                        a.is_counter = ap.__dict__[conf[el]]
                        a.save()
                        if a.is_counter == 'counter':
                            msgs.append(dict(key=a, text='Вам необходимо задать начальные показания счетчиков',
                                             description='config_item'))
                else:
                    a.is_counter = ap.__dict__[conf[el]]
                    a.save()
                    if a.is_counter == 'counter':
                        msgs.append(dict(key=a, text='Вам необходимо задать начальные показания счетчиков',
                                         description='config_item'))
            else:
                a.save()

    else:  # Проверяем есть ли отсутствующие предметы
        for el in lst:
            exist = False
            for item in items:
                if item.item_name == el:
                    if el == 'electricity':     #Начало нового блока! Проверка конфигурации
                        if item.is_counter in ['day', 'night', 'total'] and ap.el_night:
                            exist = True
                            if not item.active:
                                item.active = True
                                item.save()
                        elif item.is_counter == ap.__dict__[conf[el]] and not ap.el_night:
                            exist = True
                            if not item.active:
                                item.active = True
                                item.save()
                        else:
                            item.active = False
                            item.save()  # item.помеить_как_неактивный
                    elif item.is_counter == ap.__dict__[conf[el]]:
                        exist = True
                        if not item.active:
                            item.active = True
                            item.save()
                    else:
                        item.active = False
                        item.save()  # item.помеить_как_неактивный       #Конец нового блока! Проверка конфигурации
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


# ПРОВЕРИТЬ тариф от месяца!!!
def check_and_calculation(app_selected, month_selected):
    global msgs, month
    lst_template = ['electricity', 'water', 'gas', 'kv', 'tbo', 'domofon', 'inet', 'other']
    lst = []
    summary = 0
    ap = Appartment.objects.get(id=app_selected)
    items = Item.objects.filter(app=ap, active=True)
    first = items.first()

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
                tarifs = Tarif.objects.filter(item=item.id).exclude(created__month__gt=month).order_by('-created')[:3]
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
                                sum = round(tarif.value * (counter.value - counter.previous), 2)
                                sum_str = f'{counter.value - counter.previous} {counter.unit} / ({counter.value} - ' \
                                          f'{counter.previous}){counter.unit} * {tarif.value}{tarif.unit} = {sum}руб'
                                try:
                                    pay = Pay.objects.filter(item=item, month=month_selected).first()
                                    pay.topay = sum
                                    pay.calculation = sum_str
                                except:
                                    pay = Pay(topay=sum, month=month_selected, item=item, calculation=sum_str)
                                    # Добавить примечание с данными
                                pay.save()
                                summary += pay.topay
                                if item.item_name == 'electricity' and item.is_counter == 'day':
                                    topay_day = pay.topay
                                elif item.item_name == 'electricity' and item.is_counter == 'night':
                                    topay_night = pay.topay
                            else:
                                for t in tarifs:
                                    if t.el_counter_discrete == '0-150':
                                        t0_150 = t.value
                                    elif t.el_counter_discrete == '150-600':
                                        t150_600 = t.value
                                    elif t.el_counter_discrete == '600+':
                                        t600 = t.value
                                dif = counter.value - counter.previous
                                if dif > 150:
                                    if dif > 600:
                                        sum = round((150 * t0_150 + 600 * t150_600 + (dif - 600) * t600),2)
                                        sum_str = f'{counter.value - counter.previous} {counter.unit} / 150 * {t0_150} + 600 * {t150_600} + ({counter.value} - {counter.previous} - 600) * {t600} = {str(sum)}руб'
                                    else:
                                        sum = round((150 * t0_150 + (dif - 150) * t150_600), 2)
                                        sum_str = f'{counter.value - counter.previous} {counter.unit} / 150 * {str(t0_150)} + ({counter.value} - {counter.previous} - 150) * {t150_600} = {sum}руб'
                                else:
                                    sum = round(dif * t0_150, 2)
                                    sum_str = f'{counter.value - counter.previous} {counter.unit} / ({counter.value} - {counter.previous}) * {t0_150} = {sum}руб'
                                try:
                                    pay = Pay.objects.filter(item=item, month=month_selected).first()
                                    pay.topay = sum
                                    pay.calculation = sum_str
                                except:
                                    pay = Pay(topay=sum, calculation=sum_str, month=month_selected, item=item)
                                    # Добавить примечание с данными
                                pay.save()
                                summary += pay.topay
                                if item.item_name == 'electricity' and item.is_counter == 'day':
                                    topay_day = pay.topay
                                elif item.item_name == 'electricity' and item.is_counter == 'night':
                                    topay_night = pay.topay
                elif item.is_counter == 'tarif':
                    if ok:
                        try:
                            pay = Pay.objects.filter(item=item, month=month_selected).first()
                            pay.topay = tarif.value
                            pay.calculation = f'тариф - {tarif.value}'
                        except:
                            pay = Pay(topay=tarif.value, calculation=f'тариф - {tarif.value}',
                                      month=month_selected, item=item)
                        pay.save()
                        summary += pay.topay

    if 'electricity' in lst:
        for item in items:
            if item.item_name == 'electricity':
                if item.is_counter == 'total':
                    try:
                        pay = Pay.objects.filter(item=item, month=month_selected).first()
                        pay.topay = (topay_night + topay_day)
                        pay.calculation = f'день: {topay_day}{pay.unit} + ночь: {topay_night}{pay.unit} = ' \
                                          f'{topay_night + topay_day}{pay.unit}'
                    except:
                        pay = Pay(topay=(topay_night + topay_day),
                                  calculation=f'день: {topay_day}руб + ночь: {topay_night}руб = '
                                              f'{topay_night + topay_day}руб', month=month_selected, item=item)
                    pay.save()
    try:
        pay_selected = Pay.objects.filter(item=first, month=month_selected).first().pk
    except:
        pay_selected = 0
    return round(summary, 2), pay_selected


def count_payed_and_debts(app_selected, month_selected):
    global msgs, date
    lst_template = ['counter', 'tarif', 'total']
    payed_total = 0
    debts_total = 0
    ap = Appartment.objects.get(id=app_selected)
    items = Item.objects.filter(app=ap, active=True)

    for it in items:
        if it.is_counter in lst_template:
            pay = Pay.objects.filter(item=it, month=month_selected).first()
            if pay:
                payed_total += pay.payed
                debts_total += pay.debt

    return round(payed_total, 2), round(debts_total, 2)


def clean_msgs(msg_to_clean=None):
    global msgs
    msgs_clean_list = ['Error']
    msgs_clean_list.append(msg_to_clean)

    for i in range(3):
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


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'compay/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'compay/login.html'

    def get_context_data(self, **kwargs):
        context = super(LoginUser, self).get_context_data(**kwargs)
        context['title'] = 'Для использования приложения Вам необходимо авторизоваться'
        return context

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')

#adMin5881342