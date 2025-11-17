"""
Serene - Mental Wellness AI Companion
Main Streamlit application entry point with Dark/Light Theme Support
"""
import streamlit as st
from src.ui.disclaimer import show_disclaimer
from src.ui.checkin import show_checkin
from src.ui.conversation import show_conversation
from src.ui.dashboard import show_dashboard
from src.ui.styles.serene_styles import get_main_css
from src.ui.theme_toggle import render_theme_toggle, get_current_theme

# Configuration de la page
st.set_page_config(
    page_title="Serene",
    layout="wide",
    page_icon="🌸",
    initial_sidebar_state="expanded"
)

# Initialize theme
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'  # Default to dark as requested

# Load CSS with current theme
current_theme = get_current_theme()
st.markdown(get_main_css(theme=current_theme), unsafe_allow_html=True)


def show_home():
    """Afficher la page d'accueil avec design accueillant."""

    # Hero section - Modern glassmorphism design
    st.markdown("""
    <div style='text-align: center; padding: 4rem 2rem;
                background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
                border-radius: var(--radius-xl); margin-bottom: 3rem;
                box-shadow: var(--shadow-xl), 0 0 60px var(--color-primary-glow);
                animation: fadeInDown 0.6s ease-out;
                position: relative;
                overflow: hidden;
                border: 1px solid var(--border-accent);'>
        <div style='position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
                    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
                    animation: pulse 8s infinite;'></div>
        <div style='position: relative; z-index: 1;'>
            <h1 style='color: var(--text-inverse); font-size: 3rem; margin-bottom: 1rem;
                       font-weight: 900; letter-spacing: -0.03em;
                       text-shadow: 0 2px 20px rgba(0,0,0,0.2);
                       animation: fadeIn 0.8s ease-out;'>
                Serene
            </h1>
            <p style='color: rgba(255, 255, 255, 0.95); font-size: 1.35rem; margin-bottom: 0;
                      font-weight: 500; animation: fadeIn 1s ease-out;'>
                Votre compagnon de bien-être mental
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Introduction
    st.markdown("""
    <p style='font-size: 1.15rem; color: var(--text-secondary); text-align: center;
              margin-bottom: 4rem; line-height: 1.8; font-weight: 400;'>
    Serene vous accompagne avec empathie dans votre parcours de bien-être mental.<br/>
    <span style='color: var(--text-tertiary);'>Un espace d'écoute, de suivi et de découverte de soi.</span>
    </p>
    """, unsafe_allow_html=True)

    # Fonctionnalités - Premium cards
    st.markdown("""
    <h2 style='text-align: center; font-size: 2rem; margin-bottom: 2.5rem; color: var(--text-primary);'>
        ✨ Fonctionnalités
    </h2>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div class='feature-card' style='height: 100%; animation: fadeInUp 0.7s ease-out;'>
            <div style='font-size: 2.5rem; margin-bottom: 1rem;'>💬</div>
            <h4 style='color: var(--color-primary); margin-top: 0; font-size: 1.25rem; font-weight: 700;'>
                Conversation Empathique
            </h4>
            <p style='color: var(--text-secondary); line-height: 1.8; font-size: 1rem;'>
                Un espace d'écoute bienveillant et sans jugement. Parlez librement de ce que vous ressentez
                avec un compagnon IA qui vous écoute vraiment.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div class='feature-card' style='animation: fadeInUp 0.9s ease-out;'>
            <div style='font-size: 2.5rem; margin-bottom: 1rem;'>📊</div>
            <h4 style='color: var(--color-primary); margin-top: 0; font-size: 1.25rem; font-weight: 700;'>
                Dashboard Visuel
            </h4>
            <p style='color: var(--text-secondary); line-height: 1.8; font-size: 1rem;'>
                Visualisez vos tendances de bien-être avec des graphiques élégants inspirés d'Apple Santé.
                Comprenez vos patterns émotionnels en un coup d'œil.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='feature-card' style='height: 100%; animation: fadeInUp 0.8s ease-out;'>
            <div style='font-size: 2.5rem; margin-bottom: 1rem;'>🌸</div>
            <h4 style='color: var(--color-success); margin-top: 0; font-size: 1.25rem; font-weight: 700;'>
                Quick Check-in
            </h4>
            <p style='color: var(--text-secondary); line-height: 1.8; font-size: 1rem;'>
                Suivez votre humeur au quotidien en quelques secondes. Une pratique simple qui nourrit
                vos insights personnalisés et vous aide à mieux vous comprendre.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div class='feature-card' style='animation: fadeInUp 1s ease-out;'>
            <div style='font-size: 2.5rem; margin-bottom: 1rem;'>✨</div>
            <h4 style='color: var(--color-primary); margin-top: 0; font-size: 1.25rem; font-weight: 700;'>
                Insights IA Actionnables
            </h4>
            <p style='color: var(--text-secondary); line-height: 1.8; font-size: 1rem;'>
                Recevez des révélations personnalisées sur vos patterns émotionnels. Des insights qui
                vous donnent espoir et pouvoir d'agir sur votre bien-être.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Call to action - Premium design
    st.markdown("<div style='margin: 4rem 0;'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='cta-card' style='animation: scaleIn 0.6s ease-out;'>
        <div style='font-size: 3rem; margin-bottom: 1rem; animation: bounce 2s infinite;'>🚀</div>
        <h3 style='color: var(--text-primary); margin-top: 0; font-size: 1.75rem; font-weight: 700;'>
            Prêt à commencer ?
        </h3>
        <p style='color: var(--text-secondary); font-size: 1.1rem; margin-bottom: 0; line-height: 1.7;'>
            Utilisez le menu de navigation à gauche pour commencer votre parcours de bien-être mental.<br/>
            <span style='color: var(--text-tertiary); font-size: 0.95rem;'>Chaque pas compte. 🌸</span>
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
            # Logo et titre avec modern style
            st.markdown("""
            <div style='text-align: center; padding: 2rem 0 1.5rem 0; margin-bottom: 1rem;
                        border-bottom: 2px solid var(--border-accent);'>
                <div style='font-size: 3rem; margin-bottom: 0.75rem; animation: pulse 3s infinite;
                            filter: drop-shadow(0 0 20px var(--color-primary-glow));'>🌸</div>
                <h1 class='text-gradient' style='font-size: 2rem; margin: 0; font-weight: 900; letter-spacing: -0.03em;'>
                    Serene
                </h1>
                <p style='font-size: 0.9rem; color: var(--text-tertiary); margin: 0.5rem 0 0 0; font-weight: 500;'>
                    Votre compagnon bien-être
                </p>
            </div>
            """, unsafe_allow_html=True)

            # Theme toggle
            render_theme_toggle()

            st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
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
