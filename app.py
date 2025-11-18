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
    page_icon="◼"  # Carré noir minimaliste
)

# Charger FontAwesome pour icônes
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
""", unsafe_allow_html=True)

# Charger le CSS unifié
st.markdown(get_main_css(), unsafe_allow_html=True)


def show_home():
    """Afficher la page d'accueil - Gallery minimalist style."""

    # Hero section minimaliste
    st.markdown("""\
<div style='text-align: center; padding: 4rem 2rem; background-color: var(--white); \
border: 1px solid var(--line-light); margin-bottom: 3rem; \
animation: fadeInDown 0.6s ease-out;'>
<h1 style='font-family: "Cormorant Garamond", serif; color: var(--black); font-size: 4rem; \
font-weight: 300; margin-bottom: 1rem; letter-spacing: 0.05em; animation: fadeIn 0.8s ease-out;'>\
SERENE\
</h1>
<div style='width: 80px; height: 1px; background-color: var(--line-dark); margin: 1.5rem auto;'></div>
<p style='font-family: "Inter", sans-serif; color: var(--gray-dark); font-size: 0.9375rem; \
margin-bottom: 0; animation: fadeIn 1s ease-out; font-weight: 300; letter-spacing: 0.02em;'>\
Votre compagnon de bien-être mental\
</p>
</div>
""", unsafe_allow_html=True)

    # Introduction
    st.markdown("""\
<p style='font-family: "Inter", sans-serif; font-size: 0.9375rem; color: var(--gray-dark); \
text-align: center; margin-bottom: 4rem; line-height: 1.8; font-weight: 300; max-width: 600px; \
margin-left: auto; margin-right: auto;'>\
Serene vous accompagne avec empathie dans votre parcours de bien-être mental.<br/>\
Un espace d'écoute, de suivi et de découverte de soi.\
</p>
""", unsafe_allow_html=True)

    # Fonctionnalités - Cards minimalistes
    st.markdown("""\
<h2 style='font-family: "Cormorant Garamond", serif; font-size: 2rem; font-weight: 300; \
color: var(--black); margin-bottom: 2rem; letter-spacing: 0.02em;'>\
Fonctionnalités\
</h2>
""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""\
<div style='background-color: var(--white); padding: 2rem; border: 1px solid var(--line-light); \
height: 100%; box-shadow: var(--shadow-subtle); \
transition: all 0.3s ease-out; animation: fadeInUp 0.7s ease-out;' \
onmouseover='this.style.boxShadow="var(--shadow-soft)";' \
onmouseout='this.style.boxShadow="var(--shadow-subtle)";'>
<h4 style='font-family: "Inter", sans-serif; color: var(--black); margin-top: 0; \
font-size: 0.75rem; font-weight: 400; letter-spacing: 0.1em; text-transform: uppercase; \
margin-bottom: 1rem;'>\
<i class="fa-regular fa-comments" style='margin-right: 0.5rem; opacity: 0.7;'></i>\
Conversation Empathique\
</h4>
<p style='font-family: "Inter", sans-serif; color: var(--gray-dark); line-height: 1.8; \
font-size: 0.875rem; font-weight: 300;'>\
Un espace d'écoute bienveillant et sans jugement. Parlez librement de ce que vous ressentez \
avec un compagnon IA qui vous écoute vraiment.\
</p>
</div>
""", unsafe_allow_html=True)

        st.markdown("""\
<div style='background-color: var(--white); padding: 2rem; border: 1px solid var(--line-light); \
margin-top: 1rem; box-shadow: var(--shadow-subtle); \
transition: all 0.3s ease-out; animation: fadeInUp 0.9s ease-out;' \
onmouseover='this.style.boxShadow="var(--shadow-soft)";' \
onmouseout='this.style.boxShadow="var(--shadow-subtle)";'>
<h4 style='font-family: "Inter", sans-serif; color: var(--black); margin-top: 0; \
font-size: 0.75rem; font-weight: 400; letter-spacing: 0.1em; text-transform: uppercase; \
margin-bottom: 1rem;'>\
<i class="fa-solid fa-chart-line" style='margin-right: 0.5rem; opacity: 0.7;'></i>\
Tableau de Bord\
</h4>
<p style='font-family: "Inter", sans-serif; color: var(--gray-dark); line-height: 1.8; \
font-size: 0.875rem; font-weight: 300;'>\
Visualisez vos tendances de bien-être avec des graphiques élégants. \
Comprenez vos patterns émotionnels en un coup d'œil.\
</p>
</div>
""", unsafe_allow_html=True)

    with col2:
        st.markdown("""\
<div style='background-color: var(--white); padding: 2rem; border: 1px solid var(--line-light); \
height: 100%; box-shadow: var(--shadow-subtle); \
transition: all 0.3s ease-out; animation: fadeInUp 0.8s ease-out;' \
onmouseover='this.style.boxShadow="var(--shadow-soft)";' \
onmouseout='this.style.boxShadow="var(--shadow-subtle)";'>
<h4 style='font-family: "Inter", sans-serif; color: var(--black); margin-top: 0; \
font-size: 0.75rem; font-weight: 400; letter-spacing: 0.1em; text-transform: uppercase; \
margin-bottom: 1rem;'>\
<i class="fa-regular fa-circle-check" style='margin-right: 0.5rem; opacity: 0.7;'></i>\
Quick Check-in\
</h4>
<p style='font-family: "Inter", sans-serif; color: var(--gray-dark); line-height: 1.8; \
font-size: 0.875rem; font-weight: 300;'>\
Suivez votre humeur au quotidien en quelques secondes. Une pratique simple qui nourrit \
vos insights personnalisés et vous aide à mieux vous comprendre.\
</p>
</div>
""", unsafe_allow_html=True)

        st.markdown("""\
<div style='background-color: var(--white); padding: 2rem; border: 1px solid var(--line-light); \
margin-top: 1rem; box-shadow: var(--shadow-subtle); \
transition: all 0.3s ease-out; animation: fadeInUp 1s ease-out;' \
onmouseover='this.style.boxShadow="var(--shadow-soft)";' \
onmouseout='this.style.boxShadow="var(--shadow-subtle)";'>
<h4 style='font-family: "Inter", sans-serif; color: var(--black); margin-top: 0; \
font-size: 0.75rem; font-weight: 400; letter-spacing: 0.1em; text-transform: uppercase; \
margin-bottom: 1rem;'>\
<i class="fa-solid fa-lightbulb" style='margin-right: 0.5rem; opacity: 0.7;'></i>\
Insights IA Actionnables\
</h4>
<p style='font-family: "Inter", sans-serif; color: var(--gray-dark); line-height: 1.8; \
font-size: 0.875rem; font-weight: 300;'>\
Recevez des révélations personnalisées sur vos patterns émotionnels. Des insights qui \
vous donnent espoir et pouvoir d'agir sur votre bien-être.\
</p>
</div>
""", unsafe_allow_html=True)

    # Call to action minimaliste
    st.markdown("<div style='margin: 4rem 0 2rem 0;'></div>", unsafe_allow_html=True)

    st.markdown("""\
<div style='background-color: var(--white); padding: 3rem 2rem; border: 1px solid var(--line-light); \
text-align: center; animation: fadeInUp 0.6s ease-out; box-shadow: var(--shadow-subtle); \
transition: all 0.3s ease-out;' \
onmouseover='this.style.boxShadow="var(--shadow-soft)";' \
onmouseout='this.style.boxShadow="var(--shadow-subtle)";'>
<h3 style='font-family: "Cormorant Garamond", serif; color: var(--black); margin-top: 0; \
font-size: 1.5rem; font-weight: 300; letter-spacing: 0.02em; margin-bottom: 1rem;'>\
Prêt à commencer ?\
</h3>
<div style='width: 60px; height: 1px; background-color: var(--line-dark); margin: 1.5rem auto;'></div>
<p style='font-family: "Inter", sans-serif; color: var(--gray-dark); font-size: 0.875rem; \
margin-bottom: 0; font-weight: 300; line-height: 1.7;'>\
Utilisez le menu de navigation à gauche pour commencer votre parcours de bien-être mental.\
</p>
</div>
""", unsafe_allow_html=True)


def main():
    """Point d'entrée principal de l'application."""

    # Vérifier si l'utilisateur a reconnu le disclaimer
    if not st.session_state.get('disclaimer_acknowledged', False):
        show_disclaimer()
    else:
        # Afficher le menu de navigation dans la sidebar - Gallery minimalist
        with st.sidebar:
            # Logo et titre minimaliste
            st.markdown("""\
<div style='text-align: left; padding: 0 0 2rem 0; margin-bottom: 2rem; \
border-bottom: 1px solid var(--line-light);'>
<h1 style='font-family: "Cormorant Garamond", serif; font-size: 1.75rem; \
color: var(--black); margin: 0; font-weight: 300; letter-spacing: 0.05em; \
text-transform: uppercase;'>Serene</h1>
</div>
""", unsafe_allow_html=True)

            # Initialiser la page courante si nécessaire
            if 'current_page' not in st.session_state:
                st.session_state.current_page = "Home"

            # Style CSS pour les boutons de navigation - Textes simples avec barre
            st.markdown("""
            <style>
            /* Navigation - Textes simples avec barre fine, pas de flèches */
            section[data-testid="stSidebar"] button[kind="secondary"] {
                background-color: transparent !important;
                border: none !important;
                border-left: 1px solid transparent !important;
                border-radius: 0 !important;
                color: var(--gray-medium) !important;
                font-family: 'Inter', sans-serif !important;
                font-size: 0.875rem !important;
                font-weight: 300 !important;
                letter-spacing: 0.03em !important;
                text-transform: uppercase !important;
                padding: 0.75rem 0 0.75rem 1rem !important;
                text-align: left !important;
                box-shadow: none !important;
            }

            section[data-testid="stSidebar"] button[kind="secondary"]:hover {
                background-color: transparent !important;
                border-left-color: var(--gray-lighter) !important;
                color: var(--charcoal) !important;
            }

            /* État sélectionné - Texte noir, pas blanc */
            section[data-testid="stSidebar"] button[kind="primary"],
            section[data-testid="stSidebar"] button[kind="primary"]:active,
            section[data-testid="stSidebar"] button[kind="primary"]:focus {
                background-color: transparent !important;
                border: none !important;
                border-left: 2px solid var(--black) !important;
                border-radius: 0 !important;
                color: var(--black) !important;
                font-family: 'Inter', sans-serif !important;
                font-size: 0.875rem !important;
                font-weight: 400 !important;
                letter-spacing: 0.03em !important;
                text-transform: uppercase !important;
                padding: 0.75rem 0 0.75rem 1rem !important;
                text-align: left !important;
                box-shadow: none !important;
            }

            /* Forcer la couleur du texte intérieur à noir pour l'état sélectionné */
            section[data-testid="stSidebar"] button[kind="primary"] p,
            section[data-testid="stSidebar"] button[kind="primary"] div,
            section[data-testid="stSidebar"] button[kind="primary"] span {
                color: var(--black) !important;
            }

            section[data-testid="stSidebar"] button[kind="primary"]:hover {
                background-color: transparent !important;
            }

            /* Pas de flèches pour la navigation */
            section[data-testid="stSidebar"] button::after,
            section[data-testid="stSidebar"] button::before {
                content: none !important;
                display: none !important;
            }
            </style>
            """, unsafe_allow_html=True)

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
