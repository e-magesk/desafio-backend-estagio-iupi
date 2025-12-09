from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

from django.db.models import Sum
from .models import Transaction
from .serializers import TransactionSerializer

import json

@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def transactions_manager(request):
    """
    Gerencia a criação e listagem das transações.

    Métodos suportados:
    - **POST**: Cria uma nova transação.
        - *Campos obrigatórios*: `amount`, `type`, `date`.
        - O usuário é atribuído automaticamente com base no token de autenticação.

    - **GET**: Retorna a lista de transações do usuário logado.
        - *Filtros opcionais na URL:*
            - `?type=income` ou `?type=expense` (Filtra por tipo)
            - `?description=texto` (Busca parcial na descrição)
            - `?page=N` (Paginação)
            - `?order_by=field` ('date', '-date', 'amount', '-amount')
    """

    # Criação da transição
    if request.method == 'POST':

        new_transaction = request.data
        transaction_serializer = TransactionSerializer(data=new_transaction)

        if transaction_serializer.is_valid():
            transaction_serializer.save(user=request.user)
            return Response(transaction_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(transaction_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    # Obtendo as transações requisitadas
    if request.method == 'GET':

        # Obtém todas as transações
        transactions = Transaction.objects.filter(user=request.user).order_by('id')

        
        # Recolhe as informações de filtro (se houver)
        transaction_description = request.query_params.get('description', None)
        transaction_type = request.query_params.get('type', None)

        # Filtra pela descrição, se fornecida
        if transaction_description is not None:
            transactions = transactions.filter(description__contains=transaction_description)

        # Filtra pelo tipo, se fornecido
        if transaction_type is not None:
            transactions = transactions.filter(type=transaction_type.strip())

        # Ordena os resultados, se solicitado
        allowed_order_fields = ['date', '-date', 'amount', '-amount']
        order_by = request.query_params.get('order_by', None)
        if order_by in allowed_order_fields:
            transactions = transactions.order_by(order_by)

        # Realizando a paginação
        paginator = PageNumberPagination()
        result_transactions = paginator.paginate_queryset(transactions, request)

        transaction_serializers = TransactionSerializer(result_transactions, many=True)

        # Devolve a resposta paginada e já (por padrão) com o status 200 OK
        return paginator.get_paginated_response(transaction_serializers.data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def transaction_specific_manager(request, id):
    """
    Gerencia uma transação específica identificada pelo ID 
    (apenas o usuário que criou a transação pode fazer isso).

    Regras de Segurança:
    - Retorna 404 se a transação não existir ou pertencer a outro usuário.

    Métodos suportados:
    - **GET**: Visualiza os detalhes da transação.
    - **PUT**: Atualiza a transação inteira (todos os campos são validados).
    - **PATCH**: Atualiza parcialmente.
    - **DELETE**: Remove a transação permanentemente.
    """

    try:
        transaction = Transaction.objects.get(pk=id, user=request.user)
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
@permission_classes([IsAuthenticated])
def transactions_summary(request):
    """
    Calcula o resumo financeiro total do usuário.

    Realiza a soma agregada diretamente no banco de dados para performance.

    Retorna um JSON com:
    - `total_income`: Soma de todas as entradas.
    - `total_expense`: Soma de todas as saídas.
    - `balance`: Saldo final (Entradas - Saídas).
    """

    if request.method != 'GET':
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    transactions = Transaction.objects.filter(user=request.user)

    # Recolhe as informações de filtro (se houver)
    transaction_description = request.query_params.get('description', None)

    # Filtra pela descrição, se fornecida
    if transaction_description is not None:
        transactions = transactions.filter(description__contains=transaction_description)

    # Ordena os resultados, se solicitado
    allowed_order_fields = ['date', '-date', 'amount', '-amount']
    order_by = request.query_params.get('order_by', None)
    if order_by in allowed_order_fields:
        transactions = transactions.order_by(order_by)

    total_income = transactions.filter(type=Transaction.TransactionType.INCOME).aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = transactions.filter(type=Transaction.TransactionType.EXPENSE).aggregate(Sum('amount'))['amount__sum'] or 0
    net_balance = total_income - total_expense

    summary = {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": net_balance
    }

    return Response(summary, status=status.HTTP_200_OK)