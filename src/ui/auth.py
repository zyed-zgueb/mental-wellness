"""Interface d'authentification (Login/Signup) - Gallery Minimalist Style"""

import streamlit as st
import os
from datetime import datetime, timedelta
from src.database.db_manager import DatabaseManager
from src.utils.password_validator import (
    validate_password_strength,
    get_password_requirements,
    get_password_feedback,
    check_common_passwords
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
    <div style='text-align: center; padding: 1.5rem 2rem 1rem 2rem; animation: fadeInDown 0.4s ease-out;'>
        <h1 style='font-family: "Cormorant Garamond", serif; color: var(--black);
                   font-size: 2.5rem; font-weight: 300; margin-bottom: 0.75rem;
                   letter-spacing: 0.05em; text-transform: uppercase;'>SERENE</h1>
        <div style='width: 80px; height: 1px; background-color: var(--line-dark); margin: 1rem auto;'></div>
        <p style='font-family: "Inter", sans-serif; color: var(--gray-dark);
                 font-size: 0.9375rem; font-weight: 300; letter-spacing: 0.02em;'>
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
            scroll-margin-top: 2rem;
            position: relative;
            z-index: 10;
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

                # Initialize session timeout tracking
                init_session_timeout()

                st.success(f"Bienvenue, {st.session_state.user_display_name} !")
                st.rerun()
            else:
                st.error("Email ou mot de passe incorrect")


def show_signup_form():
    """Afficher le formulaire d'inscription avec validation de mot de passe robuste."""

    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

    st.markdown("""
    <h3 style='font-family: "Cormorant Garamond", serif; font-size: 1.5rem;
               font-weight: 300; color: var(--black); margin-bottom: 2rem;
               letter-spacing: 0.02em;'>
        Créer un compte
    </h3>
    """, unsafe_allow_html=True)

    # Email and display name
    email = st.text_input(
        "Email",
        placeholder="votre@email.com",
        key="signup_email_input"
    )

    display_name = st.text_input(
        "Nom d'affichage (optionnel)",
        placeholder="Comment souhaitez-vous être appelé ?",
        key="signup_display_name_input"
    )

    # Password with real-time validation
    password = st.text_input(
        "Mot de passe",
        type="password",
        placeholder="••••••••",
        key="signup_password_input"
    )

    password_confirm = st.text_input(
        "Confirmer le mot de passe",
        type="password",
        placeholder="••••••••",
        key="signup_password_confirm_input"
    )

    # Display password requirements with real-time checkmarks
    st.markdown("""
    <div style='background-color: #f8f9fa; padding: 1rem; border-left: 3px solid #6CB4A4; margin: 1rem 0;'>
        <strong style='font-size: 0.875rem;'>📋 Exigences du mot de passe</strong>
    </div>
    """, unsafe_allow_html=True)

    # Check requirements in real-time
    if password:
        feedback = get_password_feedback(password)

        # Display each requirement with checkmark or cross
        requirements_status = {
            "Au moins 8 caractères": len(password) >= 8,
            "Au moins une majuscule (A-Z)": any(c.isupper() for c in password),
            "Au moins une minuscule (a-z)": any(c.islower() for c in password),
            "Au moins un chiffre (0-9)": any(c.isdigit() for c in password),
            f"Au moins un caractère spécial": any(c in "@#$%^&+=!?*()-_[]{}|;:,.<>/~`" for c in password),
            "Ne doit pas être un mot de passe courant": not check_common_passwords(password)
        }

        for requirement, is_met in requirements_status.items():
            if is_met:
                st.markdown(f"✅ {requirement}")
            else:
                st.markdown(f"❌ {requirement}")
    else:
        # Show requirements without checkmarks when password is empty
        requirements = get_password_requirements()
        for req in requirements:
            st.markdown(f"⚪ {req}")

    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

    # Submit button
    submit = st.button(
        "Créer mon compte",
        use_container_width=True,
        type="primary",
        key="signup_submit_button"
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


# ============================================================================
# SESSION TIMEOUT MANAGEMENT
# ============================================================================

def get_timeout_config():
    """
    Get session timeout configuration from environment variables.

    Returns:
        dict: Configuration with timeout_minutes and warning_minutes
    """
    try:
        timeout_minutes = int(os.getenv("SESSION_TIMEOUT_MINUTES", "30"))
    except (ValueError, TypeError):
        timeout_minutes = 30  # Default to 30 minutes

    try:
        warning_minutes = int(os.getenv("SESSION_WARNING_MINUTES", "2"))
    except (ValueError, TypeError):
        warning_minutes = 2  # Default to 2 minutes

    return {
        "timeout_minutes": timeout_minutes,
        "warning_minutes": warning_minutes
    }


def init_session_timeout():
    """
    Initialize session timeout tracking.

    Sets the initial last_activity_time if not already set.
    Should be called on login.
    """
    if "last_activity_time" not in st.session_state:
        st.session_state.last_activity_time = datetime.now()


def update_activity_timestamp():
    """
    Update the last activity timestamp.

    Should be called on every user interaction.
    """
    st.session_state.last_activity_time = datetime.now()


def get_idle_minutes() -> float:
    """
    Calculate minutes since last activity.

    Returns:
        float: Minutes since last activity, or 0 if no activity recorded
    """
    if "last_activity_time" not in st.session_state:
        return 0

    now = datetime.now()
    last_activity = st.session_state.last_activity_time
    idle_time = now - last_activity
    return idle_time.total_seconds() / 60


def is_session_expired(timeout_minutes: int = None) -> bool:
    """
    Check if session has expired due to inactivity.

    Args:
        timeout_minutes: Custom timeout in minutes (uses config if None)

    Returns:
        bool: True if session is expired, False otherwise
    """
    if "last_activity_time" not in st.session_state:
        return False  # Fresh session, not expired

    if timeout_minutes is None:
        config = get_timeout_config()
        timeout_minutes = config["timeout_minutes"]

    idle_minutes = get_idle_minutes()
    return idle_minutes >= timeout_minutes


def should_show_warning(timeout_minutes: int = None, warning_minutes: int = None) -> bool:
    """
    Check if warning should be shown to user.

    Shows warning when user is close to session expiration.

    Args:
        timeout_minutes: Custom timeout in minutes (uses config if None)
        warning_minutes: Minutes before expiration to show warning (uses config if None)

    Returns:
        bool: True if warning should be shown
    """
    if "last_activity_time" not in st.session_state:
        return False

    config = get_timeout_config()
    if timeout_minutes is None:
        timeout_minutes = config["timeout_minutes"]
    if warning_minutes is None:
        warning_minutes = config["warning_minutes"]

    idle_minutes = get_idle_minutes()
    warning_threshold = timeout_minutes - warning_minutes

    return idle_minutes >= warning_threshold and idle_minutes < timeout_minutes


def handle_session_timeout():
    """
    Handle session timeout logic.

    Checks if session is expired and logs out user if necessary.
    Shows warning if user is approaching timeout.
    Provides "Extend session" button in warning.

    Should be called at the beginning of each page render.
    """
    # Skip if user is not authenticated
    if not st.session_state.get("authenticated", False):
        return

    config = get_timeout_config()
    timeout_minutes = config["timeout_minutes"]
    warning_minutes = config["warning_minutes"]

    # Check if session has expired
    if is_session_expired(timeout_minutes):
        # Log out user
        st.warning(
            f"⏱️ Votre session a expiré après {timeout_minutes} minutes d'inactivité. "
            "Vous avez été déconnecté pour des raisons de sécurité."
        )

        # Clear session state
        keys_to_clear = ["user_id", "user_email", "user_display_name", "authenticated", "current_page", "last_activity_time"]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]

        st.rerun()
        return

    # Show warning if approaching timeout
    if should_show_warning(timeout_minutes, warning_minutes):
        idle_minutes = get_idle_minutes()
        remaining_minutes = timeout_minutes - idle_minutes

        col1, col2 = st.columns([3, 1])

        with col1:
            st.warning(
                f"⚠️ Votre session va expirer dans {int(remaining_minutes)} minute(s) "
                f"en raison de l'inactivité."
            )

        with col2:
            if st.button("🔄 Prolonger", type="primary", use_container_width=True):
                update_activity_timestamp()
                st.success("✅ Session prolongée !")
                st.rerun()


def logout_user():
    """
    Log out the current user and clear session state.

    Clears all authentication-related session data.
    """
    keys_to_clear = [
        "user_id",
        "user_email",
        "user_display_name",
        "authenticated",
        "current_page",
        "last_activity_time"
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
