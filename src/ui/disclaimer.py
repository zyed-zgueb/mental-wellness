"""Disclaimer screen for Serene application"""
import streamlit as st

try:
    from streamlit_shadcn_ui import card, badge, alert
    SHADCN_AVAILABLE = True
except ImportError:
    SHADCN_AVAILABLE = False


def show_disclaimer():
    """Afficher l'écran d'avertissement et de consentement avec design premium."""

    # Centered layout
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("<h1 style='text-align: center; color: var(--color-primary);'>🌸 Serene</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 1.1rem; color: #4A5568; margin-bottom: 2rem;'>Votre compagnon de bien-être mental</p>", unsafe_allow_html=True)

        # Card 1: À propos
        st.markdown("""
        <div style='background-color: #F7FAFC; padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem; box-shadow: 0 1px 3px var(--color-primary-dark);'>
            <h3 style='color: var(--color-primary); margin-top: 0;'>💜 À propos</h3>
            <p style='color: #4A5568; line-height: 1.7;'>
                Serene est un compagnon d'intelligence artificielle conçu pour accompagner votre bien-être mental avec empathie et bienveillance.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Card 2: Limitations (Alert style)
        st.markdown("""
        <div style='background-color: #FFFAF0; padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem; border-left: 4px solid #ED8936;'>
            <h3 style='color: #C05621; margin-top: 0;'>⚠️ Limitations importantes</h3>
            <ul style='color: #744210; line-height: 1.8; margin-left: 1rem;'>
                <li>Serene n'est <strong>pas un professionnel de santé mentale</strong></li>
                <li>Serene <strong>ne remplace pas</strong> une thérapie ou un traitement médical</li>
                <li>Serene <strong>ne peut pas diagnostiquer</strong> des conditions médicales</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # Card 3: Ressources d'urgence (Emergency style)
        st.markdown("""
        <div style='background-color: #FFF5F5; padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem; border-left: 4px solid #F56565;'>
            <h3 style='color: #C53030; margin-top: 0;'>🆘 Ressources d'urgence</h3>
            <p style='color: #742A2A; line-height: 1.7; margin-bottom: 1rem;'>
                Si vous êtes en situation de crise ou avez des pensées suicidaires, <strong>contactez immédiatement</strong> :
            </p>
            <div style='background-color: white; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem;'>
                <strong style='color: #C53030; font-size: 1.2rem;'>3114</strong>
                <p style='color: #742A2A; margin: 0; font-size: 0.9rem;'>Numéro national de prévention du suicide (24/7, gratuit)</p>
            </div>
            <div style='background-color: white; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem;'>
                <strong style='color: #C53030; font-size: 1.2rem;'>15</strong>
                <p style='color: #742A2A; margin: 0; font-size: 0.9rem;'>SAMU (urgences médicales)</p>
            </div>
            <div style='background-color: white; padding: 1rem; border-radius: 8px;'>
                <strong style='color: #C53030; font-size: 1.2rem;'>09 72 39 40 50</strong>
                <p style='color: #742A2A; margin: 0; font-size: 0.9rem;'>SOS Amitié (24/7, écoute)</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Card 4: Vie privée (Success style)
        st.markdown("""
        <div style='background-color: #F0FFF4; padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem; border-left: 4px solid #48BB78;'>
            <h3 style='color: #2F855A; margin-top: 0;'>🔒 Vie privée garantie</h3>
            <p style='color: #22543D; line-height: 1.7;'>
                Toutes vos données sont <strong>stockées localement</strong> sur votre appareil.
                <strong>Aucune donnée</strong> n'est envoyée vers le cloud.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Bouton de consentement - centré
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        if st.button("✓ J'ai compris et j'accepte de continuer", type="primary", use_container_width=True):
            st.session_state.disclaimer_acknowledged = True
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
