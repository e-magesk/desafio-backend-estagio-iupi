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
            "amount": 5000.00,
            "type": "income",
            "date": "2023-12-01"
        }

        # Transação de exemplo de expense
        self.transaction_data_expense = {
            "description": "Aluguel",
            "amount": 1200.50,
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

        transaction = response.data

        # Verifica se o nome salvo é o mesmo que foi enviado
        self.assertEqual(transaction['description'], self.transaction_data_income['description'])
        # Verifica se o amount salvo é o mesmo que foi enviado
        self.assertEqual(float(transaction['amount']), self.transaction_data_income['amount'])
        # Verifica se o type salvo é o mesmo que foi enviado
        self.assertEqual(transaction['type'], self.transaction_data_income['type'])
        # Verifica se a date salvo é o mesmo que foi enviado
        self.assertEqual(transaction['date'], self.transaction_data_income['date'])



    # --- ===================  TESTE 2: POST  =================== --- 
    def test_create_transaction_fail(self):
        """
        Testa a criação de uma nova transação via POST (espera-se a falha).
        """

        # ------------ Testando valor negativo de amount --------------

        transaction_invalid = self.transaction_data_income
        transaction_invalid['amount'] = -100.00 # Valor inválido

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
    def test_get_transactions(self):
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
        self.assertEqual(response.data['count'], 2)



    # --- ===================  TESTE 4: GET  =================== --- 
    def test_get_transaction(self):
        """
        Testa a obtenção de uma única transação.
        """

        # Primeiro, cria-se uma transação para garantir que há algo para buscar
        transaction = Transaction.objects.create(**self.transaction_data_income)
        transaction_id = transaction.id

        # Segundo, faz-se a requisição GET para a transação criada
        response = self.client.get(reverse('retrieve_update_delete', args=[transaction_id]))
        
        # Terceiro, verifica se deu 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)



    # # --- ===================  TESTE 5: PATCH  =================== --- 
    def test_update_patch_transaction(self):
        """
        Testa a atualização de uma transação via PATCH.
        """

        # Primeiro, cria-se uma transação para garantir que há algo para atualizar
        transaction = Transaction.objects.create(**self.transaction_data_income)
        transaction_id = transaction.id

        # Dados para atualização
        updated_data = {
            "description": "Salário atualizado",
            "amount": 5500.00
        }
        
        # Segundo, faz-se a requisição PATCH para atualizar a transação criada
        response = self.client.patch(reverse('retrieve_update_delete', args=[transaction_id]), updated_data, format='json')
        
        # Terceiro, verifica se deu 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Quarto, verifica se os dados foram atualizados corretamente
        transaction.refresh_from_db()
        self.assertEqual(transaction.description, updated_data['description'])
        self.assertEqual(transaction.amount, updated_data['amount'])



    # # --- ===================  TESTE 6: PUT  =================== --- 
    def test_update_put_transaction(self):
            """
            Testa a atualização de uma transação via PUT.
            """

            # Primeiro, cria-se uma transação para garantir que há algo para atualizar
            transaction = Transaction.objects.create(**self.transaction_data_income)
            transaction_id = transaction.id

            # Dados para atualização completa
            updated_data = {
                "description": "Salário",
                "amount": 60000.00,
                "type": "income",
                "date": "2023-12-31"
            }
            
            # Segundo, faz-se a requisição PUT para atualizar a transação criada
            response = self.client.put(reverse('retrieve_update_delete', args=[transaction_id]), updated_data, format='json')

            # Terceiro, verifica se deu 200 OK
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # Quarto, verifica se os dados foram atualizados corretamente
            transaction.refresh_from_db()
            self.assertEqual(transaction.description, updated_data['description'])
            self.assertEqual(transaction.amount, updated_data['amount'])
            self.assertEqual(transaction.type, updated_data['type'])
            self.assertEqual(str(transaction.date), updated_data['date'])

            # Verificação extra: o id precisa permanecer o mesmo
            self.assertEqual(transaction.id, transaction_id)



    # # --- ===================  TESTE 7: DELETE  =================== ---
    def test_delete_transaction(self):
        """
        Testa a deleção de uma transação.
        """

        # Primeiro, cria-se uma transação para garantir que há algo para deletar
        transaction = Transaction.objects.create(**self.transaction_data_income)
        transaction_id = transaction.id
        
        # Segundo, faz-se a requisição DELETE para deletar a transação criada
        response = self.client.delete(reverse('retrieve_update_delete', args=[transaction_id]))
        
        # Terceiro, verifica se deu 204 No Content
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)



    # # --- ===================  TESTE 8: SUMMARY  =================== ---
    def test_transactions_summary(self):
        """
        Testa o resumo das transações.
        """

        # Primeiro, cria-se uma transação de income e uma de expense
        Transaction.objects.create(**self.transaction_data_income)
        Transaction.objects.create(**self.transaction_data_income)

        Transaction.objects.create(**self.transaction_data_expense)
        Transaction.objects.create(**self.transaction_data_expense)

        # Segundo, faz-se a requisição GET para obter o resumo
        response = self.client.get(reverse('summary'))

        # Terceiro, verifica se deu 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Quarto, verifica se os valores do resumo estão corretos
        expected_summary = {
            "total_income": self.transaction_data_income['amount'] * 2,
            "total_expense": self.transaction_data_expense['amount'] * 2,
            "net_balance": (self.transaction_data_income['amount'] * 2) - (self.transaction_data_expense['amount'] * 2)
        }

        self.assertEqual(response.data, expected_summary)

