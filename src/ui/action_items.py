"""
Composant UI pour la gestion des objectifs et actions
Phase 2.1 : Suivi Contextuel & Mémoire de l'IA
"""

import streamlit as st
from datetime import datetime, timedelta
from src.database.db_manager import DatabaseManager
from src.ui.auth import get_current_user_id
from src.ui.styles.serene_styles import COLORS


@st.cache_resource
def get_database():
    """
    Singleton DatabaseManager pour toute l'application.

    Returns:
        Instance unique de DatabaseManager.
    """
    return DatabaseManager("serene.db")


def format_datetime(timestamp_str: str) -> str:
    """
    Formate un timestamp ISO en date lisible.

    Args:
        timestamp_str: Timestamp au format ISO

    Returns:
        Date formatée (ex: "24 nov. 2025")
    """
    if not timestamp_str:
        return ""
    try:
        dt = datetime.fromisoformat(timestamp_str)
        return dt.strftime("%d %b. %Y")
    except (ValueError, TypeError):
        return timestamp_str


def get_status_badge(status: str) -> str:
    """
    Retourne le badge HTML pour un statut.

    Args:
        status: Statut de l'action

    Returns:
        HTML du badge
    """
    status_config = {
        "pending": {"label": "À faire", "color": COLORS["sage"]},
        "in_progress": {"label": "En cours", "color": COLORS["terracotta"]},
        "completed": {"label": "Terminé", "color": COLORS["moss"]},
        "abandoned": {"label": "Abandonné", "color": COLORS["stone"]},
    }

    config = status_config.get(status, {"label": status, "color": COLORS["charcoal"]})

    return f"""
    <span style="
        background: {config['color']}20;
        color: {config['color']};
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 500;
        letter-spacing: 0.02em;
    ">{config['label']}</span>
    """


def get_source_badge(source: str) -> str:
    """
    Retourne le badge HTML pour la source.

    Args:
        source: Source de l'action ('manual' ou 'ai_extracted')

    Returns:
        HTML du badge
    """
    if source == "ai_extracted":
        return f"""
        <span style="
            background: {COLORS['gold']}20;
            color: {COLORS['gold']};
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 500;
            letter-spacing: 0.02em;
        ">✨ Détecté par l'IA</span>
        """
    return ""


def action_card(action: dict, index: int) -> str:
    """
    Génère une carte HTML pour une action.

    Args:
        action: Dict contenant les données de l'action
        index: Index de l'action (pour la clé unique)

    Returns:
        HTML de la carte
    """
    created_date = format_datetime(action.get("created_at", ""))
    deadline = format_datetime(action.get("deadline", ""))
    completed_date = format_datetime(action.get("completed_at", ""))

    status_badge = get_status_badge(action["status"])
    source_badge = get_source_badge(action.get("source", "manual"))

    description_html = ""
    if action.get("description"):
        description_html = f"""
        <p style="
            color: {COLORS['charcoal']};
            margin: 0.75rem 0 0 0;
            font-size: 0.9rem;
            line-height: 1.5;
        ">{action['description']}</p>
        """

    deadline_html = ""
    if deadline:
        deadline_html = f"""
        <div style="margin-top: 0.75rem;">
            <span style="color: {COLORS['stone']}; font-size: 0.85rem;">
                📅 Échéance: {deadline}
            </span>
        </div>
        """

    completed_html = ""
    if completed_date:
        completed_html = f"""
        <div style="margin-top: 0.75rem;">
            <span style="color: {COLORS['moss']}; font-size: 0.85rem;">
                ✓ Complété le {completed_date}
            </span>
        </div>
        """

    return f"""
    <div style="
        background: white;
        border: 1px solid {COLORS['stone']}40;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.2s ease;
    ">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
            <h3 style="
                font-family: 'Cormorant Garamond', serif;
                font-size: 1.25rem;
                font-weight: 500;
                color: {COLORS['black']};
                margin: 0;
                flex: 1;
            ">{action['title']}</h3>
            <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; justify-content: flex-end;">
                {status_badge}
                {source_badge}
            </div>
        </div>

        <div style="color: {COLORS['stone']}; font-size: 0.85rem; margin-bottom: 0.5rem;">
            Créé le {created_date}
        </div>

        {description_html}
        {deadline_html}
        {completed_html}
    </div>
    """


def stats_card(stats: dict) -> str:
    """
    Génère une carte de statistiques.

    Args:
        stats: Dict contenant les statistiques

    Returns:
        HTML de la carte
    """
    return f"""
    <div style="
        background: linear-gradient(135deg, {COLORS['sage']}15 0%, {COLORS['moss']}15 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        border: 1px solid {COLORS['sage']}30;
    ">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 1.5rem;">
            <div style="text-align: center;">
                <div style="font-size: 2rem; font-weight: 600; color: {COLORS['black']};">
                    {stats['total']}
                </div>
                <div style="color: {COLORS['charcoal']}; font-size: 0.85rem; margin-top: 0.25rem;">
                    Total
                </div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; font-weight: 600; color: {COLORS['sage']};">
                    {stats['pending']}
                </div>
                <div style="color: {COLORS['charcoal']}; font-size: 0.85rem; margin-top: 0.25rem;">
                    À faire
                </div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; font-weight: 600; color: {COLORS['terracotta']};">
                    {stats['in_progress']}
                </div>
                <div style="color: {COLORS['charcoal']}; font-size: 0.85rem; margin-top: 0.25rem;">
                    En cours
                </div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; font-weight: 600; color: {COLORS['moss']};">
                    {stats['completed']}
                </div>
                <div style="color: {COLORS['charcoal']}; font-size: 0.85rem; margin-top: 0.25rem;">
                    Complétés
                </div>
            </div>
        </div>
    </div>
    """


def show_action_items():
    """Afficher la page de gestion des objectifs et actions."""

    # Header de la page
    st.markdown(f"""
    <div style="margin-bottom: 2rem;">
        <h1 style="
            font-family: 'Cormorant Garamond', serif;
            font-size: 3rem;
            font-weight: 300;
            color: {COLORS['black']};
            margin-bottom: 0.5rem;
            letter-spacing: 0.02em;
        ">Mes Objectifs & Actions</h1>
        <p style="
            color: {COLORS['charcoal']};
            font-size: 1.1rem;
            line-height: 1.6;
            max-width: 800px;
        ">
            Suivez vos objectifs de bien-être et les actions identifiées pendant vos conversations.
            L'IA détecte automatiquement vos intentions et les transforme en actions concrètes.
        </p>
    </div>
    """, unsafe_allow_html=True)

    db = get_database()
    user_id = get_current_user_id()

    # Afficher les statistiques
    stats = db.get_action_items_stats(user_id)
    st.markdown(stats_card(stats), unsafe_allow_html=True)

    # ==================== FORMULAIRE D'AJOUT D'ACTION ====================

    st.markdown(f"""
    <h2 style="
        font-family: 'Cormorant Garamond', serif;
        font-size: 2rem;
        font-weight: 300;
        color: {COLORS['black']};
        margin-bottom: 1.5rem;
        letter-spacing: 0.02em;
    ">Nouvelle Action</h2>
    """, unsafe_allow_html=True)

    with st.form("new_action_form", clear_on_submit=True):
        title = st.text_input(
            "Titre de l'action*",
            placeholder="Ex: Méditer 10 minutes chaque matin",
            max_chars=200,
        )

        description = st.text_area(
            "Description (optionnel)",
            placeholder="Ajoutez des détails sur cette action...",
            max_chars=500,
            height=100,
        )

        col1, col2 = st.columns(2)

        with col1:
            deadline = st.date_input(
                "Échéance (optionnel)",
                value=None,
                min_value=datetime.now().date(),
            )

        submitted = st.form_submit_button(
            "Ajouter l'action",
            type="primary",
            use_container_width=True
        )

        if submitted:
            if not title:
                st.error("❌ Le titre est requis")
            else:
                try:
                    deadline_str = deadline.isoformat() if deadline else None
                    action_id = db.save_action_item(
                        user_id=user_id,
                        title=title,
                        description=description,
                        source="manual",
                        deadline=deadline_str,
                    )
                    st.success(f"✅ Action ajoutée avec succès !")
                    st.rerun()
                except ValueError as e:
                    st.error(f"❌ Erreur de validation: {e}")
                except Exception as e:
                    st.error(f"❌ Erreur lors de l'ajout: {e}")

    # ==================== FILTRES ET LISTE DES ACTIONS ====================

    st.divider()
    st.markdown(f"""
    <h2 style="
        font-family: 'Cormorant Garamond', serif;
        font-size: 2rem;
        font-weight: 300;
        color: {COLORS['black']};
        margin-bottom: 1.5rem;
        letter-spacing: 0.02em;
    ">Mes Actions</h2>
    """, unsafe_allow_html=True)

    # Filtres
    filter_options = {
        "Toutes": None,
        "À faire": "pending",
        "En cours": "in_progress",
        "Complétées": "completed",
        "Abandonnées": "abandoned",
    }

    selected_filter = st.selectbox(
        "Filtrer par statut",
        options=list(filter_options.keys()),
        index=0,
    )

    status_filter = filter_options[selected_filter]

    # Récupérer les actions
    actions = db.get_action_items(user_id, status=status_filter)

    if actions:
        st.markdown(f"""
        <p style="color: {COLORS['stone']}; font-size: 0.9rem; margin-bottom: 1rem;">
            {len(actions)} action(s) affichée(s)
        </p>
        """, unsafe_allow_html=True)

        # Afficher les actions
        for i, action in enumerate(actions):
            st.markdown(action_card(action, i), unsafe_allow_html=True)

            # Boutons d'action
            col1, col2, col3, col4 = st.columns([2, 2, 2, 1])

            with col1:
                if action["status"] != "completed":
                    if st.button("✓ Marquer comme complété", key=f"complete_{action['id']}"):
                        db.update_action_item(action["id"], status="completed")
                        st.rerun()

            with col2:
                if action["status"] == "pending":
                    if st.button("▶ Commencer", key=f"start_{action['id']}"):
                        db.update_action_item(action["id"], status="in_progress")
                        st.rerun()

            with col3:
                if action["status"] not in ["completed", "abandoned"]:
                    if st.button("✕ Abandonner", key=f"abandon_{action['id']}"):
                        db.update_action_item(action["id"], status="abandoned")
                        st.rerun()

            with col4:
                if st.button("🗑", key=f"delete_{action['id']}", help="Supprimer"):
                    db.delete_action_item(action["id"])
                    st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)

    else:
        # État vide
        st.markdown(f"""
        <div style="
            text-align: center;
            padding: 3rem 2rem;
            background: {COLORS['sand']}40;
            border-radius: 12px;
            margin: 2rem 0;
        ">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🎯</div>
            <h3 style="
                font-family: 'Cormorant Garamond', serif;
                font-size: 1.5rem;
                font-weight: 400;
                color: {COLORS['black']};
                margin-bottom: 0.75rem;
            ">Aucune action pour le moment</h3>
            <p style="color: {COLORS['charcoal']}; max-width: 600px; margin: 0 auto;">
                Ajoutez votre première action manuellement ci-dessus, ou laissez l'IA
                détecter automatiquement vos objectifs lors de vos conversations.
            </p>
            <div style="
                margin-top: 1.5rem;
                padding: 1rem;
                background: white;
                border-radius: 8px;
                max-width: 500px;
                margin-left: auto;
                margin-right: auto;
            ">
                <p style="
                    color: {COLORS['gold']};
                    font-weight: 500;
                    margin-bottom: 0.5rem;
                ">💡 Astuce</p>
                <p style="color: {COLORS['charcoal']}; font-size: 0.9rem; margin: 0;">
                    Lors de vos conversations, mentionnez vos intentions avec des phrases comme
                    "Je vais..." ou "J'ai décidé de..." et l'IA les détectera automatiquement.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
