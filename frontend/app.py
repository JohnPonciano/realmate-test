import streamlit as st
import requests
import uuid
from datetime import datetime
import pytz

# URL da nossa API Django - se mudar a porta, muda aqui!
API_URL = "http://localhost:8000"

def get_all_conversations():
    """Busca todas as conversas da API"""
    try:
        # Faz um GET na API pra listar todas as conversas
        response = requests.get(f"{API_URL}/conversations/")
        if response.status_code == 200:
            conversations = response.json()
            # Atualiza o histórico com todas as conversas
            st.session_state.conversation_history = [
                {
                    "id": conv["id"],
                    "created_at": conv.get("created_at", datetime.now(pytz.UTC).isoformat()),
                    "state": conv["state"]
                }
                for conv in conversations
            ]
            return True
        return False
    except Exception as e:
        st.error(f"Erro ao buscar conversas: {str(e)}")
        return False

def create_conversation():
    # Gera um UUID único pra conversa - isso evita conflitos de ID
    conversation_id = str(uuid.uuid4())
    
    # Manda um POST pra API criar a conversa
    response = requests.post(
        f"{API_URL}/webhook/",
        json={
            "type": "NEW_CONVERSATION",
            "timestamp": datetime.now(pytz.UTC).isoformat(),
            "data": {
                "id": conversation_id
            }
        }
    )
    
    if response.status_code == 201:
        # Atualiza o histórico completo
        get_all_conversations()
        st.success("Conversa criada com sucesso!")
        return conversation_id
    else:
        st.error(f"Erro ao criar conversa: {response.json()}")
        return None

def send_message(conversation_id, content, direction):
    # Envia uma mensagem pra conversa - pode ser SENT (nossa) ou RECEIVED (do cliente)
    response = requests.post(
        f"{API_URL}/webhook/",
        json={
            "type": "NEW_MESSAGE",
            "timestamp": datetime.now(pytz.UTC).isoformat(),
            "data": {
                "id": str(uuid.uuid4()),  # Cada mensagem também tem ID único
                "direction": direction,
                "content": content,
                "conversation_id": conversation_id
            }
        }
    )
    if response.status_code == 201:
        st.success("Mensagem enviada com sucesso!")
        return True
    else:
        st.error(f"Erro ao enviar mensagem: {response.json()}")
        return False

def close_conversation(conversation_id):
    # Fecha a conversa - depois disso não dá pra mandar mais mensagens!
    response = requests.post(
        f"{API_URL}/webhook/",
        json={
            "type": "CLOSE_CONVERSATION",
            "timestamp": datetime.now(pytz.UTC).isoformat(),
            "data": {
                "id": conversation_id
            }
        }
    )
    if response.status_code in [200, 201]:
        # Atualiza o histórico completo
        get_all_conversations()
        st.success("Conversa fechada com sucesso!")
        return True
    else:
        st.error(f"Erro ao fechar conversa: {response.json()}")
        return False

def get_conversation(conversation_id):
    # Busca os detalhes de uma conversa específica
    response = requests.get(f"{API_URL}/conversations/{conversation_id}/")
    if response.status_code == 200:
        data = response.json()
        # Atualiza o estado no histórico
        if "conversation_history" in st.session_state:
            for conv in st.session_state.conversation_history:
                if conv["id"] == conversation_id:
                    conv["state"] = data["state"]
                    break
        return data
    else:
        st.error(f"Erro ao buscar conversa: {response.json()}")
        return None

def format_conversation_id(conversation_id):
    """Pega só os primeiros caracteres do ID - ninguém precisa ver aquele UUID gigante!"""
    return f"{conversation_id[:8]}..."

def main():
    # Configura a página do Streamlit
    st.set_page_config(
        page_title="Realmate Challenge - Chat",
        page_icon="💬",
        layout="wide"  # Usa a tela toda, fica mais bonito
    )

    st.title("💬 Realmate Challenge - Chat")

    # Primeira vez ou atualização? Busca todas as conversas!
    if "conversation_history" not in st.session_state:
        get_all_conversations()

    # Sidebar - aqui fica o controle das conversas
    with st.sidebar:
        st.header("Ações")
        col1, col2 = st.columns([3,1])
        with col1:
            if st.button("🆕 Nova Conversa", use_container_width=True):
                conversation_id = create_conversation()
                if conversation_id:
                    st.session_state.conversation_id = conversation_id
                    st.session_state.messages = []
                    st.rerun()
        with col2:
            if st.button("🔄", help="Atualizar histórico", use_container_width=True):
                get_all_conversations()
                st.rerun()

        st.divider()
        
        # Campo pra colar um ID de conversa existente
        conversation_id = st.text_input(
            "ID da Conversa",
            value=st.session_state.get("conversation_id", ""),
            key="conversation_id_input"
        )
        
        if conversation_id:
            st.session_state.conversation_id = conversation_id
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Atualizar", use_container_width=True):
                    # Busca as mensagens mais recentes
                    conversation = get_conversation(conversation_id)
                    if conversation:
                        st.session_state.messages = conversation.get("messages", [])
                        st.session_state.conversation_state = conversation.get("state")
                        st.rerun()

            with col2:
                if st.button("❌ Fechar", use_container_width=True):
                    if close_conversation(conversation_id):
                        st.session_state.conversation_state = "CLOSED"
                        st.rerun()

        # Lista todas as conversas que já rolaram
        st.divider()
        st.header("Histórico de Conversas")
        
        if st.session_state.conversation_history:
            # Ordena por data, mais recentes primeiro
            for conv in sorted(st.session_state.conversation_history, key=lambda x: x["created_at"], reverse=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    # Mostra 🔓 pra aberta e 🔒 pra fechada
                    if st.button(
                        f"{'🔓' if conv['state'] == 'OPEN' else '🔒'} {format_conversation_id(conv['id'])}",
                        key=f"history_{conv['id']}",
                        use_container_width=True
                    ):
                        st.session_state.conversation_id = conv["id"]
                        conversation = get_conversation(conv["id"])
                        if conversation:
                            st.session_state.messages = conversation.get("messages", [])
                            st.session_state.conversation_state = conversation.get("state")
                        st.rerun()
                with col2:
                    st.write(conv["state"])
        else:
            st.info("Nenhuma conversa no histórico")

    # Área principal - aqui é onde rola a conversa
    if "conversation_id" in st.session_state:
        conversation_id = st.session_state.conversation_id
        conversation_state = st.session_state.get("conversation_state", "OPEN")
        
        # Mostra se tá aberta ou fechada
        st.info(f"Status da conversa: {conversation_state}")

        # Área das mensagens - tipo um WhatsApp
        st.subheader("Mensagens")
        messages_container = st.container()
        
        with messages_container:
            messages = st.session_state.get("messages", [])
            for msg in messages:
                # 👤 pra nossas mensagens, 👥 pra mensagens do cliente
                if msg["direction"] == "SENT":
                    st.write("👤 Você:", msg["content"])
                else:
                    st.write("👥 Cliente:", msg["content"])

        # Campo pra digitar mensagem - só aparece se a conversa tiver aberta
        if conversation_state == "OPEN":
            # Container único para o campo de mensagem e botões
            with st.container():
                # Remove o label do campo de texto para alinhar melhor com os botões
                col1, col2, col3 = st.columns([6, 2, 2])
                with col1:
                    # Usa empty para criar espaço e alinhar com os botões
                    st.write("")
                    message = st.text_input(
                        "Digite sua mensagem:",
                        key="message_input",
                        label_visibility="collapsed"  # Esconde o label mas mantém acessibilidade
                    )
                with col2:
                    # Usa empty para criar espaço e alinhar com o campo de texto
                    st.write("")
                    if st.button("📤 Enviar", use_container_width=True, key="send_button"):
                        if message:
                            if send_message(conversation_id, message, "SENT"):
                                # Atualiza pra mostrar a mensagem nova
                                conversation = get_conversation(conversation_id)
                                if conversation:
                                    st.session_state.messages = conversation.get("messages", [])
                                st.rerun()
                with col3:
                    # Usa empty para criar espaço e alinhar com o campo de texto
                    st.write("")
                    if st.button("👥 Simular", use_container_width=True, key="simulate_button"):
                        if send_message(conversation_id, "Esta é uma resposta simulada do cliente!", "RECEIVED"):
                            conversation = get_conversation(conversation_id)
                            if conversation:
                                st.session_state.messages = conversation.get("messages", [])
                            st.rerun()
        else:
            st.warning("Esta conversa está fechada. Não é possível enviar novas mensagens.")
    else:
        st.info("👈 Crie uma nova conversa ou insira um ID de conversa existente no painel lateral.")

if __name__ == "__main__":
    main() 