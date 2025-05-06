# Aqui a gente transforma nossos modelos em JSON e vice-versa!

from rest_framework import serializers
from .models import Conversation, Message

# Serializer de mensagem - transforma cada mensagem em JSON bonitinho
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        # Campos que vão aparecer no JSON da mensagem
        fields = ['id', 'direction', 'content', 'timestamp']

# Serializer de conversa - pega a conversa e todas as mensagens dela
class ConversationSerializer(serializers.ModelSerializer):
    # Inclui todas as mensagens da conversa - many=True porque são várias!
    # read_only porque as mensagens são criadas pelo webhook, não por aqui
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        # Campos que vão aparecer no JSON da conversa
        fields = ['id', 'state', 'messages'] 