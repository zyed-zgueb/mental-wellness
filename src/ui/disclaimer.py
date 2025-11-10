"""Disclaimer screen for Serene application"""
import streamlit as st


def show_disclaimer():
    """Afficher l'écran d'avertissement et de consentement."""
    st.title("Serene")
    st.subheader("Avertissement important")

    st.markdown("""
    ### À propos

    Serene est un compagnon d'intelligence artificielle conçu pour accompagner votre bien-être mental.

    ### Limitations

    - Serene n'est pas un professionnel de santé mentale
    - Serene ne remplace pas une thérapie ou un traitement médical
    - Serene ne peut pas diagnostiquer des conditions médicales

    ### Ressources d'urgence

    Si vous êtes en situation de crise ou avez des pensées suicidaires, contactez immédiatement :

    - **3114** - Numéro national de prévention du suicide (24/7, gratuit)
    - **15** - SAMU (urgences médicales)
    - **SOS Amitié** - 09 72 39 40 50 (24/7, écoute)

    ### Vie privée

    Toutes vos données sont stockées localement sur votre appareil. Aucune donnée n'est envoyée vers le cloud.
    """)

    # Bouton de consentement
    if st.button("J'ai compris et j'accepte de continuer", type="primary"):
        st.session_state.disclaimer_acknowledged = True
        st.rerun()
