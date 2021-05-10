from django.shortcuts import render
from rest_framework import viewsets
from .serializers import InvestorSerializer, TransactionsSerializer
from .models import Investor, Transactions
# Create your views here.

class InvestorView(viewsets.ModelViewSet):
    serializer_class = InvestorSerializer
    queryset = Investor.objects.all()

class TransactionView(viewsets.ModelViewSet):
    serializer_class = TransactionsSerializer
    queryset = Transactions.objects.all()