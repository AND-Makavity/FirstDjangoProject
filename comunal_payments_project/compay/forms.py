from django import forms
from .models import *

class AppartmentForm(forms.ModelForm):

    # def __init__(self, args, kwargs):
    #     super().__init__(self, args, kwargs)
    #     self.fields['field_name'].empty_label = 'Не выбрано'

    class Meta:
        model = Appartment
        fields = ['name', 'adress', 'electricity', 'water', 'gas', 'tbo', 'domofon', 'kv', 'inet', 'other']
        widgets = {
            'adress': forms.TextInput(attrs={'class': 'form-input'}),
            'name': forms.TextInput(attrs={'class': 'form-input'})
        }


class AppartmentEditForm(forms.ModelForm):

    # def __init__(self, args, kwargs):
    #     super().__init__(self, args, kwargs)
    #     self.fields['field_name'].empty_label = 'Не выбрано'

    class Meta:
        model = Appartment
        fields = ['adress', 'electricity', 'water', 'gas', 'tbo', 'domofon', 'kv', 'inet', 'other']
        widgets = {
            'adress': forms.TextInput(attrs={'class': 'form-input'}),
        }


class ItemForm(forms.ModelForm):

    # def __init__(self, args, kwargs):
    #     super().__init__(self, args, kwargs)
    #     self.fields['app'].empty_label = 'Не выбрано'

    class Meta:
        model = Item
        fields = ['is_counter', 'day_night', 'discrete_tarif']
        widgets = {
            #'is_counter': forms.TextInput(attrs={'class': 'form-input'}),
            #'app': forms.TextInput(attrs={'class': 'form-input'}),
        }


class CounterForm(forms.ModelForm):

    class Meta:
        model = Counter
        fields = ['value']
        # exclude = ('item',)
        widgets = {}

