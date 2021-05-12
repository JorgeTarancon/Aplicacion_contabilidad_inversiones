from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import InvestorSerializer, TransactionsSerializer
from .models import Investor, Transactions
# Create your views here.
@api_view(['GET'])
def investors_list(request):
    investors = Investor.objects.all()
    investors_serializer = InvestorSerializer(investors, many=True)
    return Response(investors_serializer.data)

@api_view(['GET','POST'])
def add_transaction(request):
    if request.method == "GET":
        transactions = Transactions.objects.all()
        transactions_serializer = TransactionsSerializer(transactions, many=True)
        return Response(transactions_serializer.data)
    elif request.method == "POST":
        transactions_serializer = TransactionsSerializer(data=request.data)
        return Response(transactions_serializer.data, status=status.HTTP_400_BAD_REQUEST)
        if transactions_serializer.is_valid():
            transactions_serializer.save()
            return Response(transactions_serializer.data, status=status.HTTP_201_CREATED)

        return Response(transactions_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class InvestorView(APIView):
#     def get(self, request):
#         investors = Investor.objects.all()
#         investors_serializer = InvestorSerializer(investors, many=True)
#         return Response(investors_serializer.data)

# class TransactionView(APIView):
#     serializer_class = TransactionsSerializer
#     queryset = Transactions.objects.all()

#     def get(self, request):
#         transactions = Transactions.objects.all()
#         transactions_serializer = TransactionsSerializer(transactions, many=True)
#         return Response(transactions_serializer)

#     def post(self, request, format=None):
#         transactions_serializer = TransactionsSerializer(data=request.data)
#         return Response(transactions_serializer.data, status=status.HTTP_400_BAD_REQUEST)
#         if transactions_serializer.is_valid():
#             transactions_serializer.save()
#             return Response(transactions_serializer.data, status=status.HTTP_201_CREATED)

#         return Response(transactions_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class InvestorView(viewsets.ModelViewSet):
#     serializer_class = InvestorSerializer
#     queryset = Investor.objects.all()

#     def get(self, request):
#         investors = Investor.objects.all()
#         investors_serializer = InvestorSerializer(investors, many=True)
#         return Response(investors_serializer)

# class TransactionView(viewsets.ModelViewSet):
#     serializer_class = TransactionsSerializer
#     queryset = Transactions.objects.all()

#     def get(self, request):
#         transactions = Transactions.objects.all()
#         transactions_serializer = TransactionsSerializer(transactions, many=True)
#         return Response(transactions_serializer)

#     def post(self, request, format=None):
#         transactions_serializer = TransactionsSerializer(data=request.data)
#         return Response(transactions_serializer.data, status=status.HTTP_400_BAD_REQUEST)
#         if transactions_serializer.is_valid():
#             transactions_serializer.save()
#             return Response(transactions_serializer.data, status=status.HTTP_201_CREATED)

#         return Response(transactions_serializer.errors, status=status.HTTP_400_BAD_REQUEST)