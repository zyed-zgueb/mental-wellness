"""
Styles CSS centralisés pour l'application Serene
Design minimaliste inspiré des galeries d'art contemporain
Palette: ivoire, noir, gris - Esthétique Bauhaus et calme scandinave
"""

# Palette de couleurs minimaliste - Gallery Style
COLORS = {
    # Fond - Tons ivoire doux et chaleureux
    "ivory": "#FAF8F3",           # Ivoire principal (fond)
    "ivory_dark": "#F5F3EE",      # Ivoire légèrement plus foncé
    "ivory_darker": "#EBE8E0",    # Ivoire encore plus foncé pour contraste subtil
    "white": "#FFFFFF",           # Blanc pur

    # Texte - Noir et gris sophistiqués
    "black": "#000000",           # Noir pur pour titres
    "charcoal": "#1A1A1A",        # Charbon pour texte principal
    "gray_dark": "#4A4A4A",       # Gris foncé pour texte secondaire
    "gray_medium": "#6B6B6B",     # Gris moyen
    "gray_light": "#9E9E9E",      # Gris clair pour labels
    "gray_lighter": "#D4D4D4",    # Gris très clair pour séparateurs

    # Accents géométriques (très subtils)
    "line_dark": "#2A2A2A",       # Lignes foncées
    "line_light": "#E0E0E0",      # Lignes claires

    # Mood colors (palette désaturée et sophistiquée)
    "mood_excellent": "#4A4A4A",       # Gris foncé
    "mood_bien": "#6B6B6B",            # Gris moyen
    "mood_neutre": "#9E9E9E",          # Gris clair
    "mood_difficile": "#6B6B6B",       # Gris moyen
    "mood_tres_difficile": "#4A4A4A",  # Gris foncé

    # Feedback (très subtil, monochrome)
    "success": "#2A2A2A",
    "error": "#4A4A4A",
    "warning": "#6B6B6B",

    # Ombres (ultra-subtiles)
    "shadow_subtle": "0 1px 2px rgba(0, 0, 0, 0.03)",
    "shadow_soft": "0 2px 4px rgba(0, 0, 0, 0.04)",
    "shadow_medium": "0 4px 8px rgba(0, 0, 0, 0.05)",
}


def get_main_css():
    """Retourne le CSS principal de l'application - Gallery Minimalist Style."""
    return f"""
    <style>
    /* ==================== GOOGLE FONTS - Elegant Sans-Serif ==================== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Cormorant+Garamond:wght@300;400;500&display=swap');

    /* ==================== ROOT VARIABLES - GALLERY AESTHETICS ==================== */
    :root {{
        /* Couleurs ivoire et noirs */
        --ivory: {COLORS['ivory']};
        --ivory-dark: {COLORS['ivory_dark']};
        --ivory-darker: {COLORS['ivory_darker']};
        --white: {COLORS['white']};
        --black: {COLORS['black']};
        --charcoal: {COLORS['charcoal']};
        --gray-dark: {COLORS['gray_dark']};
        --gray-medium: {COLORS['gray_medium']};
        --gray-light: {COLORS['gray_light']};
        --gray-lighter: {COLORS['gray_lighter']};
        --line-dark: {COLORS['line_dark']};
        --line-light: {COLORS['line_light']};

        /* Variables de compatibilité (mapping anciennes -> nouvelles) */
        --color-primary: {COLORS['black']};
        --color-primary-light: {COLORS['gray_medium']};
        --color-primary-lighter: {COLORS['gray_lighter']};
        --color-primary-dark: {COLORS['charcoal']};
        --color-neutral-bg: {COLORS['ivory']};
        --color-neutral-light: {COLORS['ivory_dark']};
        --color-white: {COLORS['white']};
        --color-text-dark: {COLORS['charcoal']};
        --color-text-medium: {COLORS['gray_dark']};
        --color-text-light: {COLORS['gray_light']};
        --color-success: {COLORS['success']};
        --color-error: {COLORS['error']};
        --text-primary: {COLORS['white']};

        /* Ombres subtiles */
        --shadow-subtle: {COLORS['shadow_subtle']};
        --shadow-soft: {COLORS['shadow_soft']};
        --shadow-medium: {COLORS['shadow_medium']};
        --shadow-sm: {COLORS['shadow_subtle']};
        --shadow-md: {COLORS['shadow_soft']};
        --shadow-lg: {COLORS['shadow_medium']};

        /* Géométrie Bauhaus - lignes fines, pas de border-radius */
        --border-thin: 1px;
        --border-medium: 2px;
        --radius-none: 0px;
        --radius-subtle: 2px;
        --radius-sm: 2px;
        --radius-md: 2px;
        --radius-lg: 2px;

        /* Transition élégante */
        --transition-elegant: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        --transition-smooth: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

        /* Espacements généreux - Respiration visuelle */
        --space-xs: 0.5rem;
        --space-sm: 1rem;
        --space-md: 2rem;
        --space-lg: 3rem;
        --space-xl: 4rem;
    }}

    /* ==================== ANIMATIONS - DOUCES ET ÉLÉGANTES ==================== */
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}

    @keyframes fadeInUp {{
        from {{
            opacity: 0;
            transform: translateY(10px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    @keyframes fadeInDown {{
        from {{
            opacity: 0;
            transform: translateY(-5px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    /* ==================== GLOBAL STYLES - GALLERY SPACE ==================== */
    * {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }}

    body {{
        background-color: var(--ivory);
        color: var(--charcoal);
    }}

    .main {{
        background-color: var(--ivory);
        padding: var(--space-xl) var(--space-lg);
    }}

    .main .block-container {{
        padding-top: var(--space-lg);
        max-width: 800px;
        padding-left: var(--space-md);
        padding-right: var(--space-md);
    }}

    /* Espacements généreux entre éléments */
    .element-container {{
        margin-bottom: var(--space-md);
    }}

    /* ==================== SIDEBAR - VERTICAL GALLERY NAVIGATION ==================== */
    [data-testid="stSidebar"] {{
        background-color: var(--white);
        border-right: var(--border-thin) solid var(--line-light);
        padding: var(--space-xl) 0;
        min-width: 240px !important;
        max-width: 240px !important;
    }}

    [data-testid="stSidebar"] > div:first-child {{
        padding: 0 var(--space-md);
    }}

    [data-testid="stSidebar"] h1 {{
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.75rem;
        color: var(--black);
        font-weight: 300;
        letter-spacing: 0.05em;
        margin-bottom: var(--space-lg);
        text-align: left;
        text-transform: uppercase;
        border-bottom: var(--border-thin) solid var(--line-light);
        padding-bottom: var(--space-sm);
    }}

    /* Navigation buttons - Style minimal */
    [data-testid="stSidebar"] .stRadio > div {{
        gap: var(--space-xs);
    }}

    [data-testid="stSidebar"] .stRadio label {{
        background-color: transparent;
        padding: var(--space-sm) 0;
        border-radius: var(--radius-none);
        transition: var(--transition-elegant);
        border: none;
        border-left: var(--border-medium) solid transparent;
        padding-left: var(--space-sm);
        cursor: pointer;
        font-size: 0.875rem;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        font-weight: 400;
        color: var(--gray-medium);
    }}

    [data-testid="stSidebar"] .stRadio label:hover {{
        color: var(--black);
        border-left-color: var(--gray-lighter);
    }}

    /* ==================== TYPOGRAPHY - HIGH CONTRAST, REFINED ==================== */
    h1, h2, h3, h4 {{
        font-family: 'Cormorant Garamond', serif;
        color: var(--black);
        font-weight: 400;
        line-height: 1.2;
        letter-spacing: 0.02em;
        margin-top: 0;
    }}

    h1 {{
        font-size: 3rem;
        margin-bottom: var(--space-sm);
        font-weight: 300;
    }}

    h2 {{
        font-size: 2rem;
        margin: var(--space-lg) 0 var(--space-md) 0;
        font-weight: 300;
    }}

    h3 {{
        font-size: 1.5rem;
        margin: var(--space-md) 0 var(--space-sm) 0;
        font-weight: 400;
    }}

    h4 {{
        font-size: 1.125rem;
        margin: var(--space-sm) 0;
        font-weight: 400;
    }}

    p {{
        font-family: 'Inter', sans-serif;
        color: var(--gray-dark);
        line-height: 1.8;
        font-size: 0.9375rem;
        font-weight: 300;
    }}

    /* ==================== FORMS - EDITORIAL LUXURY ==================== */

    /* Form container - Minimal white box */
    .stForm {{
        background-color: var(--white);
        padding: var(--space-lg);
        border-radius: var(--radius-none);
        box-shadow: var(--shadow-soft);
        margin: var(--space-lg) 0;
        border: var(--border-thin) solid var(--line-light);
    }}

    /* ==================== SLIDER - GEOMETRIC MINIMALIST ==================== */
    .stSlider {{
        padding: var(--space-lg) 0;
    }}

    .stSlider > label {{
        font-family: 'Inter', sans-serif;
        font-weight: 300 !important;
        color: var(--gray-dark) !important;
        font-size: 0.875rem !important;
        letter-spacing: 0.03em !important;
        text-transform: uppercase !important;
    }}

    .stSlider [data-baseweb="slider"] {{
        margin-top: var(--space-md);
        padding: 0 var(--space-xs);
    }}

    /* Poignée circulaire simple et élégante */
    .stSlider [role="slider"] {{
        background-color: var(--black) !important;
        width: 16px !important;
        height: 16px !important;
        box-shadow: var(--shadow-subtle) !important;
        border: var(--border-thin) solid var(--white) !important;
        transition: var(--transition-elegant) !important;
    }}

    .stSlider [role="slider"]:hover {{
        box-shadow: 0 0 0 8px rgba(0, 0, 0, 0.05) !important;
        transform: scale(1.1);
    }}

    .stSlider [role="slider"]:active {{
        transform: scale(1.15);
    }}

    /* Ligne du slider - fine et géométrique */
    .stSlider [data-baseweb="slider"] > div:first-child {{
        background-color: var(--line-light) !important;
        height: 1px !important;
    }}

    /* Track rempli (avant le thumb) */
    .stSlider [data-baseweb="slider"] > div:first-child > div {{
        background-color: var(--line-dark) !important;
        height: 1px !important;
    }}

    /* Labels du slider - typographie raffinée */
    [data-testid="stSliderThumbValue"],
    [data-testid="stSliderTickBar"] {{
        font-family: 'Inter', sans-serif !important;
        font-size: 0.75rem !important;
        font-weight: 300 !important;
        color: var(--gray-light) !important;
        letter-spacing: 0.02em !important;
    }}

    [data-testid="stSliderThumbValue"] {{
        font-size: 0.875rem !important;
        font-weight: 400 !important;
        color: var(--black) !important;
    }}

    /* ==================== TEXT AREA - HIGH-END EDITORIAL ==================== */
    .stTextArea > label {{
        font-family: 'Inter', sans-serif;
        font-weight: 300 !important;
        color: var(--gray-dark) !important;
        font-size: 0.875rem !important;
        letter-spacing: 0.03em !important;
        text-transform: uppercase !important;
        margin-bottom: var(--space-sm);
    }}

    .stTextArea textarea {{
        border-radius: var(--radius-none) !important;
        border: var(--border-thin) solid var(--line-light) !important;
        padding: var(--space-sm) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9375rem !important;
        font-weight: 300 !important;
        line-height: 1.8 !important;
        transition: var(--transition-elegant) !important;
        background-color: var(--white) !important;
        color: var(--charcoal) !important;
    }}

    .stTextArea textarea:focus {{
        border-color: var(--black) !important;
        box-shadow: none !important;
        outline: none !important;
    }}

    .stTextArea textarea::placeholder {{
        color: var(--gray-light) !important;
        font-style: italic !important;
        font-weight: 300 !important;
    }}

    /* ==================== SUBMIT BUTTON - MINIMALIST WITH FONTAWESOME ==================== */
    .stForm button[kind="primary"] {{
        background-color: var(--black) !important;
        color: var(--white) !important;
        border: none !important;
        padding: var(--space-sm) var(--space-lg) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.875rem !important;
        font-weight: 400 !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
        border-radius: var(--radius-none) !important;
        transition: var(--transition-elegant) !important;
        box-shadow: none !important;
        width: 100%;
        cursor: pointer;
        position: relative;
    }}

    /* Icône FontAwesome subtile sur les boutons de formulaire */
    .stForm button[kind="primary"]::before {{
        font-family: 'Font Awesome 6 Free' !important;
        font-weight: 900 !important;
        content: '\\f00c' !important; /* fa-check - icône de validation */
        margin-right: 0.5rem !important;
        opacity: 0.7 !important;
        font-size: 0.75rem !important;
    }}

    .stForm button[kind="primary"]:hover {{
        background-color: var(--charcoal) !important;
        box-shadow: var(--shadow-soft) !important;
    }}

    .stForm button[kind="primary"]:hover::before {{
        opacity: 1 !important;
    }}

    .stForm button[kind="primary"]:active {{
        transform: scale(0.98);
    }}

    /* Boutons primaires généraux (disclaimer, etc.) - Contraste élevé */
    button[kind="primary"],
    .stButton > button[kind="primary"] {{
        background-color: var(--black) !important;
        color: var(--white) !important;
        border: none !important;
        padding: var(--space-sm) var(--space-lg) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.875rem !important;
        font-weight: 400 !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
        border-radius: var(--radius-none) !important;
        transition: var(--transition-elegant) !important;
        position: relative;
        box-shadow: none !important;
    }}

    button[kind="primary"]::after,
    .stButton > button[kind="primary"]::after {{
        font-family: 'Font Awesome 6 Free' !important;
        font-weight: 900 !important;
        content: '\\f061' !important; /* fa-arrow-right - flèche droite */
        margin-left: 0.5rem !important;
        opacity: 0.7 !important;
        font-size: 0.75rem !important;
        transition: var(--transition-elegant) !important;
    }}

    button[kind="primary"]:hover,
    .stButton > button[kind="primary"]:hover {{
        background-color: var(--charcoal) !important;
        box-shadow: var(--shadow-soft) !important;
    }}

    button[kind="primary"]:hover::after,
    .stButton > button[kind="primary"]:hover::after {{
        opacity: 1 !important;
        transform: translateX(2px);
    }}

    /* Texte des boutons - Forcer blanc sur fond noir */
    button[kind="primary"] p,
    .stButton > button[kind="primary"] p,
    button[kind="primary"] div,
    .stButton > button[kind="primary"] div {{
        color: var(--white) !important;
    }}

    /* ==================== DIVIDER - THIN GEOMETRIC LINE ==================== */
    hr {{
        margin: var(--space-lg) 0;
        border: none;
        border-top: var(--border-thin) solid var(--line-light);
        opacity: 1;
    }}

    /* ==================== SUCCESS/ERROR MESSAGES - SUBTLE ==================== */
    .stSuccess,
    .stError,
    .stWarning {{
        background-color: var(--white) !important;
        border: var(--border-thin) solid var(--line-light) !important;
        border-left: var(--border-medium) solid var(--black) !important;
        padding: var(--space-sm) var(--space-md) !important;
        border-radius: var(--radius-none) !important;
        animation: fadeInDown 0.3s ease-out;
        box-shadow: var(--shadow-subtle) !important;
    }}

    .stSuccess p,
    .stError p,
    .stWarning p {{
        font-family: 'Inter', sans-serif !important;
        color: var(--charcoal) !important;
        font-weight: 300 !important;
        font-size: 0.875rem !important;
        line-height: 1.6 !important;
    }}

    /* ==================== SCROLLBAR - MINIMALIST ==================== */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}

    ::-webkit-scrollbar-track {{
        background: var(--ivory);
    }}

    ::-webkit-scrollbar-thumb {{
        background: var(--gray-lighter);
        border-radius: 0;
    }}

    ::-webkit-scrollbar-thumb:hover {{
        background: var(--gray-light);
    }}

    /* ==================== CHAT MESSAGES - MINIMAL BUBBLES ==================== */
    .stChatMessage {{
        border-radius: var(--radius-none);
        padding: var(--space-md);
        margin-bottom: var(--space-sm);
        box-shadow: var(--shadow-subtle);
        animation: fadeInUp 0.3s ease-out;
        border: var(--border-thin) solid var(--line-light);
    }}

    .stChatMessage[data-testid="chat-message-user"] {{
        background-color: var(--black) !important;
        color: var(--white) !important;
        margin-left: var(--space-lg);
        border-color: var(--black);
    }}

    .stChatMessage[data-testid="chat-message-assistant"] {{
        background-color: var(--white) !important;
        color: var(--charcoal) !important;
        margin-right: var(--space-lg);
        border: var(--border-thin) solid var(--line-light);
    }}

    /* Texte dans les messages */
    .stChatMessage p {{
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9375rem !important;
        line-height: 1.8 !important;
        font-weight: 300 !important;
        margin: 0 !important;
    }}

    .stChatMessage[data-testid="chat-message-user"] p {{
        color: var(--white) !important;
    }}

    .stChatMessage[data-testid="chat-message-assistant"] p {{
        color: var(--charcoal) !important;
    }}

    /* Avatars minimalistes - Remplacer emojis par des initiales */
    .stChatMessage .stAvatar {{
        width: 32px !important;
        height: 32px !important;
        border-radius: 0 !important;
        background-color: transparent !important;
        border: var(--border-thin) solid var(--line-light) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.75rem !important;
        font-weight: 400 !important;
        color: var(--gray-dark) !important;
    }}

    .stChatMessage[data-testid="chat-message-user"] .stAvatar {{
        background-color: var(--charcoal) !important;
        border-color: var(--charcoal) !important;
        color: var(--white) !important;
    }}

    .stChatMessage[data-testid="chat-message-assistant"] .stAvatar {{
        background-color: var(--white) !important;
        border-color: var(--line-dark) !important;
        color: var(--black) !important;
    }}

    /* Masquer les emojis par défaut dans les avatars */
    .stChatMessage .stAvatar img {{
        display: none !important;
    }}

    /* ==================== EXPANDER - MINIMAL ==================== */
    .streamlit-expanderHeader {{
        background-color: var(--white);
        border-radius: var(--radius-none);
        padding: var(--space-sm) var(--space-md);
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        font-size: 0.875rem;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        transition: var(--transition-elegant);
        border: var(--border-thin) solid var(--line-light);
        color: var(--charcoal);
    }}

    .streamlit-expanderHeader:hover {{
        background-color: var(--ivory-dark);
        border-color: var(--line-dark);
    }}

    /* ==================== METRICS - MUSEUM LABEL STYLE ==================== */
    div[data-testid="stMetric"] {{
        background-color: var(--white);
        padding: var(--space-md);
        border-radius: var(--radius-none);
        box-shadow: var(--shadow-subtle);
        transition: var(--transition-elegant);
        border: var(--border-thin) solid var(--line-light);
    }}

    div[data-testid="stMetric"]:hover {{
        box-shadow: var(--shadow-soft);
    }}

    div[data-testid="stMetric"] [data-testid="stMetricLabel"] {{
        font-family: 'Inter', sans-serif !important;
        font-size: 0.75rem !important;
        font-weight: 400 !important;
        color: var(--gray-medium) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }}

    div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 2.5rem !important;
        font-weight: 300 !important;
        color: var(--black) !important;
    }}

    /* ==================== PLOTS & CHARTS - CLEAN CONTAINERS ==================== */
    div[data-testid="stPlotlyChart"] {{
        background-color: var(--white);
        border-radius: var(--radius-none);
        padding: var(--space-md);
        box-shadow: var(--shadow-subtle);
        border: var(--border-thin) solid var(--line-light);
    }}

    /* ==================== ACCESSIBILITY ==================== */
    button:focus-visible,
    input:focus-visible,
    textarea:focus-visible,
    a:focus-visible {{
        outline: 2px solid var(--black) !important;
        outline-offset: 2px;
    }}

    /* Reduce motion for users who prefer it */
    @media (prefers-reduced-motion: reduce) {{
        *,
        *::before,
        *::after {{
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }}
    }}

    /* High contrast mode support */
    @media (prefers-contrast: high) {{
        :root {{
            --charcoal: #000000;
            --gray-dark: #000000;
        }}

        button,
        input,
        textarea {{
            border-width: 2px !important;
        }}
    }}

    /* ==================== RESPONSIVE ==================== */
    @media (max-width: 768px) {{
        :root {{
            --space-lg: 2rem;
            --space-xl: 2.5rem;
        }}

        .main {{
            padding: var(--space-md) var(--space-sm);
        }}

        .main .block-container {{
            padding: var(--space-md) var(--space-sm);
            max-width: 100%;
        }}

        h1 {{
            font-size: 2rem;
        }}

        h2 {{
            font-size: 1.5rem;
        }}

        h3 {{
            font-size: 1.25rem;
        }}

        .stForm {{
            padding: var(--space-md);
        }}

        div[data-testid="column"] {{
            width: 100% !important;
            margin-bottom: var(--space-sm);
        }}

        div[data-testid="stMetric"] {{
            padding: var(--space-sm);
        }}

        .stChatMessage[data-testid="chat-message-user"] {{
            margin-left: var(--space-sm);
        }}

        .stChatMessage[data-testid="chat-message-assistant"] {{
            margin-right: var(--space-sm);
        }}

        [data-testid="stSidebar"] {{
            min-width: 200px !important;
            max-width: 200px !important;
        }}
    }}

    /* Tablet adjustments */
    @media (min-width: 769px) and (max-width: 1024px) {{
        .main .block-container {{
            max-width: 700px;
        }}
    }}

    /* Large screens - more generous spacing */
    @media (min-width: 1400px) {{
        .main .block-container {{
            max-width: 900px;
        }}
    }}
    </style>
    """


def get_custom_animations_css():
    """CSS pour animations personnalisées (optionnel, à ajouter si besoin)."""
    return """
    <style>
    /* Animations spécifiques aux composants */
    .mood-display {{
        animation: scaleIn 0.3s ease-out;
    }}
    
    .history-card {{
        animation: fadeInUp 0.4s ease-out;
        transition: var(--transition-smooth);
    }}
    
    .history-card:hover {{
        transform: translateX(4px);
        box-shadow: var(--shadow-lg);
    }}
    </style>
    """
