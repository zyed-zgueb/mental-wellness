"""Interface de profil utilisateur - Gallery Minimalist Style"""

import streamlit as st
import json
from datetime import datetime
from src.database.db_manager import DatabaseManager
from src.utils.password_validator import (
    validate_password_strength,
    get_password_requirements,
    get_password_feedback
)


@st.cache_resource
def get_database():
    """Singleton DatabaseManager."""
    return DatabaseManager("serene.db")


def show_profile():
    """
    Afficher la page de profil utilisateur.

    Permet de modifier:
    - Informations personnelles (nom, année de naissance, zone)
    - Nom d'affichage
    - Préférences (fréquence de rappels, objectifs)
    - Mot de passe
    - Export des données (RGPD)
    """

    # Header
    st.markdown("""
    <div style='margin-bottom: 3rem;'>
        <h1 style='font-family: "Cormorant Garamond", serif; font-size: 3rem;
                   color: var(--black); font-weight: 300; margin-bottom: 0.5rem;
                   letter-spacing: 0.02em;'>
            Mon Profil
        </h1>
        <div style='width: 60px; height: 1px; background-color: var(--line-dark); margin: 1rem 0;'></div>
        <p style='font-family: "Inter", sans-serif; font-size: 0.875rem;
                 color: var(--gray-dark); margin: 0; font-weight: 300;'>
            Gérez vos informations personnelles et préférences
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Get current user data
    db = get_database()
    user_id = st.session_state.get("user_id")
    user = db.get_user_by_id(user_id)

    if not user:
        st.error("Erreur: utilisateur introuvable")
        return

    # Tabs pour organiser le profil
    st.markdown("""
    <style>
    /* Style des tabs pour le profil */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        border-bottom: 1px solid var(--line-light);
    }

    .stTabs [data-baseweb="tab"] {
        font-family: "Inter", sans-serif;
        font-size: 0.75rem;
        font-weight: 400;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--gray-medium);
        background-color: transparent;
        border: none;
        border-bottom: 2px solid transparent;
        padding: 1rem 2rem;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: var(--charcoal);
    }

    .stTabs [aria-selected="true"] {
        color: var(--black);
        border-bottom-color: var(--black);
    }
    </style>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "Informations personnelles",
        "Préférences",
        "Sécurité",
        "Données (RGPD)"
    ])

    with tab1:
        show_personal_info_section(user, db)

    with tab2:
        show_preferences_section(user, db)

    with tab3:
        show_security_section(user, db)

    with tab4:
        show_data_export_section(user, db)


def show_personal_info_section(user, db):
    """Section d'informations personnelles."""

    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

    st.markdown("""
    <h3 style='font-family: "Cormorant Garamond", serif; font-size: 1.5rem;
               font-weight: 300; color: var(--black); margin-bottom: 2rem;
               letter-spacing: 0.02em;'>
        Informations personnelles
    </h3>
    """, unsafe_allow_html=True)

    with st.form("personal_info_form"):
        # Email (read-only)
        st.text_input(
            "Email",
            value=user["email"],
            disabled=True,
            help="L'email ne peut pas être modifié"
        )

        # Display name
        display_name = st.text_input(
            "Nom d'affichage",
            value=user.get("display_name") or "",
            placeholder="Comment souhaitez-vous être appelé ?",
            help="Ce nom sera utilisé dans l'application"
        )

        # Full name
        full_name = st.text_input(
            "Nom complet",
            value=user.get("full_name") or "",
            placeholder="Votre nom complet (optionnel)"
        )

        # Birth year
        current_year = datetime.now().year
        birth_year = st.number_input(
            "Année de naissance",
            min_value=1900,
            max_value=current_year,
            value=user.get("birth_year") or None,
            step=1,
            help="Optionnel - nous aide à personnaliser votre expérience"
        )

        # Timezone
        timezone = st.text_input(
            "Zone géographique / Fuseau horaire",
            value=user.get("timezone") or "",
            placeholder="Ex: Europe/Paris, America/New_York",
            help="Optionnel - pour les rappels personnalisés"
        )

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

        submit = st.form_submit_button(
            "Enregistrer les modifications",
            use_container_width=True,
            type="primary"
        )

        if submit:
            try:
                db.update_user_profile(
                    user_id=user["id"],
                    display_name=display_name if display_name else None,
                    full_name=full_name if full_name else None,
                    birth_year=int(birth_year) if birth_year else None,
                    timezone=timezone if timezone else None
                )

                # Update session state
                if display_name:
                    st.session_state.user_display_name = display_name

                st.success("✅ Profil mis à jour avec succès !")
                st.rerun()

            except Exception as e:
                st.error(f"❌ Erreur lors de la mise à jour: {e}")


def show_preferences_section(user, db):
    """Section des préférences."""

    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

    st.markdown("""
    <h3 style='font-family: "Cormorant Garamond", serif; font-size: 1.5rem;
               font-weight: 300; color: var(--black); margin-bottom: 2rem;
               letter-spacing: 0.02em;'>
        Préférences
    </h3>
    """, unsafe_allow_html=True)

    # Get current preferences
    current_prefs = db.get_user_preferences(user["id"])

    with st.form("preferences_form"):
        # Reminder frequency
        st.markdown("""
        <p style='font-family: "Inter", sans-serif; font-size: 0.875rem;
                 color: var(--charcoal); font-weight: 400; margin-bottom: 0.5rem;'>
            Fréquence des rappels de check-in
        </p>
        """, unsafe_allow_html=True)

        reminder_frequency = st.selectbox(
            "Fréquence des rappels",
            options=["daily", "twice_daily", "weekly", "none"],
            format_func=lambda x: {
                "daily": "Quotidien (1x par jour)",
                "twice_daily": "Bi-quotidien (2x par jour)",
                "weekly": "Hebdomadaire",
                "none": "Aucun rappel"
            }[x],
            index=["daily", "twice_daily", "weekly", "none"].index(
                current_prefs.get("reminder_frequency", "daily")
            ),
            label_visibility="collapsed"
        )

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

        # Personal goals
        st.markdown("""
        <p style='font-family: "Inter", sans-serif; font-size: 0.875rem;
                 color: var(--charcoal); font-weight: 400; margin-bottom: 0.5rem;'>
            Objectifs personnels
        </p>
        """, unsafe_allow_html=True)

        personal_goals = st.text_area(
            "Objectifs personnels",
            value=current_prefs.get("personal_goals", ""),
            placeholder="Quels sont vos objectifs de bien-être mental ?",
            height=100,
            help="Ces objectifs peuvent aider à personnaliser les insights",
            label_visibility="collapsed"
        )

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

        # Preferred conversation tone
        st.markdown("""
        <p style='font-family: "Inter", sans-serif; font-size: 0.875rem;
                 color: var(--charcoal); font-weight: 400; margin-bottom: 0.5rem;'>
            Ton de conversation préféré
        </p>
        """, unsafe_allow_html=True)

        conversation_tone = st.selectbox(
            "Ton de conversation",
            options=["empathetic", "professional", "casual", "motivational"],
            format_func=lambda x: {
                "empathetic": "Empathique (par défaut)",
                "professional": "Professionnel",
                "casual": "Décontracté",
                "motivational": "Motivant"
            }[x],
            index=["empathetic", "professional", "casual", "motivational"].index(
                current_prefs.get("conversation_tone", "empathetic")
            ),
            label_visibility="collapsed"
        )

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

        # Insights frequency
        st.markdown("""
        <p style='font-family: "Inter", sans-serif; font-size: 0.875rem;
                 color: var(--charcoal); font-weight: 400; margin-bottom: 0.5rem;'>
            Fréquence des insights personnalisés
        </p>
        """, unsafe_allow_html=True)

        insights_frequency = st.selectbox(
            "Fréquence des insights",
            options=["weekly", "biweekly", "monthly"],
            format_func=lambda x: {
                "weekly": "Hebdomadaire",
                "biweekly": "Bi-hebdomadaire",
                "monthly": "Mensuel"
            }[x],
            index=["weekly", "biweekly", "monthly"].index(
                current_prefs.get("insights_frequency", "weekly")
            ),
            label_visibility="collapsed"
        )

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

        submit = st.form_submit_button(
            "Enregistrer les préférences",
            use_container_width=True,
            type="primary"
        )

        if submit:
            try:
                new_prefs = {
                    "reminder_frequency": reminder_frequency,
                    "personal_goals": personal_goals,
                    "conversation_tone": conversation_tone,
                    "insights_frequency": insights_frequency
                }

                db.update_user_preferences(user["id"], new_prefs)
                st.success("✅ Préférences mises à jour avec succès !")
                st.rerun()

            except Exception as e:
                st.error(f"❌ Erreur lors de la mise à jour: {e}")


def show_security_section(user, db):
    """Section de sécurité (changement de mot de passe)."""

    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

    st.markdown("""
    <h3 style='font-family: "Cormorant Garamond", serif; font-size: 1.5rem;
               font-weight: 300; color: var(--black); margin-bottom: 2rem;
               letter-spacing: 0.02em;'>
        Sécurité
    </h3>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style='font-family: "Inter", sans-serif; font-size: 0.875rem;
             color: var(--gray-dark); margin-bottom: 2rem; font-weight: 300;'>
        Modifiez votre mot de passe pour sécuriser votre compte.
    </p>
    """, unsafe_allow_html=True)

    with st.form("password_form"):
        current_password = st.text_input(
            "Mot de passe actuel",
            type="password",
            placeholder="••••••••"
        )

        new_password = st.text_input(
            "Nouveau mot de passe",
            type="password",
            placeholder="••••••••"
        )

        # Display password requirements
        with st.expander("📋 Exigences du mot de passe", expanded=False):
            requirements = get_password_requirements()
            for req in requirements:
                st.markdown(f"- {req}")

        confirm_password = st.text_input(
            "Confirmer le nouveau mot de passe",
            type="password",
            placeholder="••••••••"
        )

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

        submit = st.form_submit_button(
            "Changer le mot de passe",
            use_container_width=True,
            type="primary"
        )

        if submit:
            # Validation
            if not current_password or not new_password or not confirm_password:
                st.error("⚠️ Veuillez remplir tous les champs")
                return

            # Verify current password
            auth_user = db.authenticate_user(user["email"], current_password)
            if not auth_user:
                st.error("❌ Mot de passe actuel incorrect")
                return

            # Strong password validation
            is_valid, message = validate_password_strength(new_password)
            if not is_valid:
                st.error(f"❌ **Nouveau mot de passe invalide**: {message}")

                # Show detailed feedback
                feedback = get_password_feedback(new_password)
                if feedback["messages"]:
                    st.warning("**Améliorations nécessaires:**")
                    for msg in feedback["messages"]:
                        st.write(f"  • {msg}")
                return

            if new_password != confirm_password:
                st.error("🔒 Les mots de passe ne correspondent pas")
                return

            try:
                db.change_password(user["id"], new_password)
                st.success("✅ Mot de passe changé avec succès !")

            except Exception as e:
                st.error(f"❌ Erreur lors du changement de mot de passe: {e}")


def show_data_export_section(user, db):
    """Section d'export des données (RGPD)."""

    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

    st.markdown("""
    <h3 style='font-family: "Cormorant Garamond", serif; font-size: 1.5rem;
               font-weight: 300; color: var(--black); margin-bottom: 2rem;
               letter-spacing: 0.02em;'>
        Export de vos données (RGPD)
    </h3>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style='font-family: "Inter", sans-serif; font-size: 0.875rem;
             color: var(--gray-dark); margin-bottom: 2rem; font-weight: 300; line-height: 1.8;'>
        Conformément au RGPD, vous avez le droit d'exporter toutes vos données personnelles.
        Cela inclut votre profil, vos check-ins, vos conversations et vos insights.
    </p>
    """, unsafe_allow_html=True)

    # Info box
    st.markdown("""
    <div style='background-color: var(--ivory-dark); padding: 1.5rem;
                border: 1px solid var(--line-light); margin-bottom: 2rem;'>
        <p style='font-family: "Inter", sans-serif; font-size: 0.75rem;
                 color: var(--gray-dark); margin: 0; font-weight: 300; line-height: 1.7;'>
            <strong style='color: var(--charcoal);'>Données exportées :</strong><br/>
            • Profil utilisateur (email, nom, préférences)<br/>
            • Tous vos check-ins d'humeur<br/>
            • Toutes vos conversations avec l'IA<br/>
            • Tous les insights générés pour vous<br/>
            • Horodatage de l'export
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button(
        "Télécharger mes données (JSON)",
        use_container_width=True,
        type="primary"
    ):
        try:
            # Export user data
            export_data = db.export_user_data(user["id"])

            # Convert to JSON
            json_data = json.dumps(export_data, indent=2, ensure_ascii=False)

            # Create download button
            st.download_button(
                label="📥 Télécharger le fichier JSON",
                data=json_data,
                file_name=f"serene_export_{user['email']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )

            st.success(f"✅ Export généré avec succès ! ({len(export_data['check_ins'])} check-ins, {len(export_data['conversations'])} conversations, {len(export_data['insights'])} insights)")

        except Exception as e:
            st.error(f"❌ Erreur lors de l'export: {e}")

    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

    # Additional info
    st.markdown("""
    <div style='background-color: var(--white); padding: 1.5rem;
                border: 1px solid var(--line-light);'>
        <p style='font-family: "Inter", sans-serif; font-size: 0.6875rem;
                 color: var(--gray-medium); margin: 0; font-weight: 300;
                 line-height: 1.7; text-transform: uppercase; letter-spacing: 0.05em;'>
            Note sur la confidentialité
        </p>
        <p style='font-family: "Inter", sans-serif; font-size: 0.75rem;
                 color: var(--gray-dark); margin: 0.75rem 0 0 0; font-weight: 300; line-height: 1.7;'>
            Vos données sont stockées localement et ne sont jamais partagées avec des tiers.
            L'export contient toutes vos données mais exclut votre mot de passe hashé pour des raisons de sécurité.
        </p>
    </div>
    """, unsafe_allow_html=True)
