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
    st.markdown("""
    <div style='animation: fadeInDown 0.5s ease-out;'>
        <h1 style='font-size: 2.5rem; color: #1A202C; font-weight: 600; margin-bottom: 0.5rem;'>
            Quick Check-in
        </h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        <p style='font-size: 1.1rem; color: #4A5568; margin-bottom: 2rem; animation: fadeIn 0.7s ease-out;'>
        Prenez un moment pour enregistrer votre état émotionnel.
        Cela vous aidera à suivre votre bien-être au fil du temps.
        </p>
        """,
        unsafe_allow_html=True
    )

    # Formulaire de check-in dans une card élégante
    st.markdown("### Nouveau Check-in")

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

        # Afficher le mood avec animation
        mood_label = _get_mood_label(mood_score)
        mood_color = _get_mood_color(mood_score)

        st.markdown(f"""
        <div style='text-align: center; margin: 1.5rem 0; padding: 2rem;
                    background: linear-gradient(135deg, #F7FAFC 0%, {mood_color}15 100%);
                    border-radius: 16px; animation: scaleIn 0.3s ease-out;'>
            <div style='font-size: 1.4rem; font-weight: 600; color: {mood_color};'>{mood_label}</div>
            <div style='font-size: 0.9rem; color: #718096; margin-top: 0.5rem;'>Score: {mood_score}/10</div>
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

        submitted = st.form_submit_button("Enregistrer Check-in", type="primary", use_container_width=True)

        if submitted:
            db = get_database()
            try:
                checkin_id = db.save_checkin(mood_score, notes)
                st.success("Check-in enregistré avec succès!")
                # Plus de balloons (trop flashy pour sobriété luxueuse)
            except ValueError as e:
                st.error(f"Erreur de validation: {e}")
            except Exception as e:
                st.error(f"Erreur lors de l'enregistrement: {e}")

    # Historique avec design amélioré
    st.divider()
    st.markdown("### Historique")

    db = get_database()
    history = db.get_mood_history(days=30)

    if history:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #6B46C1 0%, #805AD5 100%);
                    padding: 1rem 1.5rem; border-radius: 12px; margin-bottom: 1.5rem;
                    animation: fadeInUp 0.5s ease-out;'>
            <p style='color: white; margin: 0; font-size: 1.05rem; font-weight: 500;'>
                <strong>{len(history)} check-in(s)</strong> enregistré(s) ce mois-ci
            </p>
        </div>
        """, unsafe_allow_html=True)

        for i, checkin in enumerate(history):
            # Card pour chaque check-in
            mood_label = _get_mood_label(checkin["mood_score"])
            mood_color = _get_mood_color(checkin["mood_score"])

            # Formater le timestamp
            timestamp_str = checkin["timestamp"]
            try:
                dt = datetime.fromisoformat(timestamp_str)
                formatted_date = dt.strftime("%d/%m/%Y")
                formatted_time = dt.strftime("%H:%M")
            except (ValueError, TypeError):
                formatted_date = timestamp_str
                formatted_time = ""

            # Animation delay basée sur l'index
            animation_delay = i * 0.05

            notes_html = f"<p style='color: #4A5568; margin-top: 0.5rem; line-height: 1.6; font-size: 0.95rem;'>{checkin['notes']}</p>" if checkin["notes"] else ""

            st.markdown(f"""
            <div style='background-color: #F7FAFC; padding: 1.25rem; border-radius: 12px; margin-bottom: 0.75rem;
                        border-left: 4px solid {mood_color}; box-shadow: 0 2px 8px rgba(107, 70, 193, 0.08);
                        animation: fadeInUp {0.5 + animation_delay}s ease-out;
                        transition: all 0.3s ease-out;'
                 onmouseover='this.style.transform="translateX(4px)"; this.style.boxShadow="0 4px 12px rgba(107, 70, 193, 0.12)";'
                 onmouseout='this.style.transform="translateX(0)"; this.style.boxShadow="0 2px 8px rgba(107, 70, 193, 0.08)";'>
                <div style='margin-bottom: 0.5rem;'>
                    <div style='font-weight: 600; font-size: 1.1rem; color: {mood_color};'>{mood_label}</div>
                    <div style='font-size: 0.85rem; color: #718096;'>
                        {formatted_date} à {formatted_time} · <span style='color: {mood_color}; font-weight: 500;'>Score: {checkin["mood_score"]}/10</span>
                    </div>
                </div>
                {notes_html}
            </div>
            """, unsafe_allow_html=True)
    else:
        # État vide engageant avec animation
        st.markdown("""
        <div style='background: linear-gradient(135deg, #F7FAFC 0%, #EBF4FF 100%);
                    padding: 3rem 2rem; border-radius: 16px;
                    text-align: center; border: 2px dashed #CBD5E0;
                    animation: fadeInUp 0.5s ease-out;'>
            <div style='font-size: 1.2rem; font-weight: 600; color: #6B46C1; margin-bottom: 0.75rem;'>
                Votre journal de bien-être vous attend
            </div>
            <div style='font-size: 1rem; color: #4A5568; margin-bottom: 1rem; line-height: 1.6;'>
                Créez votre premier check-in ci-dessus pour commencer à suivre votre humeur.<br/>
                Chaque check-in est une étape vers une meilleure connaissance de soi.
            </div>
            <div style='background-color: white; padding: 1.5rem; border-radius: 12px;
                        box-shadow: 0 2px 8px rgba(107, 70, 193, 0.1); margin-top: 1.5rem;
                        display: inline-block;'>
                <div style='color: #6B46C1; font-weight: 500; font-size: 0.9rem; margin-bottom: 0.5rem;'>Le saviez-vous ?</div>
                <div style='color: #4A5568; font-size: 0.85rem;'>
                    Suivre son humeur quotidiennement aide à identifier<br/>
                    les patterns et améliorer son bien-être mental
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


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


def _get_mood_color(mood_score: int) -> str:
    """
    Retourner une couleur correspondant au mood_score.

    Args:
        mood_score: Score d'humeur (1-10).

    Returns:
        Code couleur hexadécimal.
    """
    if mood_score <= 2:
        return "#F56565"  # Rouge (très mal)
    elif mood_score <= 4:
        return "#ED8936"  # Orange (difficile)
    elif mood_score <= 6:
        return "#718096"  # Gris (neutre)
    elif mood_score <= 8:
        return "#6B46C1"  # Violet (bien)
    else:
        return "#48BB78"  # Vert (excellent)
