# Frontend - Realmate Challenge

Interface web para interagir com a API do Realmate Challenge, construída com Streamlit.

## Funcionalidades

- Criar novas conversas
- Enviar e receber mensagens
- Visualizar histórico de mensagens
- Fechar conversas
- Simular respostas do cliente
- Atualizar conversas em tempo real

## Como Executar

1. Certifique-se de que a API Django está rodando em `http://localhost:8000`
2. Execute o frontend com o comando:
```bash
poetry run streamlit run frontend/app.py
```

## Como Usar

1. **Criar Nova Conversa**
   - Clique no botão "Nova Conversa" no painel lateral
   - Um novo ID de conversa será gerado automaticamente

2. **Enviar Mensagens**
   - Digite sua mensagem no campo de texto
   - Clique em "Enviar"
   - Para simular uma resposta do cliente, clique em "Simular resposta do cliente"

3. **Gerenciar Conversas**
   - Use o botão "Atualizar Conversa" para ver novas mensagens
   - Use o botão "Fechar Conversa" para encerrar a conversa
   - Você pode inserir um ID de conversa existente no campo "ID da Conversa"

4. **Visualizar Status**
   - O status da conversa (OPEN/CLOSED) é exibido no topo
   - Mensagens enviadas são marcadas com 👤
   - Mensagens recebidas são marcadas com 👥

## Notas

- Uma conversa fechada não pode receber novas mensagens
- Todas as mensagens são ordenadas por timestamp
- O frontend atualiza automaticamente após cada ação
- As mensagens são persistidas no banco de dados da API 