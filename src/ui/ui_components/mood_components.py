"""
Composants UI réutilisables pour l'application Serene
Facilite la maintenance et garantit la cohérence visuelle
Theme-aware avec CSS variables
"""


def mood_display_card(mood_score: int, mood_emoji: str, mood_label: str, mood_color: str) -> str:
    """
    Génère le HTML pour l'affichage du mood actuel.

    Args:
        mood_score: Score de l'humeur (1-10)
        mood_emoji: Emoji représentant l'humeur
        mood_label: Label textuel de l'humeur
        mood_color: Couleur associée à l'humeur

    Returns:
        HTML string du composant
    """
    return f"""
    <div class="mood-display" style="
        text-align: center;
        margin: 2rem 0;
        padding: 2.5rem;
        background: linear-gradient(135deg, var(--bg-tertiary) 0%, {mood_color}15 100%);
        border-radius: var(--radius-lg);
        border: 2px solid {mood_color}30;
        box-shadow: var(--shadow-md);
        animation: scaleIn 0.3s ease-out;
    ">
        <div style="font-size: 4.5rem; margin-bottom: 1rem; filter: drop-shadow(0 2px 8px {mood_color}40);">
            {mood_emoji}
        </div>
        <div style="font-size: 1.75rem; font-weight: 700; color: {mood_color}; margin-bottom: 0.5rem;">
            {mood_label}
        </div>
        <div style="font-size: 1.1rem; color: var(--text-tertiary); font-weight: 500;">
            Score: {mood_score}/10
        </div>
    </div>
    """


def stats_banner(total_checkins: int) -> str:
    """
    Génère le HTML pour la bannière de statistiques.

    Args:
        total_checkins: Nombre total de check-ins

    Returns:
        HTML string du composant
    """
    return f"""
    <div style="
        background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
        padding: 1.5rem 2rem;
        border-radius: var(--radius-md);
        margin-bottom: 2rem;
        box-shadow: var(--shadow-lg), 0 0 30px var(--color-primary-glow);
        animation: fadeInUp 0.4s ease-out;
        border: 1px solid var(--border-accent);
    ">
        <p style="color: var(--text-inverse); margin: 0; font-size: 1.1rem; font-weight: 600;">
            📊 <strong>{total_checkins} check-in(s)</strong> enregistré(s) ce mois-ci
        </p>
    </div>
    """


def history_card(
    checkin: dict,
    mood_emoji: str,
    mood_label: str,
    mood_color: str,
    formatted_date: str,
    formatted_time: str,
    index: int = 0
) -> str:
    """
    Génère le HTML pour une carte d'historique.
    
    Args:
        checkin: Dictionnaire contenant les données du check-in
        mood_emoji: Emoji de l'humeur
        mood_label: Label de l'humeur
        mood_color: Couleur de l'humeur
        formatted_date: Date formatée
        formatted_time: Heure formatée
        index: Index pour l'animation (optionnel)
        
    Returns:
        HTML string du composant
    """
    notes_html = ""
    if checkin.get("notes"):
        # Échapper les caractères HTML pour éviter les problèmes
        safe_notes = (str(checkin['notes'])
                     .replace('&', '&amp;')
                     .replace('<', '&lt;')
                     .replace('>', '&gt;')
                     .replace('"', '&quot;')
                     .replace("'", '&#39;'))

        notes_html = f"""
        <div style="
            color: var(--text-secondary);
            margin-top: 1rem;
            line-height: 1.7;
            font-size: 1rem;
            padding: 1rem;
            background-color: var(--bg-tertiary);
            border-radius: var(--radius-sm);
            border-left: 3px solid {mood_color};
            font-style: italic;
        ">
            {safe_notes}
        </div>
        """
    
    # Animation delay basée sur l'index
    animation_delay = index * 0.05

    return f"""
    <div class="history-card" style="
        background-color: var(--bg-elevated);
        padding: 2rem;
        border-radius: var(--radius-lg);
        margin-bottom: 1.5rem;
        border-left: 4px solid {mood_color};
        box-shadow: var(--shadow-md);
        animation: fadeInUp {0.4 + animation_delay}s ease-out;
        border: 1px solid var(--border-primary);
        border-left: 4px solid {mood_color};
    ">
        <div style="display: flex; align-items: center; margin-bottom: 0.75rem;">
            <div style="font-size: 3rem; margin-right: 1.25rem; filter: drop-shadow(0 2px 4px {mood_color}40);">
                {mood_emoji}
            </div>
            <div style="flex: 1;">
                <div style="font-weight: 700; font-size: 1.25rem; color: {mood_color};">
                    {mood_label}
                </div>
                <div style="font-size: 0.95rem; color: var(--text-tertiary); margin-top: 0.5rem;">
                    📅 {formatted_date} à {formatted_time} ·
                    <span style="color: {mood_color}; font-weight: 600;">
                        Score: {checkin["mood_score"]}/10
                    </span>
                </div>
            </div>
        </div>
        {notes_html}
    </div>
    """


def empty_state(
    icon: str = "📝",
    title: str = "Votre journal de bien-être vous attend",
    description: str = "Créez votre premier check-in pour commencer à suivre votre humeur.",
    tip_title: str = "💡 Le saviez-vous ?",
    tip_content: str = "Suivre son humeur quotidiennement aide à identifier les patterns et améliorer son bien-être mental."
) -> str:
    """
    Génère le HTML pour un état vide.

    Args:
        icon: Emoji à afficher
        title: Titre principal
        description: Description
        tip_title: Titre du conseil
        tip_content: Contenu du conseil

    Returns:
        HTML string du composant
    """
    return f"""
    <div style="
        background: linear-gradient(135deg, var(--bg-tertiary) 0%, var(--color-primary-glow) 100%);
        padding: 4rem 2rem;
        border-radius: var(--radius-xl);
        text-align: center;
        border: 2px dashed var(--border-accent);
        animation: fadeInUp 0.5s ease-out;
    ">
        <div style="font-size: 5rem; margin-bottom: 2rem; animation: bounce 2s infinite;">
            {icon}
        </div>
        <div style="font-size: 1.5rem; font-weight: 700; color: var(--color-primary); margin-bottom: 1rem;">
            {title}
        </div>
        <div style="font-size: 1.1rem; color: var(--text-secondary); margin-bottom: 2rem; line-height: 1.7;">
            {description}
        </div>
        <div style="
            background-color: var(--bg-elevated);
            padding: 2rem;
            border-radius: var(--radius-md);
            box-shadow: var(--shadow-md);
            max-width: 500px;
            margin: 0 auto;
            border: 1px solid var(--border-primary);
        ">
            <div style="color: var(--color-primary); font-weight: 600; font-size: 1.05rem; margin-bottom: 0.75rem;">
                {tip_title}
            </div>
            <div style="color: var(--text-secondary); font-size: 1rem; line-height: 1.6;">
                {tip_content}
            </div>
        </div>
    </div>
    """


def page_header(title: str, emoji: str, description: str) -> str:
    """
    Génère le HTML pour l'en-tête de page.

    Args:
        title: Titre de la page
        emoji: Emoji associé
        description: Description de la page

    Returns:
        HTML string du composant
    """
    return f"""
    <div style="animation: fadeInDown 0.4s ease-out; margin-bottom: 2rem;">
        <h1 style="
            font-size: 2.5rem;
            color: var(--text-primary);
            font-weight: 700;
            margin-bottom: 0.75rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            letter-spacing: -0.02em;
        ">
            <span style="filter: drop-shadow(0 2px 8px var(--color-primary-glow));">
                {emoji}
            </span>
            {title}
        </h1>
        <p style="
            font-size: 1.15rem;
            color: var(--text-secondary);
            margin: 0;
            line-height: 1.7;
        ">
            {description}
        </p>
    </div>
    """