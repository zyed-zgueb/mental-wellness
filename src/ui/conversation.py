"""Interface de conversation avec l'IA - Gallery Minimalist Style"""

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
    """Afficher la page de conversation - Gallery minimalist style."""

    # Header minimaliste
    st.markdown("""
    <div style='animation: fadeInDown 0.4s ease-out; margin-bottom: 3rem;
                padding-bottom: 2rem; border-bottom: 1px solid var(--line-light);'>
        <h1 style='font-family: "Cormorant Garamond", serif; font-size: 3rem;
                   color: var(--black); font-weight: 300; margin-bottom: 1rem;
                   letter-spacing: 0.02em; line-height: 1.1;'>
            Conversation
        </h1>
        <p style='font-family: "Inter", sans-serif; font-size: 0.9375rem;
                 color: var(--gray-dark); margin: 0; line-height: 1.8;
                 font-weight: 300; max-width: 600px;'>
            Un espace d'écoute bienveillant et sans jugement. Parlez librement de ce que vous ressentez.
        </p>
    </div>
    """, unsafe_allow_html=True)

    try:
        manager = get_conversation_manager()
    except ValueError as e:
        # Error state minimaliste
        st.markdown("""
        <div style='background-color: var(--white); padding: 2rem; border: 1px solid var(--line-light);
                    border-left: 2px solid var(--black); box-shadow: var(--shadow-subtle);'>
            <h3 style='font-family: "Inter", sans-serif; color: var(--black); margin-top: 0;
                       font-size: 0.75rem; font-weight: 400; letter-spacing: 0.1em;
                       text-transform: uppercase; margin-bottom: 1rem;'>
                Configuration manquante
            </h3>
            <p style='font-family: "Inter", sans-serif; color: var(--gray-dark);
                     line-height: 1.8; font-size: 0.875rem; font-weight: 300;'>
                Veuillez configurer votre ANTHROPIC_API_KEY dans un fichier .env
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.code("ANTHROPIC_API_KEY=sk-ant-your-key-here", language="bash")
        return

    # Initialiser l'historique dans session_state si nécessaire
    if 'conversation_history' not in st.session_state:
        history = manager.db.get_conversation_history(limit=50)
        # Inverser pour afficher du plus ancien au plus récent
        st.session_state.conversation_history = list(history)

    # Afficher l'historique (avatars stylisés via CSS)
    for conv in st.session_state.conversation_history:
        with st.chat_message("user"):
            st.write(conv['user_message'])
        with st.chat_message("assistant"):
            st.write(conv['ai_response'])

    # Input utilisateur
    if user_input := st.chat_input("Votre message..."):
        # Afficher message utilisateur (avatar stylisé via CSS)
        with st.chat_message("user"):
            st.write(user_input)

        # Détection crise
        if manager.detect_crisis(user_input):
            st.warning(EMERGENCY_RESOURCES)

        # Streaming réponse IA (avatar stylisé via CSS)
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
                st.error(f"Erreur: {e}")
