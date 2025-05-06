from django.urls import path
from .views import WebhookView, ConversationDetailView, ConversationListView

urlpatterns = [
    path('webhook/', WebhookView.as_view(), name='webhook'),
    path('conversations/<uuid:pk>/', ConversationDetailView.as_view(), name='conversation-detail'),
    path('conversations/', ConversationListView.as_view(), name='conversation-list'),
] 