"""
Serene - Mental Wellness AI Companion
Main Streamlit application entry point
"""
import streamlit as st
from src.ui.disclaimer import show_disclaimer
from src.ui.checkin import show_checkin
from src.ui.conversation import show_conversation
from src.ui.dashboard import show_dashboard
from src.ui.styles.serene_styles import get_main_css

# Configuration de la page
st.set_page_config(
    page_title="Serene",
    layout="wide",
    page_icon="🌸"
)

# Charger le CSS unifié
st.markdown(get_main_css(), unsafe_allow_html=True)


def show_home():
    """Afficher la page d'accueil avec design accueillant."""

    # Styles CSS pour les cartes interactives
    st.markdown("""
    <style>
    .feature-card {
        background-color: #F7FAFC;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(107, 70, 193, 0.1);
        transition: all 0.3s ease-out;
    }
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(107, 70, 193, 0.15);
    }
    .cta-card {
        background: linear-gradient(135deg, #EBF4FF 0%, #F7FAFC 100%);
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        border-left: 4px solid var(--color-primary);
        box-shadow: 0 4px 12px rgba(107, 70, 193, 0.1);
        transition: all 0.3s ease-out;
    }
    .cta-card:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 24px rgba(107, 70, 193, 0.15);
    }
    </style>
    """, unsafe_allow_html=True)

    # Hero section avec gradient et animation
    st.markdown("""
    <div style='text-align: center; padding: 3rem 1rem; background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
                border-radius: 16px; margin-bottom: 2rem; box-shadow: 0 4px 12px var(--text-primary);
                animation: fadeInDown 0.6s ease-out;'>
        <h1 style='color: white; font-size: 3rem; margin-bottom: 0.5rem; animation: fadeIn 0.8s ease-out;'>Serene</h1>
        <p style='color: var(--text-primary); font-size: 1.3rem; margin-bottom: 0; animation: fadeIn 1s ease-out;'>
            Votre compagnon de bien-être mental
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Introduction
    st.markdown("""
    <p style='font-size: 1.1rem; color: #4A5568; text-align: center; margin-bottom: 3rem; line-height: 1.7;'>
    Serene vous accompagne avec empathie dans votre parcours de bien-être mental.<br/>
    Un espace d'écoute, de suivi et de découverte de soi.
    </p>
    """, unsafe_allow_html=True)

    # Fonctionnalités - Cards élégantes
    st.markdown("### ✨ Fonctionnalités")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class='feature-card' style='height: 100%; border-left: 4px solid var(--color-primary); animation: fadeInUp 0.7s ease-out;'>
            <h4 style='color: var(--color-primary); margin-top: 0;'>💬 Conversation Empathique</h4>
            <p style='color: #4A5568; line-height: 1.7;'>
                Un espace d'écoute bienveillant et sans jugement. Parlez librement de ce que vous ressentez
                avec un compagnon IA qui vous écoute vraiment.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='feature-card' style='margin-top: 1rem; border-left: 4px solid #805AD5; animation: fadeInUp 0.9s ease-out;'>
            <h4 style='color: #805AD5; margin-top: 0;'>📊 Dashboard Visuel</h4>
            <p style='color: #4A5568; line-height: 1.7;'>
                Visualisez vos tendances de bien-être avec des graphiques élégants inspirés d'Apple Santé.
                Comprenez vos patterns émotionnels en un coup d'œil.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='feature-card' style='height: 100%; border-left: 4px solid #9F7AEA; animation: fadeInUp 0.8s ease-out;'>
            <h4 style='color: #9F7AEA; margin-top: 0;'>🌸 Quick Check-in</h4>
            <p style='color: #4A5568; line-height: 1.7;'>
                Suivez votre humeur au quotidien en quelques secondes. Une pratique simple qui nourrit
                vos insights personnalisés et vous aide à mieux vous comprendre.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='feature-card' style='margin-top: 1rem; border-left: 4px solid #B794F4; animation: fadeInUp 1s ease-out;'>
            <h4 style='color: #B794F4; margin-top: 0;'>✨ Insights IA Actionnables</h4>
            <p style='color: #4A5568; line-height: 1.7;'>
                Recevez des révélations personnalisées sur vos patterns émotionnels. Des insights qui
                vous donnent espoir et pouvoir d'agir sur votre bien-être.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Call to action
    st.markdown("<div style='margin: 3rem 0;'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='cta-card' style='animation: scaleIn 0.6s ease-out;'>
        <h3 style='color: var(--color-primary); margin-top: 0;'>✨ Prêt à commencer ?</h3>
        <p style='color: #4A5568; font-size: 1.05rem; margin-bottom: 0;'>
            Utilisez le menu de navigation à gauche pour commencer votre parcours de bien-être mental.
        </p>
    </div>
    """, unsafe_allow_html=True)


def main():
    """Point d'entrée principal de l'application."""

    # Vérifier si l'utilisateur a reconnu le disclaimer
    if not st.session_state.get('disclaimer_acknowledged', False):
        show_disclaimer()
    else:
        # Afficher le menu de navigation dans la sidebar
        with st.sidebar:
            # Logo et titre avec style
            st.markdown("""
            <div style='text-align: center; padding: 1.5rem 0; margin-bottom: 1.5rem;
                        border-bottom: 2px solid rgba(107, 70, 193, 0.1);'>
                <div style='font-size: 2.5rem; margin-bottom: 0.5rem; animation: pulse 3s infinite;'>🌸</div>
                <h1 style='font-size: 1.75rem; color: var(--color-primary); margin: 0; font-weight: 700;'>Serene</h1>
                <p style='font-size: 0.85rem; color: #718096; margin: 0.5rem 0 0 0;'>Votre compagnon bien-être</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("### 📍 Navigation")

            page = st.radio(
                "Sélectionner une page",
                [
                    "🏠 Home",
                    "🌸 Quick Check-in",
                    "💬 Conversation",
                    "📊 Dashboard"
                ],
                index=0,
                label_visibility="hidden"
            )

        # Afficher la page appropriée
        if "Home" in page:
            show_home()
        elif "Check-in" in page:
            show_checkin()
        elif "Conversation" in page:
            show_conversation()
        elif "Dashboard" in page:
            show_dashboard()


if __name__ == "__main__":
    main()
