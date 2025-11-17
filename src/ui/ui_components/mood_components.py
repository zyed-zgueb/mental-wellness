"""
Composants UI réutilisables pour l'application Serene
Facilite la maintenance et garantit la cohérence visuelle
"""

from src.ui.styles.serene_styles import COLORS


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
        margin: 1.5rem 0; 
        padding: 2rem;
        background: linear-gradient(135deg, {COLORS['neutral_bg']} 0%, {mood_color}15 100%);
        border-radius: 16px;
        border: 2px solid {mood_color}20;
    ">
        <div style="font-size: 4rem; margin-bottom: 1rem;">{mood_emoji}</div>
        <div style="font-size: 1.5rem; font-weight: 600; color: {mood_color}; margin-bottom: 0.25rem;">
            {mood_label}
        </div>
        <div style="font-size: 1rem; color: {COLORS['text_light']};">
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
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_dark']} 100%);
        padding: 1.25rem 1.75rem; 
        border-radius: 12px; 
        margin-bottom: 1.5rem;
        box-shadow: {COLORS['shadow_md']};
        animation: fadeInUp 0.4s ease-out;
    ">
        <p style="color: white; margin: 0; font-size: 1.05rem; font-weight: 500;">
            <strong>{total_checkins} check-in(s)</strong> enregistré(s) ce mois-ci
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
            color: {COLORS['text_medium']}; 
            margin-top: 0.75rem; 
            line-height: 1.6; 
            font-size: 0.95rem;
            padding: 0.75rem;
            background-color: {COLORS['neutral_bg']};
            border-radius: 8px;
            font-style: italic;
        ">
            {safe_notes}
        </div>
        """
    
    # Animation delay basée sur l'index
    animation_delay = index * 0.05
    
    return f"""
    <div class="history-card" style="
        background-color: {COLORS['white']}; 
        padding: 1.5rem; 
        border-radius: 12px; 
        margin-bottom: 1rem;
        border-left: 4px solid {mood_color}; 
        box-shadow: {COLORS['shadow_sm']};
        animation: fadeInUp {0.4 + animation_delay}s ease-out;
    ">
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            <div style="font-size: 2.5rem; margin-right: 1rem;">{mood_emoji}</div>
            <div style="flex: 1;">
                <div style="font-weight: 600; font-size: 1.1rem; color: {mood_color};">
                    {mood_label}
                </div>
                <div style="font-size: 0.875rem; color: {COLORS['text_light']}; margin-top: 0.25rem;">
                    📅 {formatted_date} à {formatted_time} · 
                    <span style="color: {mood_color}; font-weight: 500;">
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
        background: linear-gradient(135deg, {COLORS['neutral_bg']} 0%, {COLORS['primary_lighter']}30 100%);
        padding: 3rem 2rem; 
        border-radius: 16px;
        text-align: center; 
        border: 2px dashed {COLORS['primary_light']};
        animation: fadeInUp 0.5s ease-out;
    ">
        <div style="font-size: 4rem; margin-bottom: 1.5rem;">{icon}</div>
        <div style="font-size: 1.3rem; font-weight: 600; color: {COLORS['primary']}; margin-bottom: 0.75rem;">
            {title}
        </div>
        <div style="font-size: 1rem; color: {COLORS['text_medium']}; margin-bottom: 1.5rem; line-height: 1.6;">
            {description}
        </div>
        <div style="
            background-color: {COLORS['white']}; 
            padding: 1.5rem; 
            border-radius: 12px;
            box-shadow: {COLORS['shadow_sm']};
            max-width: 500px;
            margin: 0 auto;
        ">
            <div style="color: {COLORS['primary']}; font-weight: 500; font-size: 0.95rem; margin-bottom: 0.5rem;">
                {tip_title}
            </div>
            <div style="color: {COLORS['text_medium']}; font-size: 0.9rem; line-height: 1.5;">
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
    <div style="animation: fadeInDown 0.4s ease-out; margin-bottom: 1.5rem;">
        <h1 style="
            font-size: 2.25rem; 
            color: {COLORS['text_dark']}; 
            font-weight: 600; 
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        ">
            {emoji} {title}
        </h1>
        <p style="
            font-size: 1.075rem; 
            color: {COLORS['text_medium']}; 
            margin: 0;
            line-height: 1.6;
        ">
            {description}
        </p>
    </div>
    """