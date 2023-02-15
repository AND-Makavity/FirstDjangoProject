from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('add_app', add_app, name='add_app'),
    path('item/<int:app_selected>/<int:item_selected>/', item, name='item'),
    path('config_app/<int:app_selected>/', config_app, name='config_app'),
    path('app/<int:app_selected>/', app, name='app'),
    path('enter_counters/<int:app_selected>/', enter_counters, name='enter_counters'),
    path('enter_tarifs/<int:app_selected>/', enter_tarifs, name='enter_tarifs'),
    path('tarifs/<int:app_selected>/', tarifs, name='tarifs'),
    path('info/<int:app_selected>/', info, name='info'),
    path('tarif/<int:app_selected>/<int:item_selected>/', tarif, name='tarif'),
    path('counter/<int:app_selected>/<int:item_selected>/', counter, name='counter'),
    path('enter_info/<int:app_selected>/<int:item_selected>/', enter_info, name='enter_info'),
    path('counters/<int:app_selected>/', counters, name='counters'),
    path('pay/<int:app_selected>/<int:pay_selected>/', pay, name='pay'),
    path('pay/<int:app_selected>/', pay, name='pay'),
    path('pay_history/<int:app_selected>/<int:item_selected>/', pay_history, name='pay_history'),
    path('pay_history/<int:app_selected>/', pay_history, name='pay_history')
    ]