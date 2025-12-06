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

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def transaction_specific_manager(request, id):

    try:
        transaction = Transaction.objects.get(pk=id)
    except Transaction.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # Obtendo uma transação específica
    if request.method == 'GET':
        transaction_serializer = TransactionSerializer(transaction)
        return Response(transaction_serializer.data, status=status.HTTP_200_OK)
    
    # Atualizando uma transação específica
    if request.method == 'PUT' or request.method == 'PATCH':
        updated_data = request.data

        if request.method == 'PUT':         # Atualização completa
            transaction_serializer = TransactionSerializer(transaction, data=updated_data)
        elif request.method == 'PATCH':     # Atualiação parcial
            transaction_serializer = TransactionSerializer(transaction, data=updated_data, partial=True)

        if transaction_serializer.is_valid():
            transaction_serializer.save()
            return Response(transaction_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(transaction_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    # Deletando uma transação específica
    if request.method == 'DELETE':
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def transactions_summary(request):

    if request.method != 'GET':
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    transactions = Transaction.objects.all()

    total_income = transactions.filter(type=Transaction.TransactionType.INCOME).sum(t.amount for t in transactions)
    total_expense = transactions.filter(type=Transaction.TransactionType.EXPENSE).sum(t.amount for t in transactions)
    net_balance = total_income - total_expense

    summary = {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": net_balance
    }

    return Response(summary, status=status.HTTP_200_OK)