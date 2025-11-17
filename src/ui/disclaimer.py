"""Disclaimer screen for Serene application - Gallery Minimalist Style"""
import streamlit as st

try:
    from streamlit_shadcn_ui import card, badge, alert
    SHADCN_AVAILABLE = True
except ImportError:
    SHADCN_AVAILABLE = False


def show_disclaimer():
    """Afficher l'écran d'avertissement et de consentement - Gallery minimalist style."""

    # Centered layout
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Header minimaliste
        st.markdown("""
        <div style='text-align: center; margin-bottom: 3rem; padding-bottom: 2rem;
                    border-bottom: 1px solid var(--line-light);'>
            <h1 style='font-family: "Cormorant Garamond", serif; color: var(--black);
                       font-size: 3rem; font-weight: 300; margin-bottom: 1rem;
                       letter-spacing: 0.05em; text-transform: uppercase;'>
                SERENE
            </h1>
            <div style='width: 80px; height: 1px; background-color: var(--line-dark); margin: 1.5rem auto;'></div>
            <p style='font-family: "Inter", sans-serif; color: var(--gray-dark);
                     font-size: 0.9375rem; font-weight: 300; letter-spacing: 0.02em;'>
                Votre compagnon de bien-être mental
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Card 1: À propos
        st.markdown("""
        <div style='background-color: var(--white); padding: 2rem; border: 1px solid var(--line-light);
                    margin-bottom: 1.5rem; box-shadow: var(--shadow-subtle);'>
            <h3 style='font-family: "Inter", sans-serif; color: var(--black); margin-top: 0;
                       font-size: 0.75rem; font-weight: 400; letter-spacing: 0.1em;
                       text-transform: uppercase; margin-bottom: 1rem;'>
                À propos
            </h3>
            <p style='font-family: "Inter", sans-serif; color: var(--gray-dark);
                     line-height: 1.8; font-size: 0.9375rem; font-weight: 300; margin: 0;'>
                Serene est un compagnon d'intelligence artificielle conçu pour accompagner
                votre bien-être mental avec empathie et bienveillance.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Card 2: Limitations
        st.markdown("""
        <div style='background-color: var(--white); padding: 2rem; border: 1px solid var(--line-light);
                    border-left: 2px solid var(--black); margin-bottom: 1.5rem;
                    box-shadow: var(--shadow-subtle);'>
            <h3 style='font-family: "Inter", sans-serif; color: var(--black); margin-top: 0;
                       font-size: 0.75rem; font-weight: 400; letter-spacing: 0.1em;
                       text-transform: uppercase; margin-bottom: 1rem;'>
                Limitations importantes
            </h3>
            <ul style='font-family: "Inter", sans-serif; color: var(--gray-dark);
                      line-height: 1.8; font-size: 0.875rem; font-weight: 300;
                      margin: 0; padding-left: 1.5rem;'>
                <li style='margin-bottom: 0.5rem;'>Serene n'est <strong>pas un professionnel de santé mentale</strong></li>
                <li style='margin-bottom: 0.5rem;'>Serene <strong>ne remplace pas</strong> une thérapie ou un traitement médical</li>
                <li>Serene <strong>ne peut pas diagnostiquer</strong> des conditions médicales</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # Card 3: Ressources d'urgence
        st.markdown("""
        <div style='background-color: var(--white); padding: 2rem; border: 1px solid var(--line-light);
                    border-left: 2px solid var(--black); margin-bottom: 1.5rem;
                    box-shadow: var(--shadow-subtle);'>
            <h3 style='font-family: "Inter", sans-serif; color: var(--black); margin-top: 0;
                       font-size: 0.75rem; font-weight: 400; letter-spacing: 0.1em;
                       text-transform: uppercase; margin-bottom: 1rem;'>
                Ressources d'urgence
            </h3>
            <p style='font-family: "Inter", sans-serif; color: var(--gray-dark);
                     line-height: 1.8; font-size: 0.875rem; font-weight: 300; margin-bottom: 1.5rem;'>
                Si vous êtes en situation de crise ou avez des pensées suicidaires,
                <strong>contactez immédiatement</strong> :
            </p>
            <div style='background-color: var(--ivory-dark); padding: 1rem 1.5rem;
                        border: 1px solid var(--line-light); margin-bottom: 0.75rem;'>
                <div style='font-family: "Cormorant Garamond", serif; color: var(--black);
                           font-size: 2rem; font-weight: 300; margin-bottom: 0.25rem;'>3114</div>
                <p style='font-family: "Inter", sans-serif; color: var(--gray-medium);
                         margin: 0; font-size: 0.75rem; text-transform: uppercase;
                         letter-spacing: 0.05em;'>
                    Prévention du suicide (24/7, gratuit)
                </p>
            </div>
            <div style='background-color: var(--ivory-dark); padding: 1rem 1.5rem;
                        border: 1px solid var(--line-light); margin-bottom: 0.75rem;'>
                <div style='font-family: "Cormorant Garamond", serif; color: var(--black);
                           font-size: 2rem; font-weight: 300; margin-bottom: 0.25rem;'>15</div>
                <p style='font-family: "Inter", sans-serif; color: var(--gray-medium);
                         margin: 0; font-size: 0.75rem; text-transform: uppercase;
                         letter-spacing: 0.05em;'>
                    SAMU (urgences médicales)
                </p>
            </div>
            <div style='background-color: var(--ivory-dark); padding: 1rem 1.5rem;
                        border: 1px solid var(--line-light);'>
                <div style='font-family: "Cormorant Garamond", serif; color: var(--black);
                           font-size: 1.5rem; font-weight: 300; margin-bottom: 0.25rem;'>09 72 39 40 50</div>
                <p style='font-family: "Inter", sans-serif; color: var(--gray-medium);
                         margin: 0; font-size: 0.75rem; text-transform: uppercase;
                         letter-spacing: 0.05em;'>
                    SOS Amitié (24/7, écoute)
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Card 4: Vie privée
        st.markdown("""
        <div style='background-color: var(--white); padding: 2rem; border: 1px solid var(--line-light);
                    margin-bottom: 2rem; box-shadow: var(--shadow-subtle);'>
            <h3 style='font-family: "Inter", sans-serif; color: var(--black); margin-top: 0;
                       font-size: 0.75rem; font-weight: 400; letter-spacing: 0.1em;
                       text-transform: uppercase; margin-bottom: 1rem;'>
                Vie privée garantie
            </h3>
            <p style='font-family: "Inter", sans-serif; color: var(--gray-dark);
                     line-height: 1.8; font-size: 0.9375rem; font-weight: 300; margin: 0;'>
                Toutes vos données sont <strong>stockées localement</strong> sur votre appareil.
                <strong>Aucune donnée</strong> n'est envoyée vers le cloud.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Bouton de consentement minimaliste
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        if st.button("J'ai compris et j'accepte de continuer", type="primary", use_container_width=True):
            st.session_state.disclaimer_acknowledged = True
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
