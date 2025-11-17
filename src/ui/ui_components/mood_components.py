"""
Composants UI réutilisables pour l'application Serene
Design minimaliste inspiré des galeries d'art et étiquettes de musée
Style: Bauhaus + Calme scandinave + Haute typographie
"""

from src.ui.styles.serene_styles import COLORS


def mood_display_card(mood_score: int, mood_emoji: str, mood_label: str, mood_color: str) -> str:
    """
    Génère le HTML pour l'affichage du mood actuel - Gallery minimal style.

    Args:
        mood_score: Score de l'humeur (0-10)
        mood_emoji: Emoji (non utilisé dans le design minimal)
        mood_label: Label textuel de l'humeur
        mood_color: Couleur (non utilisée, on utilise noir/gris)

    Returns:
        HTML string du composant
    """
    return f"""
    <div class="mood-display" style="
        text-align: center;
        margin: 2rem 0 3rem 0;
        padding: 3rem 2rem;
        background-color: {COLORS['white']};
        border: 1px solid {COLORS['line_light']};
        border-radius: 0;
    ">
        <div style="
            font-family: 'Cormorant Garamond', serif;
            font-size: 3.5rem;
            font-weight: 300;
            color: {COLORS['black']};
            margin-bottom: 0.5rem;
            letter-spacing: 0.02em;
        ">
            {mood_score}
        </div>
        <div style="
            font-family: 'Inter', sans-serif;
            font-size: 0.75rem;
            font-weight: 400;
            color: {COLORS['gray_medium']};
            margin-bottom: 1.5rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
        ">
            {mood_label}
        </div>
        <div style="
            width: 60px;
            height: 1px;
            background-color: {COLORS['line_dark']};
            margin: 0 auto;
        "></div>
    </div>
    """


def stats_banner(total_checkins: int) -> str:
    """
    Génère le HTML pour la bannière de statistiques - Museum label style.

    Args:
        total_checkins: Nombre total de check-ins

    Returns:
        HTML string du composant
    """
    return f"""
    <div style="
        background-color: {COLORS['white']};
        padding: 1.5rem 2rem;
        border: 1px solid {COLORS['line_light']};
        border-left: 2px solid {COLORS['black']};
        margin-bottom: 2rem;
        box-shadow: {COLORS['shadow_subtle']};
        animation: fadeInUp 0.4s ease-out;
    ">
        <p style="
            font-family: 'Inter', sans-serif;
            color: {COLORS['charcoal']};
            margin: 0;
            font-size: 0.875rem;
            font-weight: 300;
            letter-spacing: 0.02em;
        ">
            <span style="
                font-family: 'Cormorant Garamond', serif;
                font-size: 1.75rem;
                font-weight: 300;
                color: {COLORS['black']};
                margin-right: 0.5rem;
            ">{total_checkins}</span>
            <span style="
                text-transform: uppercase;
                font-size: 0.75rem;
                letter-spacing: 0.1em;
                color: {COLORS['gray_medium']};
            ">check-in(s) ce mois-ci</span>
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
    Génère le HTML pour une carte d'historique - Museum label style.
    Design inspiré des étiquettes de musée: lignes fines, typographie raffinée, géométrie stricte.

    Args:
        checkin: Dictionnaire contenant les données du check-in
        mood_emoji: Emoji (non utilisé)
        mood_label: Label de l'humeur
        mood_color: Couleur (non utilisée)
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
            font-family: 'Inter', sans-serif;
            color: {COLORS['gray_dark']};
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid {COLORS['line_light']};
            line-height: 1.8;
            font-size: 0.875rem;
            font-weight: 300;
            font-style: italic;
        ">
            {safe_notes}
        </div>
        """

    # Animation delay basée sur l'index
    animation_delay = index * 0.05

    # Petit marqueur géométrique pour le score
    marker_size = min(8 + checkin["mood_score"], 16)

    return f"""
    <div class="history-card" style="
        background-color: {COLORS['white']};
        padding: 1.5rem 2rem;
        border: 1px solid {COLORS['line_light']};
        margin-bottom: 1rem;
        box-shadow: {COLORS['shadow_subtle']};
        animation: fadeInUp {0.4 + animation_delay}s ease-out;
        transition: all 0.3s ease;
    ">
        <div style="display: flex; align-items: flex-start; gap: 1.5rem;">
            <!-- Marqueur géométrique -->
            <div style="
                width: {marker_size}px;
                height: {marker_size}px;
                background-color: {COLORS['black']};
                flex-shrink: 0;
                margin-top: 0.25rem;
            "></div>

            <!-- Contenu -->
            <div style="flex: 1;">
                <!-- Date et heure - Style musée -->
                <div style="
                    font-family: 'Inter', sans-serif;
                    font-size: 0.6875rem;
                    font-weight: 400;
                    color: {COLORS['gray_light']};
                    letter-spacing: 0.1em;
                    text-transform: uppercase;
                    margin-bottom: 0.5rem;
                ">
                    {formatted_date} · {formatted_time}
                </div>

                <!-- Score et label -->
                <div style="display: flex; align-items: baseline; gap: 1rem; margin-bottom: 0.25rem;">
                    <div style="
                        font-family: 'Cormorant Garamond', serif;
                        font-size: 2rem;
                        font-weight: 300;
                        color: {COLORS['black']};
                        line-height: 1;
                    ">
                        {checkin["mood_score"]}
                    </div>
                    <div style="
                        font-family: 'Inter', sans-serif;
                        font-size: 0.75rem;
                        font-weight: 400;
                        color: {COLORS['gray_medium']};
                        letter-spacing: 0.05em;
                        text-transform: uppercase;
                    ">
                        {mood_label}
                    </div>
                </div>

                {notes_html}
            </div>
        </div>
    </div>
    """


def empty_state(
    icon: str = "",
    title: str = "Votre journal de bien-être vous attend",
    description: str = "Créez votre premier check-in pour commencer à suivre votre humeur.",
    tip_title: str = "Le saviez-vous ?",
    tip_content: str = "Suivre son humeur quotidiennement aide à identifier les patterns et améliorer son bien-être mental."
) -> str:
    """
    Génère le HTML pour un état vide - Minimal gallery style.

    Args:
        icon: Icône (non utilisée dans le design minimal)
        title: Titre principal
        description: Description
        tip_title: Titre du conseil
        tip_content: Contenu du conseil

    Returns:
        HTML string du composant
    """
    return f"""
    <div style="
        background-color: {COLORS['ivory_dark']};
        padding: 4rem 3rem;
        border: 1px solid {COLORS['line_light']};
        text-align: center;
        animation: fadeInUp 0.5s ease-out;
    ">
        <div style="
            font-family: 'Cormorant Garamond', serif;
            font-size: 1.75rem;
            font-weight: 300;
            color: {COLORS['black']};
            margin-bottom: 1rem;
            letter-spacing: 0.02em;
        ">
            {title}
        </div>
        <div style="
            font-family: 'Inter', sans-serif;
            font-size: 0.9375rem;
            font-weight: 300;
            color: {COLORS['gray_dark']};
            margin-bottom: 2.5rem;
            line-height: 1.8;
            max-width: 500px;
            margin-left: auto;
            margin-right: auto;
        ">
            {description}
        </div>

        <!-- Séparateur géométrique -->
        <div style="
            width: 80px;
            height: 1px;
            background-color: {COLORS['line_dark']};
            margin: 2rem auto;
        "></div>

        <!-- Conseil -->
        <div style="
            background-color: {COLORS['white']};
            padding: 2rem;
            border: 1px solid {COLORS['line_light']};
            box-shadow: {COLORS['shadow_subtle']};
            max-width: 500px;
            margin: 0 auto;
            text-align: left;
        ">
            <div style="
                font-family: 'Inter', sans-serif;
                color: {COLORS['black']};
                font-weight: 400;
                font-size: 0.75rem;
                letter-spacing: 0.1em;
                text-transform: uppercase;
                margin-bottom: 0.75rem;
            ">
                {tip_title}
            </div>
            <div style="
                font-family: 'Inter', sans-serif;
                color: {COLORS['gray_dark']};
                font-size: 0.875rem;
                font-weight: 300;
                line-height: 1.7;
            ">
                {tip_content}
            </div>
        </div>
    </div>
    """


def page_header(title: str, emoji: str, description: str) -> str:
    """
    Génère le HTML pour l'en-tête de page - Gallery title style.

    Args:
        title: Titre de la page
        emoji: Emoji (non utilisé dans le design minimal)
        description: Description de la page

    Returns:
        HTML string du composant
    """
    return f"""
    <div style="
        animation: fadeInDown 0.4s ease-out;
        margin-bottom: 3rem;
        padding-bottom: 2rem;
        border-bottom: 1px solid {COLORS['line_light']};
    ">
        <h1 style="
            font-family: 'Cormorant Garamond', serif;
            font-size: 3rem;
            color: {COLORS['black']};
            font-weight: 300;
            margin-bottom: 1rem;
            letter-spacing: 0.02em;
            line-height: 1.1;
        ">
            {title}
        </h1>
        <p style="
            font-family: 'Inter', sans-serif;
            font-size: 0.9375rem;
            color: {COLORS['gray_dark']};
            margin: 0;
            line-height: 1.8;
            font-weight: 300;
            max-width: 600px;
        ">
            {description}
        </p>
    </div>
    """