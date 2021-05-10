from rest_framework import serializers
from .models import Investor, Transactions

class InvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investor
        fields = ('investor_id', 'worth')

class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ('transaction_id', 'investor', 'transaction_date', 'amount', 'asset_name')