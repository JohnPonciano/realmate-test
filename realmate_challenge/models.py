# Aqui é onde a mágica acontece! 🎩
# Vamos definir as estruturas das nossas tabelas no banco

from django.db import models
import uuid

# Modelo da conversa -
class Conversation(models.Model):
    # Estados possíveis da conversa 
    STATES = [
        ('OPEN', 'Open'),    # Conversa rolando! 
        ('CLOSED', 'Closed'), # Conversa encerrada!
    ]

    # UUID 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # OPEN ou CLOSED 
    state = models.CharField(max_length=6, choices=STATES, default='OPEN')
    # Pra gente saber quando a conversa começou e foi atualizada pela última vez
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversa {self.id} ({self.state})"

# Modelo de mensagem 
class Message(models.Model):
    # Quem mandou a mensagem?
    DIRECTIONS = [
        ('SENT', 'Sent')
        ('RECEIVED', 'Received'),
    ]

    # Cada mensagem também tem seu UUID único
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Link com a conversa - se a conversa for deletada, as mensagens vão junto!
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    # SENT ou RECEIVED - de onde veio a mensagem?
    direction = models.CharField(max_length=8, choices=DIRECTIONS)
    # O texto da mensagem
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
