from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('add_app', add_app, name='add_app'),
    path('item/<int:app_selected>/<int:item_selected>/', item, name='item'),
    path('config_app/<int:app_selected>/', config_app, name='config_app'),
    path('config_app_item/<int:app_selected>/<int:item_selected>/', config_app_item, name='config_app_item'),
    path('app/<int:app_selected>/', app, name='app'),
    path('enter_counters/<int:app_selected>/', enter_counters, name='enter_counters'),
    path('counters/<int:app_selected>/', counters, name='counters')
    ]