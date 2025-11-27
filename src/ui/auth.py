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

    # Custom CSS for the auth page
    st.markdown("""
    <style>
    /* Hide Streamlit elements for full-screen auth */
    [data-testid="stSidebar"] {
        display: none !important;
    }

    /* Full-screen layout */
    .main .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    /* Auth container styling */
    .auth-container {
        display: flex;
        min-height: 100vh;
        width: 100%;
    }

    /* Left column - Form */
    .auth-form-column {
        flex: 1;
        background-color: #F5F5F5;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem;
    }

    /* Right column - Illustration */
    .auth-illustration-column {
        flex: 1;
        background: linear-gradient(135deg, #7B9FD3 0%, #9FC4E7 50%, #A8E6CF 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 4rem;
        color: white;
        text-align: center;
    }

    /* Form card */
    .auth-form-card {
        background: white;
        border-radius: 24px;
        padding: 3rem 2.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        max-width: 440px;
        width: 100%;
    }

    /* Title styling */
    .auth-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.75rem;
        font-weight: 600;
        color: #1A1A1A;
        margin-bottom: 0.5rem;
        line-height: 1.3;
    }

    /* Input container with icon */
    .input-with-icon {
        position: relative;
        margin-bottom: 1rem;
    }

    .input-icon {
        position: absolute;
        left: 16px;
        top: 50%;
        transform: translateY(-50%);
        color: #9E9E9E;
        font-size: 1.125rem;
        pointer-events: none;
        z-index: 10;
    }

    /* Custom input styling */
    .stTextInput input {
        padding-left: 48px !important;
        border-radius: 12px !important;
        border: 1px solid #E0E0E0 !important;
        padding-top: 0.75rem !important;
        padding-bottom: 0.75rem !important;
        font-size: 0.9375rem !important;
    }

    .stTextInput input:focus {
        border-color: #6CB4A4 !important;
        box-shadow: 0 0 0 3px rgba(108, 180, 164, 0.1) !important;
    }

    /* Password show button */
    .password-show-btn {
        position: absolute;
        right: 16px;
        top: 50%;
        transform: translateY(-50%);
        background: none;
        border: none;
        color: #6CB4A4;
        font-size: 0.875rem;
        font-weight: 500;
        cursor: pointer;
        z-index: 10;
    }

    /* Sign in button - Turquoise */
    button[kind="primaryFormSubmit"] {
        background-color: #6CB4A4 !important;
        background: #6CB4A4 !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 0.875rem 1.5rem !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        border: none !important;
        width: 100% !important;
        margin-top: 1.5rem !important;
        text-transform: none !important;
        letter-spacing: normal !important;
    }

    button[kind="primaryFormSubmit"]:hover {
        background-color: #5A9E8E !important;
        background: #5A9E8E !important;
    }

    /* Forgot password link */
    .forgot-password {
        text-align: center;
        margin-top: 1rem;
        margin-bottom: 1.5rem;
    }

    .forgot-password a {
        color: #6CB4A4;
        font-size: 0.875rem;
        text-decoration: none;
        font-weight: 500;
    }

    /* Social buttons */
    .social-buttons {
        display: flex;
        gap: 1rem;
        margin-top: 1.5rem;
    }

    .social-button {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0.75rem;
        border: 1px solid #E0E0E0;
        border-radius: 12px;
        background: white;
        cursor: pointer;
        transition: all 0.2s;
    }

    .social-button:hover {
        border-color: #B0B0B0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    .social-button img {
        width: 24px;
        height: 24px;
    }

    /* Sign up link */
    .signup-link {
        text-align: center;
        margin-top: 2rem;
        font-size: 0.9375rem;
        color: #4A4A4A;
    }

    .signup-link a {
        color: #6CB4A4;
        text-decoration: none;
        font-weight: 500;
    }

    /* Illustration text */
    .illustration-text {
        font-family: 'Inter', sans-serif;
        font-size: 2.25rem;
        font-weight: 400;
        line-height: 1.4;
        margin-top: 2rem;
    }

    /* Hide navigation buttons */
    button[key="goto_signup"],
    button[key="goto_login"],
    button[key="goto_signup_from_login"],
    button[key="goto_login_from_signup"],
    button[key="goto_forgot_password"],
    button[key="goto_login_from_forgot"] {
        display: none !important;
    }

    /* Hide labels for inputs in auth forms */
    .stTextInput label {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Initialize auth_page in session state if not exists (login or signup or forgot_password)
    if "auth_page" not in st.session_state:
        st.session_state.auth_page = "login"

    # Show appropriate page based on auth_page state
    if st.session_state.auth_page == "login":
        show_login_form()
    elif st.session_state.auth_page == "signup":
        show_signup_form()
    elif st.session_state.auth_page == "forgot_password":
        show_forgot_password_form()


def show_login_form():
    """Afficher le formulaire de connexion."""

    # Add icons positioning CSS and JavaScript for password toggle
    st.markdown("""
    <style>
    /* Position icons before email input */
    div[data-testid="stForm"] div[data-testid="stVerticalBlock"] > div:nth-child(1) .stTextInput::before {
        content: '✉';
        position: absolute;
        left: 16px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.125rem;
        color: #9E9E9E;
        z-index: 10;
    }

    /* Position icons before password input */
    div[data-testid="stForm"] div[data-testid="stVerticalBlock"] > div:nth-child(2) .stTextInput::before {
        content: '🔒';
        position: absolute;
        left: 16px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.125rem;
        z-index: 10;
    }

    /* Show/Hide button for password */
    .password-toggle-btn {
        position: absolute;
        right: 16px;
        top: 50%;
        transform: translateY(-50%);
        color: #6CB4A4;
        font-size: 0.875rem;
        font-weight: 500;
        cursor: pointer;
        z-index: 10;
        background: none;
        border: none;
        padding: 0;
        font-family: 'Inter', sans-serif;
    }

    .password-toggle-btn:hover {
        color: #5A9E8E;
    }
    </style>

    <script>
    function togglePasswordVisibility() {
        // Find the password input
        const passwordInputs = document.querySelectorAll('input[type="password"], input[data-password-toggle]');

        passwordInputs.forEach(input => {
            if (input.type === 'password') {
                input.type = 'text';
                input.setAttribute('data-password-toggle', 'text');
                // Update button text
                const btn = input.parentElement.querySelector('.password-toggle-btn');
                if (btn) btn.textContent = 'Hide';
            } else {
                input.type = 'password';
                input.setAttribute('data-password-toggle', 'password');
                // Update button text
                const btn = input.parentElement.querySelector('.password-toggle-btn');
                if (btn) btn.textContent = 'Show';
            }
        });
    }

    // Add toggle button after page loads
    document.addEventListener('DOMContentLoaded', function() {
        setTimeout(function() {
            const passwordInputContainers = document.querySelectorAll('input[type="password"]');
            passwordInputContainers.forEach(container => {
                const parent = container.parentElement;
                if (parent && !parent.querySelector('.password-toggle-btn')) {
                    const btn = document.createElement('button');
                    btn.className = 'password-toggle-btn';
                    btn.textContent = 'Show';
                    btn.onclick = togglePasswordVisibility;
                    parent.style.position = 'relative';
                    parent.appendChild(btn);
                }
            });
        }, 100);
    });
    </script>
    """, unsafe_allow_html=True)

    # Create two-column layout
    left_col, right_col = st.columns([1, 1])

    with left_col:
        # Left column - Login form with proper container
        st.markdown('<div style="min-height: 100vh; background-color: #F5F5F5; display: flex; align-items: center; justify-content: center; padding: 2rem;">', unsafe_allow_html=True)
        st.markdown('<div style="background: white; border-radius: 24px; padding: 3rem 2.5rem; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); max-width: 440px; width: 100%;">', unsafe_allow_html=True)

        # Title
        st.markdown("""
        <h1 style='font-family: "Inter", sans-serif; font-size: 1.75rem; font-weight: 600;
                   color: #1A1A1A; margin-bottom: 2rem; line-height: 1.3;'>
            Welcome Back to<br/>SereneMind.
        </h1>
        """, unsafe_allow_html=True)

        with st.form("login_form", clear_on_submit=False):
            email = st.text_input(
                "Email",
                placeholder="Email Address",
                key="login_email",
                label_visibility="collapsed"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Password",
                key="login_password",
                label_visibility="collapsed"
            )

            submit = st.form_submit_button(
                "Sign In",
                use_container_width=True,
                type="primary"
            )

            if submit:
                if not email or not password:
                    st.error("Please fill in all fields")
                    return

                db = get_database()
                user = db.authenticate_user(email, password)

                if user:
                    st.session_state.user_id = user["id"]
                    st.session_state.user_email = user["email"]
                    st.session_state.user_display_name = user.get("display_name") or email.split("@")[0]
                    st.session_state.authenticated = True
                    init_session_timeout()
                    st.success(f"Welcome, {st.session_state.user_display_name}!")
                    st.rerun()
                else:
                    st.error("Incorrect email or password")

        # Forgot Password link with functional click handler
        col_forgot = st.columns([1])[0]
        with col_forgot:
            st.markdown("""
            <div style='text-align: center; margin-top: 1rem; margin-bottom: 1.5rem;'>
                <span id='forgot-password-link' style='color: #6CB4A4; font-size: 0.875rem; font-weight: 500; cursor: pointer;'>
                    Forgot Password?
                </span>
            </div>
            <script>
            document.getElementById('forgot-password-link').addEventListener('click', function() {
                const buttons = window.parent.document.querySelectorAll('button');
                buttons.forEach(btn => {
                    if (btn.innerText.includes('Go to forgot password')) {
                        btn.click();
                    }
                });
            });
            </script>
            """, unsafe_allow_html=True)

            # Hidden button for forgot password navigation
            if st.button("Go to forgot password", key="goto_forgot_password", type="secondary"):
                st.session_state.auth_page = "forgot_password"
                st.rerun()

        # Sign up link with functional click handler
        col_signup = st.columns([1])[0]
        with col_signup:
            st.markdown("""
            <div style='text-align: center; margin-bottom: 1.5rem; font-size: 0.9375rem; color: #4A4A4A;'>
                Don't have an account? <span id='signup-link-text' style='color: #6CB4A4; font-weight: 500; cursor: pointer;'>Sign Up</span>
            </div>
            <script>
            document.getElementById('signup-link-text').addEventListener('click', function() {
                // Find and click the hidden Streamlit button
                const buttons = window.parent.document.querySelectorAll('button');
                buttons.forEach(btn => {
                    if (btn.innerText.includes('Go to signup page')) {
                        btn.click();
                    }
                });
            });
            </script>
            """, unsafe_allow_html=True)

            # Hidden button that will be triggered by JavaScript
            if st.button("Go to signup page", key="goto_signup_from_login", type="secondary"):
                st.session_state.auth_page = "signup"
                st.rerun()

        # Social login buttons
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div style='padding: 0.75rem; border: 1px solid #E0E0E0; border-radius: 12px;
                        background: white; text-align: center; cursor: pointer;'>
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" style='vertical-align: middle;'>
                    <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                    <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                    <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
                    <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
                </svg>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div style='padding: 0.75rem; border: 1px solid #E0E0E0; border-radius: 12px;
                        background: white; text-align: center; cursor: pointer;'>
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" style='vertical-align: middle;'>
                    <path d="M17.05 20.28c-.98.95-2.05.88-3.08.4-1.09-.5-2.08-.48-3.24 0-1.44.62-2.2.44-3.06-.4C2.79 15.25 3.51 7.59 9.05 7.31c1.35.07 2.29.74 3.08.8 1.18-.24 2.31-.93 3.57-.84 1.51.12 2.65.72 3.4 1.8-3.12 1.87-2.38 5.98.48 7.13-.57 1.5-1.31 2.99-2.54 4.09l.01-.01zM12.03 7.25c-.15-2.23 1.66-4.07 3.74-4.25.29 2.58-2.34 4.5-3.74 4.25z" fill="#000000"/>
                </svg>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

    with right_col:
        # Right column - Illustration
        st.markdown("""
        <div style='min-height: 100vh; background: linear-gradient(135deg, #7B9FD3 0%, #9FC4E7 50%, #A8E6CF 100%);
                    display: flex; align-items: center; justify-content: center; padding: 4rem; text-align: center;'>
            <div>
                <div style='max-width: 400px; margin: 0 auto;'>
                    <svg width="300" height="300" viewBox="0 0 300 300" style='margin: 0 auto;'>
                        <circle cx="150" cy="120" r="80" fill="rgba(255, 255, 255, 0.2)"/>
                        <circle cx="150" cy="140" r="30" fill="rgba(255, 255, 255, 0.3)"/>
                        <ellipse cx="150" cy="180" rx="40" ry="50" fill="rgba(255, 255, 255, 0.3)"/>
                        <circle cx="80" cy="100" r="40" fill="rgba(167, 199, 231, 0.3)"/>
                        <circle cx="220" cy="150" r="50" fill="rgba(168, 230, 207, 0.3)"/>
                        <circle cx="100" cy="240" r="35" fill="rgba(167, 199, 231, 0.3)"/>
                    </svg>
                </div>
                <h2 style='font-family: "Inter", sans-serif; font-size: 2.25rem; font-weight: 400;
                           line-height: 1.4; margin-top: 2rem; color: white;'>
                    Your daily path to mental<br/>clarity and balance.
                </h2>
            </div>
        </div>
        """, unsafe_allow_html=True)


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
            st.info("🔄 Redirection vers la page de connexion...")

            # Redirect to login page after successful signup
            st.session_state.auth_page = "login"
            st.rerun()

        except ValueError as e:
            st.error(f"❌ Erreur: {e}")

    # Lien discret pour retourner à la connexion
    st.markdown("<div style='margin-top: 2rem; text-align: center;'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align: center;'>
        <span style='color: var(--gray-medium); font-family: "Inter", sans-serif; font-size: 0.875rem;'>
            Déjà un compte ?
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Lien texte simple
    col_left, col_center, col_right = st.columns([1, 1, 1])
    with col_center:
        if st.button(
            "Se connecter",
            key="goto_login",
            use_container_width=True,
            type="tertiary"
        ):
            st.session_state.auth_page = "login"
            st.rerun()


def show_forgot_password_form():
    """Afficher le formulaire de réinitialisation de mot de passe."""

    # Create two-column layout matching login page
    left_col, right_col = st.columns([1, 1])

    with left_col:
        # Left column - Forgot password form
        st.markdown('<div style="min-height: 100vh; background-color: #F5F5F5; display: flex; align-items: center; justify-content: center; padding: 2rem;">', unsafe_allow_html=True)
        st.markdown('<div style="background: white; border-radius: 24px; padding: 3rem 2.5rem; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); max-width: 440px; width: 100%;">', unsafe_allow_html=True)

        # Title
        st.markdown("""
        <h1 style='font-family: "Inter", sans-serif; font-size: 1.75rem; font-weight: 600;
                   color: #1A1A1A; margin-bottom: 1rem; line-height: 1.3;'>
            Reset Your Password
        </h1>
        <p style='font-family: "Inter", sans-serif; font-size: 0.9375rem; color: #6B6B6B;
                  margin-bottom: 2rem; line-height: 1.6;'>
            Enter your email address and we'll send you instructions to reset your password.
        </p>
        """, unsafe_allow_html=True)

        with st.form("forgot_password_form", clear_on_submit=False):
            # Email input
            email = st.text_input(
                "Email",
                placeholder="Email Address",
                key="forgot_password_email",
                label_visibility="collapsed"
            )

            submit = st.form_submit_button(
                "Send Reset Link",
                use_container_width=True,
                type="primary"
            )

            if submit:
                if not email:
                    st.error("Please enter your email address")
                    return

                # Check if user exists
                db = get_database()
                # For now, just show a success message
                # In production, you would send an actual email here
                st.success(f"If an account exists for {email}, you will receive password reset instructions shortly.")
                st.info("Note: Password reset functionality requires email configuration in production.")

        # Back to login link
        col_back = st.columns([1])[0]
        with col_back:
            st.markdown("""
            <div style='text-align: center; margin-top: 2rem;'>
                <span id='back-to-login-link' style='color: #6CB4A4; font-size: 0.875rem; font-weight: 500; cursor: pointer;'>
                    ← Back to Login
                </span>
            </div>
            <script>
            document.getElementById('back-to-login-link').addEventListener('click', function() {
                const buttons = window.parent.document.querySelectorAll('button');
                buttons.forEach(btn => {
                    if (btn.innerText.includes('Back to login page')) {
                        btn.click();
                    }
                });
            });
            </script>
            """, unsafe_allow_html=True)

            # Hidden button for navigation
            if st.button("Back to login page", key="goto_login_from_forgot", type="secondary"):
                st.session_state.auth_page = "login"
                st.rerun()

        st.markdown("</div></div>", unsafe_allow_html=True)

    with right_col:
        # Right column - Same illustration as login page
        st.markdown("""
        <div style='min-height: 100vh; background: linear-gradient(135deg, #7B9FD3 0%, #9FC4E7 50%, #A8E6CF 100%);
                    display: flex; align-items: center; justify-content: center; padding: 4rem; text-align: center;'>
            <div>
                <div style='max-width: 400px; margin: 0 auto;'>
                    <svg width="300" height="300" viewBox="0 0 300 300" style='margin: 0 auto;'>
                        <circle cx="150" cy="120" r="80" fill="rgba(255, 255, 255, 0.2)"/>
                        <circle cx="150" cy="140" r="30" fill="rgba(255, 255, 255, 0.3)"/>
                        <ellipse cx="150" cy="180" rx="40" ry="50" fill="rgba(255, 255, 255, 0.3)"/>
                        <circle cx="80" cy="100" r="40" fill="rgba(167, 199, 231, 0.3)"/>
                        <circle cx="220" cy="150" r="50" fill="rgba(168, 230, 207, 0.3)"/>
                        <circle cx="100" cy="240" r="35" fill="rgba(167, 199, 231, 0.3)"/>
                    </svg>
                </div>
                <h2 style='font-family: "Inter", sans-serif; font-size: 2.25rem; font-weight: 400;
                           line-height: 1.4; margin-top: 2rem; color: white;'>
                    Your daily path to mental<br/>clarity and balance.
                </h2>
            </div>
        </div>
        """, unsafe_allow_html=True)


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
        keys_to_clear = ["user_id", "user_email", "user_display_name", "authenticated", "current_page", "auth_page"]
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
        keys_to_clear = ["user_id", "user_email", "user_display_name", "authenticated", "current_page", "last_activity_time", "auth_page"]
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
        "last_activity_time",
        "auth_page"
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
