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
        

    # Obtendo as transações requisitadas
    if request.method == 'GET':

        # Obtém todas as transações
        transactions = Transaction.objects.all()
        
        # Recolhe as informações de filtro (se houver)
        transaction_description = request.query_params.get('description', None)
        transaction_type = request.query_params.get('type', None)

        # Filtra pela descrição, se fornecida
        if transaction_description is not None:
            transactions = transactions.filter(description__contains=transaction_description)

        # Filtra pelo tipo, se fornecido
        if transaction_type is not None:
            transactions = transactions.filter(type=transaction_type.strip())

        transaction_serializers = TransactionSerializer(transactions, many=True)

        return Response(transaction_serializers.data, status=status.HTTP_200_OK)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_transaction_by_id(request, id):

    if request.method != 'GET':
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    try:
        transaction = Transaction.objects.get(pk=id)
    except Transaction.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    transaction_serializer = TransactionSerializer(transaction)
    return Response(transaction_serializer.data, status=status.HTTP_200_OK)