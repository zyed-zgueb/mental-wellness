"""
Composant UI pour le check-in quotidien - Version refactorisée
Design cohérent, maintenable et optimisé pour la santé mentale
"""

import streamlit as st
from datetime import datetime
from src.database.db_manager import DatabaseManager
from src.ui.auth import get_current_user_id
from src.ui.styles.serene_styles import COLORS
from src.ui.ui_components.mood_components import (
    mood_display_card,
    stats_banner,
    history_card,
    empty_state,
    page_header
)


@st.cache_resource
def get_database():
    """
    Singleton DatabaseManager pour toute l'application.
    
    Returns:
        Instance unique de DatabaseManager.
    """
    return DatabaseManager("serene.db")


def get_mood_data(mood_score: int) -> tuple[str, str, str]:
    """
    Retourne les données de mood (emoji, label, couleur) pour un score donné.
    Note: Dans le design minimaliste, emojis et couleurs ne sont plus utilisés visuellement.

    Args:
        mood_score: Score d'humeur (0-10)

    Returns:
        Tuple (emoji, label, couleur) - emoji et couleur gardés pour compatibilité
    """
    if mood_score <= 2:
        return "", "Très difficile", COLORS['mood_tres_difficile']
    elif mood_score <= 4:
        return "", "Difficile", COLORS['mood_difficile']
    elif mood_score <= 6:
        return "", "Neutre", COLORS['mood_neutre']
    elif mood_score <= 8:
        return "", "Bien", COLORS['mood_bien']
    else:
        return "", "Excellent", COLORS['mood_excellent']


def format_datetime(timestamp_str: str) -> tuple[str, str]:
    """
    Formate un timestamp ISO en date et heure séparées.
    
    Args:
        timestamp_str: Timestamp au format ISO
        
    Returns:
        Tuple (date_formatée, heure_formatée)
    """
    try:
        dt = datetime.fromisoformat(timestamp_str)
        return dt.strftime("%d/%m/%Y"), dt.strftime("%H:%M")
    except (ValueError, TypeError):
        return timestamp_str, ""


def show_checkin():
    """Afficher la page de check-in avec formulaire et historique."""

    # Header de la page
    st.markdown(
        page_header(
            title="Quick Check-in",
            emoji="",
            description="Prenez un moment pour enregistrer votre état émotionnel. "
                       "Cela vous aidera à suivre votre bien-être au fil du temps."
        ),
        unsafe_allow_html=True
    )
    
    # ==================== FORMULAIRE DE CHECK-IN ====================
    
    st.markdown("""<h2 style='font-family: "Cormorant Garamond", serif; font-size: 2rem; font-weight: 300;
                color: var(--black); margin-bottom: 2rem; letter-spacing: 0.02em;'>
    Nouveau Check-in</h2>
                """, unsafe_allow_html=True)
    
    with st.form("checkin_form", clear_on_submit=True):
        # Slider avec label
        st.markdown(
            f"<p style='font-weight: 500; color: {COLORS['charcoal']}; "
            f"margin-bottom: 0.5rem;'>Comment vous sentez-vous maintenant ?</p>",
            unsafe_allow_html=True
        )
        
        mood_score = st.slider(
            "Score d'humeur",
            min_value=0,
            max_value=10,
            value=5,
            help="0 = Très mal | 5 = Neutre | 10 = Excellent",
            label_visibility="hidden"
        )
        
        # Affichage du mood actuel
        mood_emoji, mood_label, mood_color = get_mood_data(mood_score)
        st.markdown(
            mood_display_card(mood_score, mood_emoji, mood_label, mood_color),
            unsafe_allow_html=True
        )
        
        # Zone de notes
        st.markdown(
            f"<p style='font-weight: 500; color: {COLORS['charcoal']}; "
            f"margin-bottom: 0.5rem; margin-top: 1rem;'>Notes (optionnel)</p>",
            unsafe_allow_html=True
        )
        
        notes = st.text_area(
            "Notes additionnelles",
            placeholder="Décrivez ce qui influence votre humeur... "
                       "(ex: 'Journée stressante au travail' ou 'Belle promenade ce matin')",
            max_chars=500,
            help="Partagez ce qui vous vient à l'esprit",
            height=100,
            label_visibility="hidden"
        )
        
        # Bouton de soumission
        submitted = st.form_submit_button(
            "Enregistrer Check-in",
            type="primary",
            use_container_width=True
        )
        
        if submitted:
            db = get_database()
            user_id = get_current_user_id()
            try:
                checkin_id = db.save_checkin(user_id, mood_score, notes)
                st.success(
                    f"✅ Check-in enregistré avec succès ! "
                    f"Mood: {mood_label} ({mood_score}/10)"
                )
                # Pas de balloons pour rester sobre
            except ValueError as e:
                st.error(f"❌ Erreur de validation: {e}")
            except Exception as e:
                st.error(f"❌ Erreur lors de l'enregistrement: {e}")
    
    # ==================== HISTORIQUE ====================
    
    st.divider()
    st.markdown("""<h2 style='font-family: "Cormorant Garamond", serif; font-size: 2rem; font-weight: 300;
                color: var(--black); margin-bottom: 2rem; letter-spacing: 0.02em;'>
    Historique</h2>
                """, unsafe_allow_html=True)

    db = get_database()
    user_id = get_current_user_id()
    history = db.get_mood_history(user_id, days=30)
    
    if history:
        # Bannière de statistiques
        st.markdown(
            stats_banner(len(history)),
            unsafe_allow_html=True
        )
        
        # Affichage des check-ins
        for i, checkin in enumerate(history):
            mood_emoji, mood_label, mood_color = get_mood_data(checkin["mood_score"])
            formatted_date, formatted_time = format_datetime(checkin["timestamp"])
            
            st.html(
                history_card(
                    checkin=checkin,
                    mood_emoji=mood_emoji,
                    mood_label=mood_label,
                    mood_color=mood_color,
                    formatted_date=formatted_date,
                    formatted_time=formatted_time,
                    index=i
                )
            )
    else:
        # État vide
        st.markdown(
            empty_state(
                icon="📝",
                title="Votre journal de bien-être vous attend",
                description="Créez votre premier check-in ci-dessus pour commencer à suivre votre humeur.<br/>"
                           "Chaque check-in est une étape vers une meilleure connaissance de soi.",
                tip_title="💡 Le saviez-vous ?",
                tip_content="Suivre son humeur quotidiennement aide à identifier "
                           "les patterns et améliorer son bien-être mental."
            ),
            unsafe_allow_html=True
        )


# ==================== FONCTIONS LEGACY (pour compatibilité) ====================
# À supprimer une fois la migration terminée

def _get_mood_emoji(mood_score: int) -> str:
    """Wrapper legacy - utilise get_mood_data()."""
    return get_mood_data(mood_score)[0]


def _get_mood_label(mood_score: int) -> str:
    """Wrapper legacy - utilise get_mood_data()."""
    return get_mood_data(mood_score)[1]


def _get_mood_color(mood_score: int) -> str:
    """Wrapper legacy - utilise get_mood_data()."""
    return get_mood_data(mood_score)[2]