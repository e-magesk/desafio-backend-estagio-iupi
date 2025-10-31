# 📖 Desafio de Estágio Backend (API REST) - IUPI

Olá, candidato\! Que bom ter você aqui. Este desafio foi criado para avaliarmos seus conhecimentos fundamentais na construção de APIs REST, modelagem de dados e boas práticas de desenvolvimento backend.

## Stack Tecnológica

  * **Nossa Stack (Preferencial):** Na IUPI, nossa stack principal de backend é **Python** com **Django** e **Django REST Framework (DRF)**. Gostaríamos muito de ver seu desafio construído com essas ferramentas.
  * **Outras Stacks:** Se você ainda não domina Django, mas é fera em outra stack (Node.js, Flask/FastAPI, Spring Boot, etc.), sinta-se à vontade para usá-la. Valorizamos bons fundamentos de programação acima de tudo.
  * **Banco de Dados:** Recomendamos o uso de **SQLite**. É um banco de dados leve, baseado em arquivo, que não exige um servidor separado e foca na lógica da API.

-----

## 🎯 O Desafio

Sua missão é construir a API REST para o nosso "Controle de Despesas". Esta API será a fonte da verdade para as transações financeiras e deve permitir que um frontend crie, liste, edite e delete essas transações.

### O Modelo de Dados: `Transaction`

O objeto principal da sua API deve ter a seguinte estrutura:

  * `id` (string ou número): Identificador único (gerado automaticamente).
  * `description` (string): Descrição da transação (ex: "Salário", "Aluguel").
  * `amount` (número): O valor da transação. **Deve ser sempre um número positivo.**
  * `type` (string): O tipo de transação. Deve ser `income` (entrada) ou `expense` (saída).
  * `date` (string ou data): A data da transação (formato `YYYY-MM-DD`).

-----

## ✅ Requisitos Funcionais (Endpoints)

Sua API deve expor os seguintes endpoints (o CRUD completo).

### 1\. Criar Transação

  * **Endpoint:** `POST /transactions/`
  * **Request Body (JSON):** Um objeto contendo `description`, `amount`, `type`, e `date`.
  * **Validação (Obrigatório):**
      * Todos os campos são obrigatórios.
      * `amount` deve ser um número maior que zero.
      * `type` deve ser obrigatoriamente `income` ou `expense`.
      * Se a validação falhar, a API deve retornar um status `400 Bad Request` com uma mensagem de erro clara.
  * **Resposta (Sucesso):**
      * Status `201 Created`
      * Body: O objeto da transação recém-criada, incluindo seu `id`.

### 2\. Listar Transações (com Filtros)

  * **Endpoint:** `GET /transactions/`
  * **Query Params (Filtros):**
      * `?description=...`: Filtrar por descrição (busca parcial, "case-insensitive". Ex: `desc=sal` deve encontrar "Salário").
      * `?type=...`: Filtrar por tipo (ex: `?type=income` ou `?type=expense`).
      * *Os filtros devem ser combináveis.*
  * Exemplo de chamada (Query Params completo):
      * Se o candidato quiser encontrar todas as transações do tipo "saída" (expense) que contenham a palavra "café" na descrição, a URL completa da requisição GET ficaria assim:
        `GET http://localhost:8000/transactions/?type=expense&description=cafe`
  * **Resposta (Sucesso):**
      * Status `200 OK`
      * Body: Um array com as transações que correspondem aos filtros.


### 3\. Obter Transação Específica

  * **Endpoint:** `GET /transactions/:id/`
  * **Validação:**
      * Se a transação com o `id` informado não existir, retorne um status `404 Not Found`.
  * **Resposta (Sucesso):**
      * Status `200 OK`
      * Body: O objeto único da transação.

### 4\. Atualizar Transação

  * **Endpoint:** `PUT /transactions/:id/` (ou `PATCH`)
  * **Request Body (JSON):** Os campos que devem ser atualizados.
  * **Validação:** Aplicam-se as mesmas regras da criação.
  * **Resposta (Sucesso):**
      * Status `200 OK`
      * Body: O objeto da transação *atualizado*.

### 5\. Deletar Transação

  * **Endpoint:** `DELETE /transactions/:id/`
  * **Resposta (Sucesso):**
      * Status `2_4 No Content`
      * Body: Vazio.

### 6\. Obter Resumo (Desafio de Lógica)

  * **Endpoint:** `GET /summary/`
  * **Lógica:** Este é um endpoint customizado que exigirá lógica de agregação de dados.
  * **Resposta (Sucesso):**
      * Status `200 OK`
      * Body (JSON):
    <!-- end list -->
    ```json
    {
        "total_income": "15000.00",  // Soma de todos os 'income'
        "total_expense": "4500.00", // Soma de todos os 'expense'
        "net_balance": "10500.00"   // (income - expense)
    }
    ```

-----
## 💎 Requisitos de Qualidade de Código

* **1. Padrões de Nomenclatura:**
    * **Se usar nossa stack (Python/Django):**
        * Use `snake_case` para variáveis, funções, métodos e nomes de arquivos.
        * Use `PascalCase` para classes.
    * **Se usar outra stack:** Siga as convenções de nomenclatura dessa linguagem. O importante é a consistência.
        * **Exemplo (JavaScript/Node.js):** Use `camelCase` para variáveis e funções, `PascalCase` para classes e `kebab-case` para nomes de arquivos.
        * **Exemplo (Java/Spring):** Use `camelCase` para variáveis e métodos, e `PascalCase` para classes e interfaces.

* **2. Documentação de Código (Comentários):**
    * Use `docstrings` (para Python) ou o formato de documentação padrão da sua linguagem (JSDoc, JavaDoc, etc.) para documentar suas classes e funções/métodos principais.

* **3. Estrutura de Projeto:**
    * Você deve organizar seu código de forma lógica e escalável. A forma como você estrutura seus arquivos e módulos (separação de responsabilidades) será avaliada.

* **4. `.gitignore`:**
    * Configure seu `.gitignore` corretamente para ignorar arquivos desnecessários (ex: `__pycache__`, `node_modules/`, `.env`, `db.sqlite3`, `venv/`).

-----

## ⭐ Requisitos Bônus (Opcional)

  * **Paginação:** Adicione paginação à sua lista de `GET /transactions/`.
  * **Testes Automatizados:** Escreva testes unitários para sua API usando o framework de testes do Django.
  * **Autenticação JWT:**
    * 1\.  Criar um endpoint `POST /login/` que retorna um token (JWT).
    * 2\.  Proteger os endpoints de transações (só acessíveis com `Authorization: Bearer <token>`).
    * 3\.  A API deve retornar apenas transações do usuário autenticado.

-----

## 🚀 Como Testar sua API

Para testar os endpoints de uma API (enviar `POST`, `PUT`, etc.), você não usa o navegador. Recomendamos o uso de uma ferramenta como o **Postman** ou **Insomnia**. Elas facilitam o envio de requisições e a visualização das respostas.

## 📚 Materiais de Aprendizado (Pode consultar\!)
  * **Aprenda com vídeos**
    * [Como criar uma API em Django - Criando um CRUD - Aula Completa](https://youtu.be/Q2tEqNfgIXM?si=KBBw_cqHJ75b181a)

  * **Django (Fundamentos):**
      * [Guia de Instalação Rápida](https://docs.djangoproject.com/pt-br/5.2/intro/install/)
      * [Tutorial Oficial do Django](https://docs.djangoproject.com/pt-br/5.2/intro/tutorial01/)
      * [Documentação Oficial do Django](https://docs.djangoproject.com/pt-br/5.2/)
  * **Django REST Framework (Documentação):**
      * [Página Inicial da Documentação do DRF](https://www.django-rest-framework.org/)
      * [DRF - Serializers (Serialização)](https://www.django-rest-framework.org/tutorial/1-serialization/)
      * [DRF - ViewSets & Routers (Views)](https://www.django-rest-framework.org/api-guide/viewsets/)
      * [DRF - Filtering (Filtros)](https://www.django-rest-framework.org/api-guide/filtering/)
  * **Geral (Conceitos):**
      * [O que é uma API REST? (Guia da AWS)](https://aws.amazon.com/pt/what-is/restful-api/)
      * [HTTP Status Codes (MDN)](https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Status)
  * **Ferramentas de Teste de API:**
      * [O que é o Postman? (Guia para Iniciantes)](https://learning.postman.com/docs/getting-started/introduction/)
  * **Autenticação:**
      * [DRF Simple JWT (Biblioteca popular)](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
      * [DRF - Autenticação (Documentação)](https://www.django-rest-framework.org/api-guide/authentication/)

## 🚚 Como Entregar

1.  Faça um Fork deste repositório.
2.  Crie uma nova branch (ex: `meu-nome-desafio`).
3.  Faça seus commits.
4.  **IMPORTANTE:** Adicione ou atualize o `README.md` do seu projeto explicando:
      * A stack que você usou.
      * Como instalar as dependências.
      * Como preparar o banco de dados (rodar migrações, etc.).
      * Como rodar o projeto.
5.  Ao finalizar, abra um **Pull Request (PR)** do seu fork de volta para este repositório original.
6.  No corpo do PR, deixe comentários sobre suas decisões, dificuldades e o que você mais gostou.

Boa sorte\!
