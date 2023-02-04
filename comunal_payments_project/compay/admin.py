from django.contrib import admin

from .models import *


class AppartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'adress', 'created', 'electricity', 'water',
                    'gas', 'kv', 'tbo', 'domofon', 'inet', 'other')
    list_display_links = ('id', 'name', )
    search_fields = ('name',)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'item_name', 'app', 'is_counter', 'day_night', 'discrete_tarif', 'created')
    list_display_links = ('id', 'item_name', )
    search_fields = ('item_name',)


class CounterAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'type', 'value', 'previous', 'created')
    list_display_links = ('id', 'item', )
    search_fields = ('item',)


admin.site.register(Appartment, AppartmentAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Tarif)
admin.site.register(DiscreteConfiguration)
admin.site.register(Info)
admin.site.register(Counter, CounterAdmin)
admin.site.register(ToPay)
admin.site.register(Payed)
admin.site.register(Debts)

