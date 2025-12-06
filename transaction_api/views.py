from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Transaction
from .serializers import TransactionSerializer

import json

@api_view(['POST', 'GET'])
def transactions_manager(request):

    # Criação da transição
    if request.method == 'POST':

        new_transaction = request.data
        transaction_serializer = TransactionSerializer(data=new_transaction)

        if transaction_serializer.is_valid():
            transaction_serializer.save()
            return Response(transaction_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(transaction_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    # Obtendo todas as transações
    if request.method == 'GET':

        transactions = Transaction.objects.all()
        transaction_serializers = TransactionSerializer(transactions, many=True)

        return Response(transaction_serializers.data, status=status.HTTP_200_OK)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)