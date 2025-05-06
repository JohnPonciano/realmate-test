# 📬 Postman Collection - Realmate Challenge

E aí! Aqui você encontra tudo que precisa pra testar nossa API do Realmate Challenge direto no Postman. Bora ver como funciona? 🚀

## 🎯 Como Importar

1. Abre o Postman
2. Clica no botão "Import" lá em cima
3. Arrasta o arquivo `realmate_challenge.postman_collection.json` pra lá (ou clica em "Upload Files" se preferir fazer do jeito tradicional 😉)
4. Manda ver no "Import"!

## 🔥 Endpoints Disponíveis

### 1. Criar Nova Conversa 📥
- **Método**: POST
- **URL**: `http://localhost:8000/webhook/`
- **O que faz**: Cria uma conversa novinha em folha!
- **Cola esse JSON aqui**:
```json
{
    "type": "NEW_CONVERSATION",
    "timestamp": "2025-02-21T10:20:41.349308",
    "data": {
        "id": "6a41b347-8d80-4ce9-84ba-7af66f369f6a"
    }
}
```

### 2. Cliente Mandou Mensagem 👥
- **Método**: POST
- **URL**: `http://localhost:8000/webhook/`
- **O que faz**: Registra uma mensagem que o cliente mandou
- **JSON da boa**:
```json
{
    "type": "NEW_MESSAGE",
    "timestamp": "2025-02-21T10:20:42.349308",
    "data": {
        "id": "49108c71-4dca-4af3-9f32-61bc745926e2",
        "direction": "RECEIVED",
        "content": "Olá, tudo bem?",
        "conversation_id": "6a41b347-8d80-4ce9-84ba-7af66f369f6a"
    }
}
```

### 3. A Gente Mandou Mensagem 👤
- **Método**: POST
- **URL**: `http://localhost:8000/webhook/`
- **O que faz**: Registra uma mensagem que a gente mandou pro cliente
- **Manda esse JSON**:
```json
{
    "type": "NEW_MESSAGE",
    "timestamp": "2025-02-21T10:20:44.349308",
    "data": {
        "id": "16b63b04-60de-4257-b1a1-20a5154abc6d",
        "direction": "SENT",
        "content": "Tudo ótimo e você?",
        "conversation_id": "6a41b347-8d80-4ce9-84ba-7af66f369f6a"
    }
}
```

### 4. Fechar Conversa 🔒
- **Método**: POST
- **URL**: `http://localhost:8000/webhook/`
- **O que faz**: Fecha a conversa (depois não dá pra mandar mais mensagem!)
- **JSON pra fechar**:
```json
{
    "type": "CLOSE_CONVERSATION",
    "timestamp": "2025-02-21T10:20:45.349308",
    "data": {
        "id": "6a41b347-8d80-4ce9-84ba-7af66f369f6a"
    }
}
```

### 5. Ver Detalhes da Conversa 🔍
- **Método**: GET
- **URL**: `http://localhost:8000/conversations/{conversation_id}/`
- **O que faz**: Mostra tudo que rolou na conversa (estado, mensagens, etc)

## 🎮 Roteiro de Teste

Quer testar tudo certinho? Segue o fio:

1. Primeiro cria uma conversa nova ✨
2. Finge que o cliente mandou uma mensagem 👥
3. Responde o cliente 👤
4. Dá uma olhada em como a conversa tá (GET) 🔍
5. Fecha a conversa 🔒
6. Tenta mandar outra mensagem pra ver o erro (vai dar erro mesmo, é assim que tem que ser! 😉)
7. Confere de novo a conversa pra ver se fechou direitinho

## 💡 Dicas e Macetes

- Antes de sair testando, confere se o Django tá rodando em `http://localhost:8000` 🚦
- Os IDs nos exemplos são UUIDs - pode usar esses mesmos ou criar novos, tanto faz! 🎲
- Não esquece de colocar `Content-Type: application/json` nos headers quando for POST 📝
- Se der erro 400, confere se não esqueceu nenhum campo obrigatório no JSON 🔍
- Anota o ID da conversa que criar, vai precisar dele pra todos os outros testes! 📝

## 🆘 Deu Ruim?

Se algo não funcionar como esperado:
1. Respira fundo 😌
2. Confere se o servidor tá rodando
3. Olha se não esqueceu nenhum campo no JSON
4. Verifica se tá usando o ID certo da conversa
5. Se ainda assim não rolar, fala com a gente! 🤙 