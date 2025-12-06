from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Transaction

class TransactionTests(APITestCase):

    # Configurações iniciais ants de rodar os testes
    def setUp(self):

        # Transação de exemplo de income
        self.transaction_data_income = {
            "description": "Salário",
            "amount": "5000.00",
            "type": "income",
            "date": "2023-12-01"
        }

        # Transação de exemplo de expense
        self.transaction_data_expense = {
            "description": "Aluguel",
            "amount": "1200.50",
            "type": "expense",
            "date": "2023-12-05"
        }



    # --- ===================  TESTE 1: POST  =================== --- 
    def test_create_transaction_sucess(self):
        """
        Testa a criação de uma nova transação via POST (espera-se sucesso).
        """
        url = reverse('create_list')
        response = self.client.post(url, self.transaction_data_income, format='json')
        
        # Verifica se deu 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Verifica se agora tem 1 transação no banco
        self.assertEqual(Transaction.objects.count(), 1)

        transaction = response.data['results']

        # Verifica se o nome salvo é o mesmo que foi enviado
        self.assertEqual(transaction.description, self.transaction_data_income.description)
        # Verifica se o amount salvo é o mesmo que foi enviado
        self.assertEqual(transaction.amount, self.transaction_data_income.amount)
        # Verifica se o type salvo é o mesmo que foi enviado
        self.assertEqual(transaction.type, self.transaction_data_income.type)
        # Verifica se a date salvo é o mesmo que foi enviado
        self.assertEqual(transaction.date, self.transaction_data_income.date)



    # --- ===================  TESTE 2: POST  =================== --- 
    def test_create_transaction_fail(self):
        """
        Testa a criação de uma nova transação via POST (espera-se a falha).
        """

        # ------------ Testando valor negativo de amount --------------

        transaction_invalid = self.transaction_data_income
        transaction_invalid.amount = -100.00 # Valor inválido

        url = reverse('create_list')
        response = self.client.post(url, transaction_invalid, format='json')
        
        # Verifica se deu 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Verifica se nenhuma transação foi adicionada ao banco
        self.assertEqual(Transaction.objects.count(), 0)
        # Verifica se a mensagem de erro menciona o campo 'amount'
        self.assertIn('amount', response.data)


        # ------------ Testando campos obrigatórios --------------
        transaction_invalid = {
            "description": "",
            "amount": "",
            "type": "",
            "date": ""
        }

        url = reverse('create_list')
        response = self.client.post(url, transaction_invalid, format='json')
        
        # Verifica se deu 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Verifica se nenhuma transação foi adicionada ao banco
        self.assertEqual(Transaction.objects.count(), 0)
        # Verifica se a mensagem de erro menciona o campo 'description'
        self.assertIn('description', response.data)
        # Verifica se a mensagem de erro menciona o campo 'amount'
        self.assertIn('amount', response.data)
        # Verifica se a mensagem de erro menciona o campo 'type'
        self.assertIn('type', response.data)
        # Verifica se a mensagem de erro menciona o campo 'date'
        self.assertIn('date', response.data)



    # --- ===================  TESTE 3: GET  =================== --- 
    def test_get_transaction(self):
        """
        Testa a obtenção de uma única transação.
        """

        # Primeiro, cria-se uma transação para garantir que há algo para buscar
        transaction = Transaction.objects.create(**self.transaction_data_income)
        transaction_id = transaction.id
        
        # Segundo, faz-se a requisição GET para a transação criada
        response = self.client.get(reverse('create_list', args=[transaction_id]))
        
        # Terceiro, verifica se deu 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)



    # --- ===================  TESTE 4: GET  =================== --- 
    def test_get_transaction(self):
        """
        Testa a obtenção de uma lista de transações.
        """

        # Primeiro, cria-se duas transações para garantir que há algo para buscar
        Transaction.objects.create(**self.transaction_data_income)
        Transaction.objects.create(**self.transaction_data_expense)
        
        # Segundo, faz-se a requisição GET para se obter a lista de transações
        response = self.client.get(reverse('create_list'))
        
        # Terceiro, verifica se deu 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Quarto verifica se retornou todas as transações criadas
        self.assertEqual(len(response.data['results']), 2)




    # --- ===================  TESTE 5: DELETE  =================== --- 
