# Aqui é core da API
from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Conversation, Message
from .serializers import ConversationSerializer
from django.utils.dateparse import parse_datetime
from django.db import IntegrityError
from django.core.exceptions import ValidationError
import uuid

# Webhook - recebe todos os eventos do chat
class WebhookView(APIView):
    def post(self, request):
        # Pega os dados do evento que chegou
        event_type = request.data.get('type')
        timestamp = request.data.get('timestamp')
        data = request.data.get('data', {})

        try:
            # Valida o ID antes de qualquer coisa
            if 'id' not in data:
                return Response(
                    {'error': 'ID é obrigatório'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Verifica se o ID é um UUID válido
            try:
                uuid.UUID(str(data['id']))
            except ValueError:
                return Response(
                    {'error': 'ID deve ser um UUID válido'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Nova conversa 
            if event_type == 'NEW_CONVERSATION':
                try:
                    conversation = Conversation.objects.create(
                        id=data['id'],
                        state='OPEN'  # Toda conversa começa aberta!
                    )
                    return Response({'status': 'conversation created'}, status=status.HTTP_201_CREATED)
                except IntegrityError:
                    return Response(
                        {'error': f'Já existe uma conversa com o ID {data["id"]}'},
                        status=status.HTTP_409_CONFLICT
                    )

            # Nova mensagem 
            elif event_type == 'NEW_MESSAGE':
                # Validações específicas para mensagem
                if 'conversation_id' not in data:
                    return Response(
                        {'error': 'ID da conversa é obrigatório'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                if 'direction' not in data:
                    return Response(
                        {'error': 'Direction é obrigatório (SENT ou RECEIVED)'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                if data['direction'] not in ['SENT', 'RECEIVED']:
                    return Response(
                        {'error': 'Direction deve ser SENT ou RECEIVED'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                if 'content' not in data:
                    return Response(
                        {'error': 'Content é obrigatório'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                try:
                    # Procura a conversa - se não achar, já retorna 404
                    conversation = Conversation.objects.get(id=data['conversation_id'])
                except Conversation.DoesNotExist:
                    return Response(
                        {'error': f'Conversa com ID {data["conversation_id"]} não encontrada'},
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                # conversa fechada não recebe mensagem
                if conversation.state == 'CLOSED':
                    return Response(
                        {'error': 'Não é possível adicionar mensagem em uma conversa fechada'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                try:
                    # Cria a mensagem no banco
                    Message.objects.create(
                        id=data['id'],
                        conversation=conversation,
                        direction=data['direction'],  # SENT ou RECEIVED
                        content=data['content'],      # O texto da mensagem
                        timestamp=parse_datetime(timestamp)  
                    )
                    return Response({'status': 'message created'}, status=status.HTTP_201_CREATED)
                except IntegrityError:
                    return Response(
                        {'error': f'Já existe uma mensagem com o ID {data["id"]}'},
                        status=status.HTTP_409_CONFLICT
                    )

            # Fechando a conversa
            elif event_type == 'CLOSE_CONVERSATION':
                try:
                    conversation = Conversation.objects.get(id=data['id'])
                    if conversation.state == 'CLOSED':
                        return Response(
                            {'error': 'Esta conversa já está fechada'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    conversation.state = 'CLOSED'
                    conversation.save()
                    return Response({'status': 'conversation closed'})
                except Conversation.DoesNotExist:
                    return Response(
                        {'error': f'Conversa com ID {data["id"]} não encontrada'},
                        status=status.HTTP_404_NOT_FOUND
                    )

            # Tipo de evento que a gente não conhece
            return Response(
                {'error': 'Tipo de evento inválido. Use NEW_CONVERSATION, NEW_MESSAGE ou CLOSE_CONVERSATION'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Se faltar algum campo obrigatório...
        except KeyError as e:
            return Response(
                {'error': f'Campo obrigatório não encontrado: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Se der algum erro na validação dos dados...
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Se der qualquer outro erro inesperado...
        except Exception as e:
            return Response(
                {'error': f'Erro inesperado: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# View pra consultar os detalhes de uma conversa
class ConversationDetailView(generics.RetrieveAPIView):
    # Pega todas as conversas do banco
    queryset = Conversation.objects.all()
    # Usa o ConversationSerializer pra transformar em JSON
    serializer_class = ConversationSerializer

# View pra listar todas as conversas
class ConversationListView(generics.ListAPIView):
    # Pega todas as conversas do banco
    queryset = Conversation.objects.all().order_by('-created_at')
    # Usa o mesmo serializer da view de detalhes
    serializer_class = ConversationSerializer
