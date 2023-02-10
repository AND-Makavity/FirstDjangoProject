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