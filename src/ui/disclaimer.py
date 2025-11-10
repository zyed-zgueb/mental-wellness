"""Disclaimer screen for Serene application"""
import streamlit as st


def show_disclaimer():
    """Afficher l'écran d'avertissement et de consentement."""
    st.title("🌸 Bienvenue sur Serene")

    st.warning("⚠️ Avertissement Important")

    st.markdown("""
    ### À propos de Serene

    Serene est un **compagnon d'IA** conçu pour vous accompagner dans votre bien-être mental.

    **IMPORTANT :**
    - ❌ Serene **n'est PAS** un professionnel de santé mentale
    - ❌ Serene **ne remplace PAS** une thérapie ou un traitement médical
    - ❌ Serene **ne peut PAS** diagnostiquer des conditions médicales

    ### Ressources d'Urgence 🆘

    Si vous êtes en crise ou avez des pensées suicidaires, contactez immédiatement :

    - **3114** : Numéro national de prévention du suicide (24/7, gratuit)
    - **15** : SAMU (urgences médicales)
    - **SOS Amitié** : 09 72 39 40 50 (24/7, écoute bienveillante)

    ### Vie Privée 🔒

    Toutes vos données sont stockées **localement** sur votre appareil. Aucune donnée n'est envoyée vers le cloud.

    [Lire la politique de confidentialité complète](#)
    """)

    # Bouton de consentement
    if st.button("J'ai compris et j'accepte de continuer", type="primary"):
        st.session_state.disclaimer_acknowledged = True
        st.rerun()
