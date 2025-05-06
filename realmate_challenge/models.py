# Aqui é onde a mágica acontece! 🎩
# Vamos definir as estruturas das nossas tabelas no banco

from django.db import models
import uuid

# Modelo da conversa - tipo um chat do WhatsApp 
class Conversation(models.Model):
    # Estados possíveis da conversa - ou tá rolando ou já acabou!
    STATES = [
        ('OPEN', 'Open'),    # Conversa rolando! 
        ('CLOSED', 'Closed') # Conversa encerrada! 
    ]

    # UUID é tipo CPF da conversa - cada uma tem o seu, único!
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # OPEN ou CLOSED - simples assim!
    state = models.CharField(max_length=6, choices=STATES, default='OPEN')
    # Pra gente saber quando a conversa começou e foi atualizada pela última vez
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversa {self.id} ({self.state})"

# Modelo de mensagem - cada balãozinho numa conversa 
class Message(models.Model):
    # Quem mandou a mensagem? A gente ou o cliente?
    DIRECTIONS = [
        ('SENT', 'Sent'),     # Mensagem que a gente mandou 
        ('RECEIVED', 'Received')  # Mensagem que a gente recebeu 
    ]

    # Cada mensagem também tem seu UUID único
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Link com a conversa - se a conversa for deletada, as mensagens vão junto!
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    # SENT ou RECEIVED - de onde veio a mensagem?
    direction = models.CharField(max_length=8, choices=DIRECTIONS)
    # O texto da mensagem em si
    content = models.TextField()
    # Quando a mensagem foi enviada
    timestamp = models.DateTimeField()
    # Quando criamos o registro no banco
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensagem {self.direction} na conversa {self.conversation.id}"

    class Meta:
        # Ordena as mensagens por timestamp - as mais antigas primeiro!
        ordering = ['timestamp']
