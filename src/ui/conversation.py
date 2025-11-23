"""Interface de conversation avec l'IA - Gallery Minimalist Style"""

import streamlit as st
import html
from dotenv import load_dotenv
from src.database.db_manager import DatabaseManager
from src.ui.auth import get_current_user_id
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
    # Désactiver l'extraction automatique car on la fait manuellement dans l'UI
    return ConversationManager(db, enable_action_extraction=False)


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
        user_id = get_current_user_id()
        history = manager.db.get_conversation_history(user_id, limit=5)
        # Inverser pour afficher du plus ancien au plus récent
        st.session_state.conversation_history = list(history)

    # Initialiser l'état pour les propositions
    if 'last_proposals' not in st.session_state:
        st.session_state.last_proposals = []

    # Afficher l'historique (avatars stylisés via CSS)
    for conv in st.session_state.conversation_history:
        with st.chat_message("Moi", avatar =":material/circle:"):
            st.write('<span style=\"opacity: 0.87\"><b>MOI</b><br>&#8209;&nbsp;', conv['user_message'], '</span>', unsafe_allow_html=True)
        with st.chat_message("Serene", avatar =":material/circle:"):
            st.write('<b>SERENE</b><br>&#8209;&nbsp;', conv['ai_response'], unsafe_allow_html=True)

    # Input utilisateur
    if user_input := st.chat_input("Votre message..."):
        # Afficher message utilisateur (avatar stylisé via CSS)
        with st.chat_message("user"):
            st.write(user_input)

        # Détection crise
        if manager.detect_crisis(user_input):
            st.warning(EMERGENCY_RESOURCES)

        # Streaming réponse IA (avatar stylisé via CSS)
        user_id = get_current_user_id()
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""
            try:
                for chunk in manager.send_message(user_id, user_input):
                    full_response += chunk
                    placeholder.markdown(full_response + "▌")
                placeholder.markdown(full_response)

                # Ajouter à l'historique de session
                st.session_state.conversation_history.append({
                    'user_message': user_input,
                    'ai_response': full_response
                })

                # Extraire les propositions manuellement et les stocker dans session_state
                try:
                    from src.llm.action_extractor import ActionExtractor
                    db = get_database()
                    extractor = ActionExtractor(db)

                    # Récupérer le dernier conversation_id (celui qui vient d'être créé)
                    history = db.get_conversation_history(user_id, limit=1)
                    conversation_id = history[0]['id'] if history else None

                    # Extraire les actions
                    proposals = extractor.extract_actions_from_message(
                        user_input, user_id, conversation_id
                    )
                    st.session_state.last_proposals = proposals or []
                except Exception as e:
                    print(f"Erreur extraction: {e}")
                    st.session_state.last_proposals = []

                # Afficher les propositions d'actions détectées
                proposals = st.session_state.last_proposals
                if proposals:
                    st.markdown("---")
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #F5F5F0 0%, #E8E8E0 100%);
                        border-left: 4px solid #1A1A1A;
                        border-radius: 8px;
                        padding: 1rem 1.5rem;
                        margin: 1rem 0;
                    ">
                        <p style="
                            font-weight: 500;
                            color: #1A1A1A;
                            margin: 0;
                            font-size: 0.95rem;
                        ">✨ J'ai détecté {len(proposals)} action(s) dans votre message ! Voulez-vous les ajouter à votre liste ?</p>
                    </div>
                    """, unsafe_allow_html=True)

                    for i, proposal in enumerate(proposals):
                        # Échapper le HTML pour sécurité
                        safe_title = html.escape(proposal.get('title', ''))
                        safe_description = html.escape(proposal.get('description', ''))

                        # Carte de proposition stylisée
                        st.markdown(f"""
                        <div style="
                            background: white;
                            border: 2px solid #6B6B6B30;
                            border-radius: 8px;
                            padding: 1.25rem;
                            margin: 1rem 0;
                        ">
                            <h4 style="
                                font-family: 'Cormorant Garamond', serif;
                                font-size: 1.15rem;
                                font-weight: 500;
                                color: #1A1A1A;
                                margin: 0 0 0.5rem 0;
                            ">{safe_title}</h4>
                            <p style="
                                color: #6B6B6B;
                                margin: 0;
                                font-size: 0.9rem;
                                line-height: 1.5;
                            ">{safe_description}</p>
                        </div>
                        """, unsafe_allow_html=True)

                        # Boutons d'action
                        col1, col2, col3 = st.columns([1, 1, 3])
                        with col1:
                            if st.button("✓ Accepter", key=f"accept_prop_{proposal['id']}_{i}", type="primary", use_container_width=True):
                                try:
                                    db = get_database()
                                    action_id = db.accept_proposed_action(proposal['id'])
                                    st.success("✅ Action ajoutée à votre liste !")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Erreur: {e}")

                        with col2:
                            if st.button("✕ Rejeter", key=f"reject_prop_{proposal['id']}_{i}", use_container_width=True):
                                try:
                                    db = get_database()
                                    db.reject_proposed_action(proposal['id'])
                                    st.info("Action rejetée")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Erreur: {e}")

                        if i < len(proposals) - 1:
                            st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Erreur: {e}")
