"""
Serene - Mental Wellness AI Companion
Main Streamlit application entry point
"""
import streamlit as st
from src.ui.disclaimer import show_disclaimer

# Configuration de la page
st.set_page_config(
    page_title="Serene",
    layout="wide"
)


def show_home():
    """Afficher la page d'accueil."""
    st.title("Serene")
    st.subheader("Compagnon de bien-être mental")

    st.markdown("""
    ### Fonctionnalités

    - **Conversation Empathique** : Un espace d'écoute bienveillant et sans jugement
    - **Quick Check-in** : Suivez votre humeur au quotidien
    - **Dashboard** : Visualisez vos tendances de bien-être
    - **Insights** : Recevez des analyses personnalisées

    ### Statut actuel

    **Disponible :**
    - Home

    **En développement :**
    - Quick Check-in (Story 2)
    - Conversation (Story 3)
    - Dashboard (Story 4)
    """)


def main():
    """Point d'entrée principal de l'application."""

    # Vérifier si l'utilisateur a reconnu le disclaimer
    if not st.session_state.get('disclaimer_acknowledged', False):
        show_disclaimer()
    else:
        # Afficher le menu de navigation dans la sidebar
        with st.sidebar:
            st.title("Navigation")

            page = st.radio(
                "Menu",
                [
                    "Home",
                    "Quick Check-in",
                    "Conversation",
                    "Dashboard"
                ],
                index=0
            )

        # Afficher la page appropriée
        if page == "Home":
            show_home()
        elif page == "Quick Check-in":
            st.info("Quick Check-in sera disponible dans Story 2")
            st.markdown("""
            Cette fonctionnalité vous permettra de :
            - Enregistrer votre humeur quotidienne (échelle 1-10)
            - Ajouter des notes personnelles
            - Suivre l'historique de vos check-ins
            """)
        elif page == "Conversation":
            st.info("Conversation sera disponible dans Story 3")
            st.markdown("""
            Cette fonctionnalité vous permettra de :
            - Discuter avec Serene
            - Recevoir du soutien empathique
            - Exprimer vos émotions en toute sécurité
            """)
        elif page == "Dashboard":
            st.info("Dashboard sera disponible dans Story 4")
            st.markdown("""
            Cette fonctionnalité vous permettra de :
            - Visualiser vos tendances d'humeur
            - Voir l'activité de vos conversations
            - Recevoir des insights personnalisés
            """)


if __name__ == "__main__":
    main()
