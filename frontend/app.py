import streamlit as st
import requests
import uuid
from datetime import datetime
import pytz

# URL da nossa API Django - se mudar a porta, muda aqui!
API_URL = "http://localhost:8000"

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
        # Deu bom! Vamo guardar no histórico pra não perder, o historico é temporario, então se atualizar a apagina ele some junto, o ideal seria salvar no banco de dados
        if "conversation_history" not in st.session_state:
            st.session_state.conversation_history = []
        st.session_state.conversation_history.append({
            "id": conversation_id,
            "created_at": datetime.now(pytz.UTC).isoformat(),
            "state": "OPEN"
        })
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
        # Atualiza o status no histórico pra mostrar que fechou
        if "conversation_history" in st.session_state:
            for conv in st.session_state.conversation_history:
                if conv["id"] == conversation_id:
                    conv["state"] = "CLOSED"
                    break
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
        # Se a conversa não tá no histórico ainda, adiciona
        if "conversation_history" in st.session_state:
            found = False
            for conv in st.session_state.conversation_history:
                if conv["id"] == conversation_id:
                    conv["state"] = data["state"]
                    found = True
                    break
            if not found:
                st.session_state.conversation_history.append({
                    "id": conversation_id,
                    "created_at": datetime.now(pytz.UTC).isoformat(),
                    "state": data["state"]
                })
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

    # Cria o histórico vazio
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []

    # Sidebar - aqui fica o controle das conversas
    with st.sidebar:
        st.header("Ações")
        if st.button("🆕 Nova Conversa"):
            conversation_id = create_conversation()
            if conversation_id:
                st.session_state.conversation_id = conversation_id
                st.session_state.messages = []
                st.rerun()  # Recarrega pra mostrar a nova conversa

        st.divider()
        
        # Campo pra colar um ID de conversa existente
        conversation_id = st.text_input(
            "ID da Conversa",
            value=st.session_state.get("conversation_id", ""),
            key="conversation_id_input"
        )
        
        if conversation_id:
            st.session_state.conversation_id = conversation_id
            if st.button("🔄 Atualizar Conversa"):
                # Busca as mensagens mais recentes
                conversation = get_conversation(conversation_id)
                if conversation:
                    st.session_state.messages = conversation.get("messages", [])
                    st.session_state.conversation_state = conversation.get("state")

            if st.button("❌ Fechar Conversa"):
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
                        key=f"history_{conv['id']}"
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
            with st.container():
                col1, col2 = st.columns([4, 1])
                with col1:
                    message = st.text_input("Digite sua mensagem:", key="message_input")
                with col2:
                    if st.button("Enviar"):
                        if message:
                            if send_message(conversation_id, message, "SENT"):
                                # Atualiza pra mostrar a mensagem nova
                                conversation = get_conversation(conversation_id)
                                if conversation:
                                    st.session_state.messages = conversation.get("messages", [])
                                st.rerun()
                
                # Botão pra simular resposta do cliente - só pra teste mesmo
                if st.button("Simular resposta do cliente"):
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