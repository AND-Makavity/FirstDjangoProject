import datetime

from django import forms
from .models import *


class AppartmentForm(forms.ModelForm):
    # def __init__(self, args, kwargs):
    #     super().__init__(self, args, kwargs)
    #     self.fields['field_name'].empty_label = 'Не выбрано'

    class Meta:
        model = Appartment
        fields = ['name', 'adress', 'electricity', 'el_is_counter',
                  'el_counter_discrete', 'el_night', 'water', 'wat_is_counter',
                  'gas', 'gas_is_counter', 'kv', 'tbo', 'domofon', 'inet', 'other']
        widgets = {
            'adress': forms.TextInput(attrs={'size': '50'}),
            'name': forms.TextInput(attrs={'class': 'form-input'})
        }


class AppartmentEditForm(forms.ModelForm):
    # def __init__(self, args, kwargs):
    #     super().__init__(self, args, kwargs)
    #     self.fields['field_name'].empty_label = 'Не выбрано'

    class Meta:
        model = Appartment
        fields = ['adress', 'electricity', 'el_is_counter',
                  'el_counter_discrete', 'el_night', 'water', 'wat_is_counter',
                  'gas', 'gas_is_counter', 'kv', 'tbo', 'domofon', 'inet', 'other']
        widgets = {
            'adress': forms.TextInput(attrs={'size': '50'}),
        }


class CounterForm(forms.ModelForm):
    class Meta:
        model = Counter
        fields = ['value']
        # exclude = ('item',)
        widgets = {}


class TarifForm(forms.ModelForm):
    class Meta:
        model = Tarif
        fields = ['value']
        # exclude = ('item',)
        widgets = {}


class InfoForm(forms.ModelForm):
    class Meta:
        model = Info
        fields = '__all__'
        exclude = ('created', 'app', 'item')


class MonthForm(forms.Form):
    MONTHES = {'1': 'Январь', '2': 'Февраль', '3': 'Март', '4': 'Апрель', '5': 'Май', '6': 'Июнь',
               '7': 'Июль', '8': 'Август', '9': 'Сентябрь', '10': 'Октябрь', '11': 'Ноябрь', '12': 'Декабрь'}

    date = forms.DateField(widget=forms.SelectDateWidget(months=MONTHES), label='',
                           initial=datetime.date.today, )
