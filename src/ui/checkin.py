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
        Prenez un moment pour enregistrer votre état émotionnel.
        Cela vous aidera à suivre votre bien-être au fil du temps.
        """
    )

    # Formulaire de check-in
    st.subheader("📝 Nouveau Check-in")

    with st.form("checkin_form", clear_on_submit=True):
        mood_score = st.slider(
            "Comment vous sentez-vous maintenant?",
            min_value=1,
            max_value=10,
            value=5,
            help="1 = Très mal | 5 = Neutre | 10 = Excellent",
        )

        # Afficher un emoji selon le mood_score
        mood_emoji = _get_mood_emoji(mood_score)
        st.markdown(f"### {mood_emoji}")

        notes = st.text_area(
            "Notes (optionnel)",
            placeholder="Décrivez ce qui influence votre humeur...",
            max_chars=500,
            help="Partagez ce qui vous vient à l'esprit",
        )

        submitted = st.form_submit_button("💾 Enregistrer Check-in", type="primary")

        if submitted:
            db = get_database()
            try:
                checkin_id = db.save_checkin(mood_score, notes)
                st.success(f"✅ Check-in #{checkin_id} enregistré avec succès!")
                st.balloons()
            except ValueError as e:
                st.error(f"❌ Erreur de validation: {e}")
            except Exception as e:
                st.error(f"❌ Erreur lors de l'enregistrement: {e}")

    # Historique
    st.divider()
    st.subheader("📊 Historique (30 derniers jours)")

    db = get_database()
    history = db.get_mood_history(days=30)

    if history:
        st.info(f"**{len(history)} check-in(s)** enregistré(s) ce mois-ci")

        for checkin in history:
            col1, col2, col3 = st.columns([1, 2, 5])

            with col1:
                mood_emoji = _get_mood_emoji(checkin["mood_score"])
                st.markdown(f"### {mood_emoji}")

            with col2:
                st.metric("Mood", checkin["mood_score"])

            with col3:
                # Formater le timestamp
                timestamp_str = checkin["timestamp"]
                try:
                    dt = datetime.fromisoformat(timestamp_str)
                    formatted_date = dt.strftime("%d/%m/%Y %H:%M")
                except (ValueError, TypeError):
                    formatted_date = timestamp_str

                st.caption(f"🕐 {formatted_date}")

                if checkin["notes"]:
                    st.write(checkin["notes"])

            st.divider()
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
