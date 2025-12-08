# 📖 Desafio de Estágio Backend (API REST) - IUPI

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

## ⭐ Requisitos Bônus (Opcional)

  * **Paginação:** Adicione paginação à sua lista de `GET /transactions/`.
  * **Testes Automatizados:** Escreva testes unitários para sua API usando o framework de testes do Django.
  * **Autenticação JWT:**
    * 1\.  Criar um endpoint `POST /login/` que retorna um token (JWT).
    * 2\.  Proteger os endpoints de transações (só acessíveis com `Authorization: Bearer <token>`).
    * 3\.  A API deve retornar apenas transações do usuário autenticado.

-----

# 💰 Implementação API de Transações

## Tecnologias Utilizadas

* **Linguagem:** Python 3.12.9
* **Framework Web:** Django
* **API Toolkit:** Django REST Framework (DRF)
* **Autenticação:** JWT (SimpleJWT)
* **Banco de Dados:** SQLite

## ⚙️ Instalação e Configuração

Siga o passo a passo abaixo para rodar o projeto na sua máquina local.

### 1. Pré-requisitos
Certifique-se de ter o **Python** instalado na sua máquina.

### 2. Clonar o repositório e acessar a pasta
```bash
git clone <URL_DESTE_REPOSITORIO>
cd nome-da-pasta-do-projeto
```

### 3. Criar/Ativar o ambiente virtual
Abra o terminal na pasta raiz do projeto e execute:

Caso o ambiente virtual ainda não exista, `para criá-lo` execute:

```bash
python -m venv venv
```

`Para ativar` o ambiente virtual, execute:

**No Windows (Prompt)**

```bash
venv\Scripts\activate
```

**No Windows (PowerShell)**

```bash
.\venv\Scripts\Activate.ps1
```

**No Linux ou macOS**

```bash
source venv/bin/activate
```

### 4. Instalar dependências necessárias

Com o ambiente virtual ativado, instale as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

### 5. Preparando o banco de dados

O projeto utiliza SQLite. Você precisa criar as tabelas antes de rodar.

```bash
python manage.py makemigrations
python manage.py migrate
```

(Opcional) Se quiser criar um superusuário para acessar o admin, bastar roda o comando abaixo e seguir as instruções no terminal.

```bash
python manage.py createsuperuser
```
-----

## 🚀 Como Rodar o Projeto

Para iniciar o servidor de desenvolvimento:

```bash
python manage.py runserver
```

A API estará disponível em: `http://127.0.0.1:8000/`.

-----

## 🔑 Autenticação e Endpoints

Esta API utiliza **JSON Web Tokens (JWT)** para segurança.
Com exceção da rota de login, **todas** as outras rotas são protegidas e exigem autenticação.

### Como Autenticar

Para acessar os endpoints protegidos, você deve enviar o `token de acesso` no **Header** da requisição HTTP seguindo este padrão exato:

* **Key:** `Authorization`
* **Value:** `Bearer <seu_token_access_aqui>`

---

### 📡 Tabela de Endpoints

Abaixo estão as rotas disponíveis na API.

| Método | Endpoint | Acesso | Descrição |
| :--- | :--- | :--- | :--- |
| **POST** | `/api/login/` | 🔓 Público | Recebe `username` e `password` e retorna os tokens (`access` e `refresh`). |
| **POST** | `/api/transactions/` | 🔒 Protegido | Cria uma nova transação. Campos obrigatórios: `amount`, `type`, `date`. |
| **GET** | `/api/transactions/` | 🔒 Protegido | Lista todas as transações do usuário. Aceita paginação (`?page=1`). |
| **GET** | `/api/transactions/{id}/` | 🔒 Protegido | Exibe os detalhes de uma transação específica. |
| **PUT** | `/api/transactions/{id}/` | 🔒 Protegido | Atualiza uma transação completa. |
| **PATCH**| `/api/transactions/{id}/` | 🔒 Protegido | Atualiza parcialmente uma transação (ex: mudar só o valor). |
| **DELETE**| `/api/transactions/{id}/` | 🔒 Protegido | Remove uma transação permanentemente. |
| **GET** | `/api/summary/` | 🔒 Protegido | Retorna o resumo financeiro (Total Receitas, Despesas e Saldo). |

#### 🔍 Filtros Disponíveis
Na rota de listagem (`GET /api/transactions/`), você pode usar os seguintes filtros na URL:

* **Por Tipo:** `?type=income` ou `?type=expense`
* **Por Descrição (Busca):** `?description=aluguel`

## 🚀 Como Testar sua API

Para testar os endpoints de uma API (enviar `POST`, `PUT`, etc.), você não usa o navegador. Recomendamos o uso de uma ferramenta como o **Postman** ou **Insomnia**. Elas facilitam o envio de requisições e a visualização das resp

