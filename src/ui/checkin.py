"""Composant UI pour le check-in quotidien."""

import streamlit as st
from datetime import datetime
from src.database.db_manager import DatabaseManager


@st.cache_resource
def get_database():
    """
    Singleton DatabaseManager pour toute l'application.

    Returns:
        Instance unique de DatabaseManager.
    """
    return DatabaseManager("serene.db")


def show_checkin():
    """Afficher la page de check-in avec formulaire et historique."""
    st.title("🌸 Quick Check-in")

    st.markdown(
        """
        <p style='font-size: 1.1rem; color: #4A5568; margin-bottom: 2rem;'>
        Prenez un moment pour enregistrer votre état émotionnel.
        Cela vous aidera à suivre votre bien-être au fil du temps.
        </p>
        """,
        unsafe_allow_html=True
    )

    # Formulaire de check-in dans une card élégante
    st.markdown("### 📝 Nouveau Check-in")

    with st.form("checkin_form", clear_on_submit=True):
        # Slider avec label élégant
        st.markdown("""
        <p style='font-weight: 500; color: #2D3748; margin-bottom: 0.5rem;'>
        Comment vous sentez-vous maintenant ?
        </p>
        """, unsafe_allow_html=True)

        mood_score = st.slider(
            "Mood Score",
            min_value=1,
            max_value=10,
            value=5,
            help="1 = Très mal | 5 = Neutre | 10 = Excellent",
            label_visibility="collapsed"
        )

        # Afficher un emoji selon le mood_score avec animation
        mood_emoji = _get_mood_emoji(mood_score)
        mood_label = _get_mood_label(mood_score)
        st.markdown(f"""
        <div style='text-align: center; margin: 1.5rem 0;'>
            <div style='font-size: 4rem; margin-bottom: 0.5rem;'>{mood_emoji}</div>
            <div style='font-size: 1.2rem; font-weight: 500; color: #6B46C1;'>{mood_label}</div>
        </div>
        """, unsafe_allow_html=True)

        # Text area avec style amélioré
        st.markdown("""
        <p style='font-weight: 500; color: #2D3748; margin-bottom: 0.5rem; margin-top: 1rem;'>
        Notes (optionnel)
        </p>
        """, unsafe_allow_html=True)

        notes = st.text_area(
            "Notes",
            placeholder="Décrivez ce qui influence votre humeur... (ex: 'Journée stressante au travail' ou 'Belle promenade ce matin')",
            max_chars=500,
            help="Partagez ce qui vous vient à l'esprit",
            label_visibility="collapsed"
        )

        submitted = st.form_submit_button("💾 Enregistrer Check-in", type="primary", use_container_width=True)

        if submitted:
            db = get_database()
            try:
                checkin_id = db.save_checkin(mood_score, notes)
                st.success(f"✅ Check-in enregistré avec succès!")
                # Plus de balloons (trop flashy pour sobriété luxueuse)
            except ValueError as e:
                st.error(f"❌ Erreur de validation: {e}")
            except Exception as e:
                st.error(f"❌ Erreur lors de l'enregistrement: {e}")

    # Historique avec design amélioré
    st.divider()
    st.markdown("### 📊 Historique")

    db = get_database()
    history = db.get_mood_history(days=30)

    if history:
        st.markdown(f"""
        <p style='color: #4A5568; margin-bottom: 1.5rem;'>
        <strong>{len(history)} check-in(s)</strong> enregistré(s) ce mois-ci
        </p>
        """, unsafe_allow_html=True)

        for i, checkin in enumerate(history):
            # Card pour chaque check-in
            mood_emoji = _get_mood_emoji(checkin["mood_score"])
            mood_label = _get_mood_label(checkin["mood_score"])

            # Formater le timestamp
            timestamp_str = checkin["timestamp"]
            try:
                dt = datetime.fromisoformat(timestamp_str)
                formatted_date = dt.strftime("%d/%m/%Y")
                formatted_time = dt.strftime("%H:%M")
            except (ValueError, TypeError):
                formatted_date = timestamp_str
                formatted_time = ""

            # Couleur de fond alternée pour distinction visuelle
            bg_color = "#F7FAFC" if i % 2 == 0 else "#FFFFFF"

            notes_html = f"<p style='color: #4A5568; margin-top: 0.5rem; line-height: 1.6;'>{checkin['notes']}</p>" if checkin["notes"] else ""

            st.markdown(f"""
            <div style='background-color: {bg_color}; padding: 1.25rem; border-radius: 12px; margin-bottom: 0.75rem; border-left: 4px solid #6B46C1;'>
                <div style='display: flex; align-items: center; margin-bottom: 0.5rem;'>
                    <div style='font-size: 2rem; margin-right: 1rem;'>{mood_emoji}</div>
                    <div style='flex: 1;'>
                        <div style='font-weight: 600; font-size: 1.1rem; color: #6B46C1;'>{mood_label}</div>
                        <div style='font-size: 0.9rem; color: #718096;'>
                            {formatted_date} à {formatted_time} · Score: {checkin["mood_score"]}/10
                        </div>
                    </div>
                </div>
                {notes_html}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info(
            "📭 Aucun check-in enregistré. "
            "Commencez par soumettre votre premier check-in ci-dessus!"
        )


def _get_mood_emoji(mood_score: int) -> str:
    """
    Retourner un emoji correspondant au mood_score.

    Args:
        mood_score: Score d'humeur (1-10).

    Returns:
        Emoji représentant l'humeur.
    """
    if mood_score <= 2:
        return "😢"
    elif mood_score <= 4:
        return "😔"
    elif mood_score <= 6:
        return "😐"
    elif mood_score <= 8:
        return "🙂"
    else:
        return "😊"


def _get_mood_label(mood_score: int) -> str:
    """
    Retourner un label textuel correspondant au mood_score.

    Args:
        mood_score: Score d'humeur (1-10).

    Returns:
        Label textuel représentant l'humeur.
    """
    if mood_score <= 2:
        return "Très difficile"
    elif mood_score <= 4:
        return "Difficile"
    elif mood_score <= 6:
        return "Neutre"
    elif mood_score <= 8:
        return "Bien"
    else:
        return "Excellent"
