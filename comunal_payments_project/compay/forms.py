import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
        widgets = {
            'item_provider': forms.TextInput(attrs={'size': '42'}),
            'item_user_number': forms.TextInput(attrs={'size': '42'}),
            'item_comment': forms.Textarea(attrs={'size': '42', 'rows': '5'}),
        }


class MonthForm(forms.Form):
    MONTHES = {'1': 'Январь', '2': 'Февраль', '3': 'Март', '4': 'Апрель', '5': 'Май', '6': 'Июнь',
               '7': 'Июль', '8': 'Август', '9': 'Сентябрь', '10': 'Октябрь', '11': 'Ноябрь', '12': 'Декабрь'}

    date = forms.DateField(widget=forms.SelectDateWidget(months=MONTHES), label='',
                           initial=datetime.date.today, )


class PayedForm(forms.Form):
    payed = forms.FloatField(label='')


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-reg'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-reg'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-reg'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-reg'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-reg'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-reg'})
        }
