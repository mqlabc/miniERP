from django.contrib import admin
from . import models
from debt.models import Debt

# Register your models here.
class CompanyAdmin(admin.ModelAdmin):
    search_fields = ['comp_name']
    fields = ['comp_name', 'comp_addr', 'comp_legal_person', 'comp_agent_person', 'comp_phone','comp_mail','comp_bank_name','comp_bank_account','comp_tax_account','comp_contact_person']
    list_display = ('comp_name', 'comp_addr', 'comp_legal_person', 'comp_agent_person', 'comp_phone','comp_mail','comp_bank_name','comp_bank_account','comp_tax_account','comp_contact_person')

class DebtInline(admin.StackedInline):
    model = Debt
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    search_fields = ['buyer__comp_name']
    fields = ['buyer', 'seller','mat_set', 'order_place', 'order_code', 'order_date','deposit_percent']
    list_display = ('buyer', 'seller', 'order_place', 'order_code', 'order_date','deposit_percent')
    inlines = [DebtInline]

admin.site.register(models.Company, CompanyAdmin)
admin.site.register(models.Order, OrderAdmin)
