"""Interface de conversation avec l'IA."""

import streamlit as st
from dotenv import load_dotenv
from src.database.db_manager import DatabaseManager
from src.llm.conversation_manager import ConversationManager
from src.utils.prompts import EMERGENCY_RESOURCES

# Charger les variables d'environnement
load_dotenv()


@st.cache_resource
def get_database():
    """Singleton DatabaseManager."""
    return DatabaseManager("serene.db")


@st.cache_resource
def get_conversation_manager():
    """Singleton ConversationManager."""
    db = get_database()
    return ConversationManager(db)


def show_conversation():
    """Afficher la page de conversation avec design empathique."""
    st.title("Conversation")
    st.markdown("""
    <p style='font-size: 1.1rem; color: #4A5568; margin-bottom: 2rem;'>
    Un espace d'écoute bienveillant et sans jugement. Parlez librement de ce que vous ressentez.
    </p>
    """, unsafe_allow_html=True)

    try:
        manager = get_conversation_manager()
    except ValueError as e:
        # Error state élégant
        st.markdown("""
        <div style='background-color: #FFF5F5; padding: 2rem; border-radius: 12px; border-left: 4px solid #F56565;'>
            <h3 style='color: #C53030; margin-top: 0;'>❌ Configuration manquante</h3>
            <p style='color: #742A2A;'>Veuillez configurer votre ANTHROPIC_API_KEY dans un fichier .env</p>
        </div>
        """, unsafe_allow_html=True)
        st.code("ANTHROPIC_API_KEY=sk-ant-your-key-here", language="bash")
        return

    # Initialiser l'historique dans session_state si nécessaire
    if 'conversation_history' not in st.session_state:
        history = manager.db.get_conversation_history(limit=50)
        # Inverser pour afficher du plus ancien au plus récent
        st.session_state.conversation_history = list(reversed(history))

    # Afficher l'historique
    for conv in st.session_state.conversation_history:
        with st.chat_message("user"):
            st.write(conv['user_message'])
        with st.chat_message("assistant"):
            st.write(conv['ai_response'])

    # Input utilisateur
    if user_input := st.chat_input("Votre message..."):
        # Afficher message utilisateur
        with st.chat_message("user"):
            st.write(user_input)

        # Détection crise
        if manager.detect_crisis(user_input):
            st.warning(EMERGENCY_RESOURCES)

        # Streaming réponse IA
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""
            try:
                for chunk in manager.send_message(user_input):
                    full_response += chunk
                    placeholder.markdown(full_response + "▌")
                placeholder.markdown(full_response)

                # Ajouter à l'historique de session
                st.session_state.conversation_history.append({
                    'user_message': user_input,
                    'ai_response': full_response
                })
            except Exception as e:
                st.error(f"❌ Erreur: {e}")
