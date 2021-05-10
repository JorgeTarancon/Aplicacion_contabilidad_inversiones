from django.contrib import admin
from self_index_app.models import Investor, Transactions

# Register your models here.
class InvestorAdmin(admin.ModelAdmin):
    list_display = ['investor_id', 'worth']

class TransactionsAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'investor', 'transaction_date', 'amount', 'asset_name']

admin.site.register(Investor, InvestorAdmin)
admin.site.register(Transactions, TransactionsAdmin)