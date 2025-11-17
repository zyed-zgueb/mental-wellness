"""
Theme toggle component for dark/light mode switching
Beautiful modern design inspired by premium web applications
"""

import streamlit as st


def render_theme_toggle():
    """Render a beautiful theme toggle switch in the sidebar."""

    # Initialize theme in session state if not exists
    if 'theme' not in st.session_state:
        st.session_state.theme = 'dark'  # Default to dark theme as requested

    current_theme = st.session_state.theme

    # Modern theme toggle with CSS
    st.markdown("""
    <style>
    .theme-toggle-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
        padding: 1rem;
        margin: 1.5rem 0;
        background: var(--bg-tertiary);
        border-radius: var(--radius-lg);
        border: 1px solid var(--border-primary);
    }

    .theme-icon {
        font-size: 1.25rem;
        opacity: 0.5;
        transition: opacity 0.3s ease;
    }

    .theme-icon.active {
        opacity: 1;
    }

    /* Hide default streamlit toggle */
    .theme-toggle-container .stCheckbox {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

    # Theme toggle UI
    st.markdown(f"""
    <div class='theme-toggle-container'>
        <span class='theme-icon {"active" if current_theme == "light" else ""}'>☀️</span>
        <span style='color: var(--text-tertiary); font-size: 0.85rem; font-weight: 500;'>
            {current_theme.upper()}
        </span>
        <span class='theme-icon {"active" if current_theme == "dark" else ""}'>🌙</span>
    </div>
    """, unsafe_allow_html=True)

    # Toggle button
    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("☀️ Light", key="light_btn", use_container_width=True, type="secondary" if current_theme == "dark" else "primary"):
            st.session_state.theme = 'light'
            st.rerun()

    with col2:
        if st.button("🌙 Dark", key="dark_btn", use_container_width=True, type="secondary" if current_theme == "light" else "primary"):
            st.session_state.theme = 'dark'
            st.rerun()


def get_current_theme():
    """Get the current theme from session state."""
    return st.session_state.get('theme', 'dark')
