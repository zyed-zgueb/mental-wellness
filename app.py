"""
Serene - Mental Wellness AI Companion
Main Streamlit application entry point
"""
import streamlit as st
from src.ui.disclaimer import show_disclaimer

# Configuration de la page
st.set_page_config(
    page_title="Serene - Compagnon de Bien-être Mental",
    page_icon="🌸",
    layout="wide"
)


def show_home():
    """Afficher la page d'accueil."""
    st.title("🌸 Bienvenue sur Serene")

    st.markdown("""
    Serene est votre compagnon IA bienveillant pour le bien-être mental.

    ### 🌟 Fonctionnalités

    **Serene vous accompagne avec :**
    - 💬 **Conversation Empathique** : Un espace d'écoute bienveillant et sans jugement
    - 📊 **Quick Check-in** : Suivez votre humeur au quotidien
    - 📈 **Dashboard** : Visualisez vos tendances de bien-être
    - 💡 **AI Insights** : Recevez des insights personnalisés

    ### 📍 Où en sommes-nous ?

    **Actuellement disponible :**
    - ✅ **Home** : Vous êtes ici !

    **Prochainement :**
    - 🔄 **Quick Check-in** : Disponible dans Story 2
    - 🔄 **Conversation** : Disponible dans Story 3
    - 🔄 **Dashboard** : Disponible dans Story 4

    ---

    *Utilisez le menu de navigation à gauche pour explorer l'application.*
    """)


def main():
    """Point d'entrée principal de l'application."""

    # Vérifier si l'utilisateur a reconnu le disclaimer
    if not st.session_state.get('disclaimer_acknowledged', False):
        show_disclaimer()
    else:
        # Afficher le menu de navigation dans la sidebar
        with st.sidebar:
            st.title("🧭 Navigation")

            page = st.radio(
                "Aller à :",
                [
                    "🏠 Home",
                    "📊 Quick Check-in",
                    "💬 Conversation",
                    "📈 Dashboard"
                ],
                index=0
            )

        # Afficher la page appropriée
        if page == "🏠 Home":
            show_home()
        elif page == "📊 Quick Check-in":
            st.info("📊 **Quick Check-in** sera disponible dans Story 2 !")
            st.markdown("""
            Cette fonctionnalité vous permettra de :
            - Enregistrer votre humeur quotidienne (échelle 1-10)
            - Ajouter des notes personnelles
            - Suivre l'historique de vos check-ins
            """)
        elif page == "💬 Conversation":
            st.info("💬 **Conversation** sera disponible dans Story 3 !")
            st.markdown("""
            Cette fonctionnalité vous permettra de :
            - Discuter avec Serene, votre compagnon IA
            - Recevoir du soutien empathique
            - Exprimer vos émotions en toute sécurité
            """)
        elif page == "📈 Dashboard":
            st.info("📈 **Dashboard** sera disponible dans Story 4 !")
            st.markdown("""
            Cette fonctionnalité vous permettra de :
            - Visualiser vos tendances d'humeur
            - Voir l'activité de vos conversations
            - Recevoir des insights IA personnalisés
            """)


if __name__ == "__main__":
    main()
