from django.contrib import admin

from . import models

# Register your models here.
# 没注册不能修改
class DebtAdmin(admin.ModelAdmin):
    search_fields = ['buyer']
    # list_display = ('order.buyer', 'order.order_place', 'order.order_code', 'order.order_date', 'clear', 'last_date')
    list_display = ('order', 'clear', 'last_date')


admin.site.register(models.Debt, DebtAdmin)
