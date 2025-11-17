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

# Charger FontAwesome pour icônes
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
""", unsafe_allow_html=True)

# Charger le CSS unifié
st.markdown(get_main_css(), unsafe_allow_html=True)


def show_home():
    """Afficher la page d'accueil avec design accueillant."""

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
    st.markdown("### Fonctionnalités")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style='background-color: #F7FAFC; padding: 2rem; border-radius: 12px; height: 100%;
                    box-shadow: 0 1px 3px var(--color-primary-dark); border-left: 4px solid var(--color-primary);
                    transition: all 0.3s ease-out; animation: fadeInUp 0.7s ease-out;'
             onmouseover='this.style.transform="translateY(-4px)"; this.style.boxShadow="0 8px 24px rgba(107, 70, 193, 0.15)";'
             onmouseout='this.style.transform="translateY(0)"; this.style.boxShadow="0 1px 3px var(--color-primary-dark)";'>
            <h4 style='color: var(--color-primary); margin-top: 0;'>
                <i class="fa-regular fa-comments" style="margin-right: 0.5rem;"></i>Conversation Empathique
            </h4>
            <p style='color: #4A5568; line-height: 1.7;'>
                Un espace d'écoute bienveillant et sans jugement. Parlez librement de ce que vous ressentez
                avec un compagnon IA qui vous écoute vraiment.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style='background-color: #F7FAFC; padding: 2rem; border-radius: 12px; margin-top: 1rem;
                    box-shadow: 0 1px 3px var(--color-primary-dark); border-left: 4px solid #805AD5;
                    transition: all 0.3s ease-out; animation: fadeInUp 0.9s ease-out;'
             onmouseover='this.style.transform="translateY(-4px)"; this.style.boxShadow="0 8px 24px rgba(128, 90, 213, 0.15)";'
             onmouseout='this.style.transform="translateY(0)"; this.style.boxShadow="0 1px 3px var(--color-primary-dark)";'>
            <h4 style='color: #805AD5; margin-top: 0;'>
                <i class="fa-solid fa-chart-line" style="margin-right: 0.5rem;"></i>Tableau de Bord
            </h4>
            <p style='color: #4A5568; line-height: 1.7;'>
                Visualisez vos tendances de bien-être avec des graphiques élégants inspirés d'Apple Santé.
                Comprenez vos patterns émotionnels en un coup d'œil.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='background-color: #F7FAFC; padding: 2rem; border-radius: 12px; height: 100%;
                    box-shadow: 0 1px 3px var(--color-primary-dark); border-left: 4px solid #9F7AEA;
                    transition: all 0.3s ease-out; animation: fadeInUp 0.8s ease-out;'
             onmouseover='this.style.transform="translateY(-4px)"; this.style.boxShadow="0 8px 24px rgba(159, 122, 234, 0.15)";'
             onmouseout='this.style.transform="translateY(0)"; this.style.boxShadow="0 1px 3px var(--color-primary-dark)";'>
            <h4 style='color: #9F7AEA; margin-top: 0;'>
                <i class="fa-regular fa-heart-pulse" style="margin-right: 0.5rem;"></i>Quick Check-in
            </h4>
            <p style='color: #4A5568; line-height: 1.7;'>
                Suivez votre humeur au quotidien en quelques secondes. Une pratique simple qui nourrit
                vos insights personnalisés et vous aide à mieux vous comprendre.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style='background-color: #F7FAFC; padding: 2rem; border-radius: 12px; margin-top: 1rem;
                    box-shadow: 0 1px 3px var(--color-primary-dark); border-left: 4px solid #B794F4;
                    transition: all 0.3s ease-out; animation: fadeInUp 1s ease-out;'
             onmouseover='this.style.transform="translateY(-4px)"; this.style.boxShadow="0 8px 24px rgba(183, 148, 244, 0.15)";'
             onmouseout='this.style.transform="translateY(0)"; this.style.boxShadow="0 1px 3px var(--color-primary-dark)";'>
            <h4 style='color: #B794F4; margin-top: 0;'>
                <i class="fa-solid fa-lightbulb" style="margin-right: 0.5rem;"></i>Insights IA Actionnables
            </h4>
            <p style='color: #4A5568; line-height: 1.7;'>
                Recevez des révélations personnalisées sur vos patterns émotionnels. Des insights qui
                vous donnent espoir et pouvoir d'agir sur votre bien-être.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Call to action
    st.markdown("<div style='margin: 3rem 0;'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div style='background: linear-gradient(135deg, #EBF4FF 0%, #F7FAFC 100%);
                padding: 2rem; border-radius: 16px; text-align: center; border-left: 4px solid var(--color-primary);
                animation: scaleIn 0.6s ease-out; box-shadow: 0 4px 12px rgba(107, 70, 193, 0.1);
                transition: all 0.3s ease-out;'
         onmouseover='this.style.transform="scale(1.02)"; this.style.boxShadow="0 8px 24px rgba(107, 70, 193, 0.15)";'
         onmouseout='this.style.transform="scale(1)"; this.style.boxShadow="0 4px 12px rgba(107, 70, 193, 0.1)";'>
        <h3 style='color: var(--color-primary); margin-top: 0;'>Prêt à commencer ?</h3>
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
            # Logo et titre avec style épuré
            st.markdown("""
            <div style='text-align: center; padding: 1rem 0 1.5rem 0; margin-bottom: 1.5rem;
                        border-bottom: 1px solid #E2E8F0;'>
                <h1 style='font-size: 1.5rem; color: #6B46C1; margin: 0; font-weight: 600;'>Serene</h1>
            </div>
            """, unsafe_allow_html=True)

            # Initialiser la page courante si nécessaire
            if 'current_page' not in st.session_state:
                st.session_state.current_page = "Home"

            # Style CSS pour les boutons de navigation
            st.markdown("""
            <style>
            /* Fix états clicked et selected - Approche ciblée */
            section[data-testid="stSidebar"] button[kind="secondary"]:active,
            section[data-testid="stSidebar"] button[kind="secondary"]:focus {
                background-color: rgba(240, 242, 246, 0.5) !important;
                border-color: rgba(49, 51, 63, 0.1) !important;
                color: rgb(49, 51, 63) !important;
            }

            section[data-testid="stSidebar"] button[kind="primary"],
            section[data-testid="stSidebar"] button[kind="primary"]:active,
            section[data-testid="stSidebar"] button[kind="primary"]:focus {
                background-color: rgba(240, 242, 246, 0.7) !important;
                border-color: rgba(107, 70, 193, 0.3) !important;
                color: rgb(107, 70, 193) !important;
                font-weight: 500 !important;
            }

            section[data-testid="stSidebar"] button[kind="primary"]:hover {
                background-color: rgba(237, 233, 254, 0.8) !important;
                border-color: rgba(107, 70, 193, 0.5) !important;
            }
            </style>
            """, unsafe_allow_html=True)

            st.markdown("<p style='font-size: 0.75rem; color: #A0AEC0; margin-bottom: 0.5rem; padding-left: 1rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;'>Navigation</p>", unsafe_allow_html=True)

            # Navigation avec boutons épurés
            pages = {
                "Home": "Home",
                "Check-in": "Check-in",
                "Conversation": "Conversation",
                "Dashboard": "Dashboard"
            }

            for key, label in pages.items():
                if st.button(
                    label,
                    key=f"nav_{key}",
                    type="primary" if st.session_state.current_page == key else "secondary",
                    use_container_width=True
                ):
                    st.session_state.current_page = key
                    st.rerun()

            page = st.session_state.current_page

        # Afficher la page appropriée
        if page == "Home":
            show_home()
        elif page == "Check-in":
            show_checkin()
        elif page == "Conversation":
            show_conversation()
        elif page == "Dashboard":
            show_dashboard()


if __name__ == "__main__":
    main()
