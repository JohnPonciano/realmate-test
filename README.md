# Realmate Challenge

## 📝 Sobre o Projeto

O projeto consiste em uma API Django para sincronização de eventos de atendimento do WhatsApp e um frontend em Streamlit para visualização e interação com as conversas.

## 🛠️ Tecnologias Utilizadas

- **Backend**:
  - Django
  - Django Rest Framework
  - SQLite
  - Poetry (gerenciamento de dependências)

- **Frontend**:
  - Streamlit
  - Requests
  - PyTZ

## 🚀 Como Executar

### Pré-requisitos

- Python 3.8 ou superior
- Poetry instalado:
```bash
pip install poetry
```
- Postman (para testar a API)

### 1️⃣ Instalação das Dependências

```bash
# Clone o repositório
git clone <seu-repositorio>
cd realmate-challenge

# Instale as dependências usando Poetry
poetry install
```

### 2️⃣ Configuração do Banco de Dados

```bash
# Aplique as migrações
poetry run python manage.py migrate
```

### 3️⃣ Executando a API (Backend)

```bash
# Inicie o servidor Django
poetry run python manage.py runserver
```

A API estará disponível em `http://localhost:8000`

### 4️⃣ Executando o Frontend

Em outro terminal, execute:

```bash
# Inicie o servidor Streamlit
poetry run streamlit run frontend/app.py
```

O frontend estará disponível em `http://localhost:8501`

## 📌 Endpoints da API

### Webhook (`POST /webhook/`)
Recebe eventos de:
- Nova conversa
- Nova mensagem
- Fechamento de conversa

### Conversas (`GET /conversations/{id}/`)
Retorna detalhes de uma conversa específica, incluindo:
- Estado (OPEN/CLOSED)
- Mensagens

## 🧪 Testando a API com Postman

Para facilitar os testes da API, disponibilizei uma coleção do Postman com todos os endpoints configurados:

1. Abra o Postman
2. Importe a coleção em `postman/realmate_challenge.postman_collection.json`
3. A coleção inclui exemplos para:
   - Criar nova conversa
   - Enviar mensagem (SENT/RECEIVED)
   - Fechar conversa
   - Consultar conversa por ID

Cada request já está pré-configurado com:
- URL correta
- Método HTTP apropriado
- Headers necessários
- Exemplo de body JSON
- Descrição do que cada endpoint faz

> 💡 **Dica**: Os exemplos usam variáveis para IDs de conversa. Após criar uma conversa, copie o ID retornado e use nos outros requests!

## 💻 Interface do Frontend

### Funcionalidades
- Criar novas conversas
- Enviar e receber mensagens
- Visualizar histórico de mensagens
- Fechar conversas
- Simular respostas do cliente
- Histórico de todas as conversas
- Atualização em tempo real

### Seções
1. **Painel Lateral**:
   - Botão para nova conversa
   - Campo para ID de conversa
   - Histórico de conversas
   - Ações de atualizar e fechar

2. **Área Principal**:
   - Status da conversa
   - Histórico de mensagens
   - Campo para envio de mensagens
   - Simulação de resposta do cliente

## 🧪 Testando a Aplicação

1. Inicie a API Django
2. Inicie o frontend Streamlit
3. Crie uma nova conversa pelo frontend
4. Envie algumas mensagens
5. Teste o fechamento da conversa
6. Verifique o histórico de conversas

## 📋 Regras de Negócio

- Toda conversa começa como "OPEN"
- Conversas fechadas não podem receber novas mensagens
- Mensagens devem estar associadas a uma conversa existente
- IDs de mensagens e conversas são únicos (UUID)
- Sistema trata erros graciosamente

## 📧 Dúvidas e Suporte

Em caso de dúvidas, entre em contato pelo e-mail: tecnologia@realmate.com.br