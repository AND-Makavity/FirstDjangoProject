from django.contrib import admin

from .models import *


class AppartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'adress', 'created', 'electricity', 'el_is_counter',
                    'el_counter_discrete', 'el_night', 'water', 'wat_is_counter',
                    'gas', 'gas_is_counter', 'kv', 'tbo', 'domofon', 'inet', 'other')
    list_display_links = ('id', 'name', )
    search_fields = ('name',)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'item_name', 'app', 'is_counter', 'created', 'active')
    list_display_links = ('id', 'item_name', )
    search_fields = ('item_name',)


class CounterAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'type', 'value', 'previous', 'created', 'updated')
    list_display_links = ('id', 'item', )
    search_fields = ('item',)


class TarifAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'type', 'value', 'el_counter_discrete', 'created')
    list_display_links = ('id', 'item', )
    search_fields = ('item',)


class InfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'item_provider', 'item_user_number', 'item_comment', 'created')
    list_display_links = ('id', 'item', )
    search_fields = ('item',)


class PayAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'topay', 'payed', 'debt', 'month', 'calculation', 'created', 'updated')
    list_display_links = ('id', 'item', )
    search_fields = ('item', 'id')


class PaySummaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'app', 'topay', 'payed', 'debt', 'debt_summary', 'debt_sum_before', 'month',
                    'comment', 'created', 'updated')
    list_display_links = ('id', 'app', )
    search_fields = ('item',)



admin.site.register(Appartment, AppartmentAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Tarif, TarifAdmin)
admin.site.register(Info, InfoAdmin)
admin.site.register(Counter, CounterAdmin)
admin.site.register(Pay, PayAdmin)
admin.site.register(PaySummary, PaySummaryAdmin)


