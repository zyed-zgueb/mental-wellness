"""Interface d'authentification (Login/Signup) - Gallery Minimalist Style"""

import streamlit as st
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


def show_auth():
    """
    Afficher la page d'authentification (Login ou Signup).

    Gère la session utilisateur via st.session_state.
    Stocke: user_id, email, display_name dans session_state après authentification réussie.
    """

    # Header minimaliste
    st.markdown("""
    <div style='text-align: center; padding: 4rem 2rem 2rem 2rem; animation: fadeInDown 0.4s ease-out;'>
        <h1 style='font-family: "Cormorant Garamond", serif; font-size: 4rem;
                   color: var(--black); font-weight: 300; margin-bottom: 1rem;
                   letter-spacing: 0.05em;'>
            SERENE
        </h1>
        <div style='width: 80px; height: 1px; background-color: var(--line-dark); margin: 1.5rem auto;'></div>
        <p style='font-family: "Inter", sans-serif; font-size: 0.9375rem;
                 color: var(--gray-dark); margin: 0; line-height: 1.8;
                 font-weight: 300;'>
            Votre compagnon de bien-être mental
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Container centré pour le formulaire
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Tabs pour Login / Signup avec style minimaliste
        st.markdown("""
        <style>
        /* Style des tabs */
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

        tab1, tab2 = st.tabs(["Connexion", "Inscription"])

        with tab1:
            show_login_form()

        with tab2:
            show_signup_form()


def show_login_form():
    """Afficher le formulaire de connexion."""

    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

    with st.form("login_form", clear_on_submit=False):
        st.markdown("""
        <h3 style='font-family: "Cormorant Garamond", serif; font-size: 1.5rem;
                   font-weight: 300; color: var(--black); margin-bottom: 2rem;
                   letter-spacing: 0.02em;'>
            Bienvenue
        </h3>
        """, unsafe_allow_html=True)

        email = st.text_input(
            "Email",
            placeholder="votre@email.com",
            key="login_email"
        )

        password = st.text_input(
            "Mot de passe",
            type="password",
            placeholder="••••••••",
            key="login_password"
        )

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

        submit = st.form_submit_button(
            "Se connecter",
            use_container_width=True,
            type="primary"
        )

        if submit:
            if not email or not password:
                st.error("Veuillez remplir tous les champs")
                return

            db = get_database()
            user = db.authenticate_user(email, password)

            if user:
                # Stocker les infos utilisateur dans session_state
                st.session_state.user_id = user["id"]
                st.session_state.user_email = user["email"]
                st.session_state.user_display_name = user.get("display_name") or email.split("@")[0]
                st.session_state.authenticated = True

                st.success(f"Bienvenue, {st.session_state.user_display_name} !")
                st.rerun()
            else:
                st.error("Email ou mot de passe incorrect")


def show_signup_form():
    """Afficher le formulaire d'inscription avec validation de mot de passe robuste."""

    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

    with st.form("signup_form", clear_on_submit=True):
        st.markdown("""
        <h3 style='font-family: "Cormorant Garamond", serif; font-size: 1.5rem;
                   font-weight: 300; color: var(--black); margin-bottom: 2rem;
                   letter-spacing: 0.02em;'>
            Créer un compte
        </h3>
        """, unsafe_allow_html=True)

        email = st.text_input(
            "Email",
            placeholder="votre@email.com",
            key="signup_email"
        )

        display_name = st.text_input(
            "Nom d'affichage (optionnel)",
            placeholder="Comment souhaitez-vous être appelé ?",
            key="signup_display_name"
        )

        password = st.text_input(
            "Mot de passe",
            type="password",
            placeholder="••••••••",
            key="signup_password"
        )

        # Display password requirements
        with st.expander("📋 Exigences du mot de passe", expanded=False):
            requirements = get_password_requirements()
            for req in requirements:
                st.markdown(f"- {req}")

        password_confirm = st.text_input(
            "Confirmer le mot de passe",
            type="password",
            placeholder="••••••••",
            key="signup_password_confirm"
        )

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

        submit = st.form_submit_button(
            "Créer mon compte",
            use_container_width=True,
            type="primary"
        )

        if submit:
            # Basic validation
            if not email or not password:
                st.error("📧 Email et mot de passe sont requis")
                return

            if password != password_confirm:
                st.error("🔒 Les mots de passe ne correspondent pas")
                return

            # Strong password validation
            is_valid, message = validate_password_strength(password)
            if not is_valid:
                st.error(f"❌ **Mot de passe invalide**: {message}")

                # Show detailed feedback
                feedback = get_password_feedback(password)
                if feedback["messages"]:
                    st.warning("**Améliorations nécessaires:**")
                    for msg in feedback["messages"]:
                        st.write(f"  • {msg}")
                return

            # Create user
            db = get_database()
            try:
                user_id = db.create_user(
                    email=email,
                    password=password,
                    display_name=display_name if display_name else None
                )

                st.success("✅ Compte créé avec succès !")
                st.info("👉 Vous pouvez maintenant vous connecter dans l'onglet 'Connexion'")

            except ValueError as e:
                st.error(f"❌ Erreur: {e}")


def show_user_menu():
    """
    Afficher le menu utilisateur dans la sidebar (après authentification).

    Affiche le nom de l'utilisateur et un bouton de déconnexion.
    """
    if not st.session_state.get("authenticated"):
        return

    st.markdown("""
    <div style='padding: 1rem; border: 1px solid var(--line-light);
                background-color: var(--ivory-dark); margin-bottom: 2rem;'>
        <div style='font-family: "Inter", sans-serif; font-size: 0.6875rem;
                   color: var(--gray-medium); text-transform: uppercase;
                   letter-spacing: 0.1em; margin-bottom: 0.5rem;'>
            Connecté en tant que
        </div>
        <div style='font-family: "Inter", sans-serif; font-size: 0.9375rem;
                   color: var(--black); font-weight: 400;'>
            {display_name}
        </div>
    </div>
    """.format(display_name=st.session_state.get("user_display_name", "Utilisateur")),
    unsafe_allow_html=True)

    if st.button("Se déconnecter", use_container_width=True, type="secondary"):
        # Clear session state
        keys_to_clear = ["user_id", "user_email", "user_display_name", "authenticated", "current_page"]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()


def is_authenticated() -> bool:
    """
    Vérifier si l'utilisateur est authentifié.

    Returns:
        True si authentifié, False sinon.
    """
    return st.session_state.get("authenticated", False)


def get_current_user_id() -> int:
    """
    Récupérer l'ID de l'utilisateur actuel.

    Returns:
        User ID si authentifié, None sinon.
    """
    return st.session_state.get("user_id")
