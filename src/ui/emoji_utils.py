"""
Emoji utilities for accessible and responsive emoji rendering in Streamlit.

This module provides helper functions to render emojis with proper accessibility
support (ARIA labels), CSS classes, and semantic HTML structure.
"""

from typing import Optional


def emoji(
    icon: str,
    label: str,
    size: str = "md",
    animated: bool = False,
    interactive: bool = False,
    css_class: str = "",
) -> str:
    """
    Generate accessible emoji HTML with proper ARIA labels and CSS classes.

    Args:
        icon: The emoji character (e.g., "😊", "🌸")
        label: Accessible label for screen readers (e.g., "Happy face", "Flower")
        size: Size class - one of: xs, sm, md, lg, xl, 2xl, 3xl (default: md)
        animated: Whether to apply floating animation (default: False)
        interactive: Whether to apply hover interaction (default: False)
        css_class: Additional CSS classes to apply

    Returns:
        HTML string with accessible emoji markup

    Example:
        >>> emoji("😊", "Happy face", size="xl", interactive=True)
        '<span class="emoji emoji-xl emoji-interactive" role="img" aria-label="Happy face">😊</span>'
    """
    classes = ["emoji", f"emoji-{size}"]

    if animated:
        classes.append("emoji-animated")
    if interactive:
        classes.append("emoji-interactive")
    if css_class:
        classes.append(css_class)

    class_str = " ".join(classes)

    return f'<span class="{class_str}" role="img" aria-label="{label}">{icon}</span>'


def emoji_hero(icon: str, label: str) -> str:
    """
    Generate a hero-sized emoji with entrance animation.

    Args:
        icon: The emoji character
        label: Accessible label for screen readers

    Returns:
        HTML string for hero emoji

    Example:
        >>> emoji_hero("🌸", "Serene flower logo")
    """
    return f'<span class="emoji emoji-hero" role="img" aria-label="{label}">{icon}</span>'


def emoji_mood(icon: str, label: str, mood_score: Optional[int] = None) -> str:
    """
    Generate a mood emoji with appropriate styling.

    Args:
        icon: The emoji character
        label: Accessible label describing the mood
        mood_score: Optional mood score (1-10) for additional context

    Returns:
        HTML string for mood emoji

    Example:
        >>> emoji_mood("😊", "Excellent mood", mood_score=10)
    """
    aria_label = label
    if mood_score:
        aria_label = f"{label} (score: {mood_score}/10)"

    return f'<span class="emoji emoji-mood" role="img" aria-label="{aria_label}">{icon}</span>'


def emoji_button(icon: str, label: str) -> str:
    """
    Generate an emoji for use in buttons.

    Args:
        icon: The emoji character
        label: Accessible label for the emoji

    Returns:
        HTML string for button emoji

    Example:
        >>> emoji_button("💬", "Start conversation")
    """
    return f'<span class="emoji emoji-button" role="img" aria-label="{label}">{icon}</span>'


# Mood emoji mappings with accessibility labels
MOOD_EMOJIS = {
    1: {"emoji": "😢", "label": "Très difficile - très triste", "color": "#F56565"},
    2: {"emoji": "😢", "label": "Très difficile - triste", "color": "#F56565"},
    3: {"emoji": "😔", "label": "Difficile - préoccupé", "color": "#ED8936"},
    4: {"emoji": "😔", "label": "Difficile - un peu bas", "color": "#ED8936"},
    5: {"emoji": "😐", "label": "Neutre - ni bien ni mal", "color": "#718096"},
    6: {"emoji": "😐", "label": "Neutre - correct", "color": "#718096"},
    7: {"emoji": "🙂", "label": "Bien - positif", "color": "#6B46C1"},
    8: {"emoji": "🙂", "label": "Bien - de bonne humeur", "color": "#6B46C1"},
    9: {"emoji": "😊", "label": "Excellent - très content", "color": "#48BB78"},
    10: {"emoji": "😊", "label": "Excellent - fantastique", "color": "#48BB78"},
}


def get_mood_emoji(score: int) -> dict:
    """
    Get mood emoji data for a given score.

    Args:
        score: Mood score from 1-10

    Returns:
        Dictionary with emoji, label, and color

    Example:
        >>> get_mood_emoji(8)
        {'emoji': '🙂', 'label': 'Bien - de bonne humeur', 'color': '#6B46C1'}
    """
    if score < 1 or score > 10:
        raise ValueError("Score must be between 1 and 10")

    return MOOD_EMOJIS[score]


def render_mood_emoji(score: int) -> str:
    """
    Render a mood emoji with full accessibility support.

    Args:
        score: Mood score from 1-10

    Returns:
        HTML string for mood emoji with proper ARIA labels

    Example:
        >>> render_mood_emoji(8)
    """
    mood_data = get_mood_emoji(score)
    return emoji_mood(mood_data["emoji"], mood_data["label"], mood_score=score)
