"""
Styles CSS centralisés pour l'application Serene
Design system cohérent avec palette apaisante pour santé mentale
"""

# Palette de couleurs unifiée
COLORS = {
    # Primaires - Tons apaisants vert sauge
    "primary": "#6B9080",
    "primary_light": "#A4C3B2",
    "primary_lighter": "#CCE3DE",
    "primary_dark": "#557568",
    
    # Neutres
    "neutral_bg": "#F7FAFC",
    "neutral_light": "#EDF2F7",
    "white": "#FFFFFF",
    
    # Texte
    "text_dark": "#2D3748",
    "text_medium": "#4A5568",
    "text_light": "#718096",
    
    # Mood colors (gradient subtil)
    "mood_excellent": "#48BB78",  # Vert
    "mood_bien": "#6B9080",       # Vert sauge (primary)
    "mood_neutre": "#718096",     # Gris
    "mood_difficile": "#ED8936",  # Orange doux
    "mood_tres_difficile": "#E76F51",  # Rouge terre cuite
    
    # Feedback
    "success": "#48BB78",
    "error": "#E76F51",
    "warning": "#ED8936",
    
    # Ombres
    "shadow_sm": "0 1px 3px rgba(0, 0, 0, 0.04)",
    "shadow_md": "0 4px 12px rgba(107, 144, 128, 0.08)",
    "shadow_lg": "0 8px 24px rgba(107, 144, 128, 0.12)",
}


def get_main_css():
    """Retourne le CSS principal de l'application."""
    return f"""
    <style>
    /* ==================== ROOT VARIABLES ==================== */
    :root {{
        --color-primary: {COLORS['primary']};
        --color-primary-light: {COLORS['primary_light']};
        --color-primary-lighter: {COLORS['primary_lighter']};
        --color-primary-dark: {COLORS['primary_dark']};
        --color-neutral-bg: {COLORS['neutral_bg']};
        --color-neutral-light: {COLORS['neutral_light']};
        --color-white: {COLORS['white']};
        --color-text-dark: {COLORS['text_dark']};
        --color-text-medium: {COLORS['text_medium']};
        --color-text-light: {COLORS['text_light']};
        --color-success: {COLORS['success']};
        --color-error: {COLORS['error']};
        --shadow-sm: {COLORS['shadow_sm']};
        --shadow-md: {COLORS['shadow_md']};
        --shadow-lg: {COLORS['shadow_lg']};
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
        --transition-smooth: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    /* ==================== ANIMATIONS SUBTILES ==================== */
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    
    @keyframes fadeInUp {{
        from {{
            opacity: 0;
            transform: translateY(20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    @keyframes fadeInDown {{
        from {{
            opacity: 0;
            transform: translateY(-10px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    @keyframes scaleIn {{
        from {{
            opacity: 0;
            transform: scale(0.95);
        }}
        to {{
            opacity: 1;
            transform: scale(1);
        }}
    }}
    
    /* Animation bounce simplifiée (moins aggressive) */
    @keyframes gentleBounce {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-5px); }}
    }}
    
    /* ==================== GLOBAL STYLES ==================== */
    .main {{
        background-color: var(--color-neutral-bg);
        padding: 2rem 3rem;
    }}
    
    .main .block-container {{
        padding-top: 2rem;
        max-width: 900px;
    }}
    
    /* Réduire l'espacement entre éléments */
    .element-container {{
        margin-bottom: 0.75rem;
    }}
    
    /* ==================== SIDEBAR ==================== */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, var(--color-white) 0%, var(--color-neutral-bg) 100%);
        padding: 2rem 1.5rem;
        min-width: 280px !important;
    }}
    
    [data-testid="stSidebar"] h1 {{
        font-size: 1.75rem;
        color: var(--color-primary);
        font-weight: 600;
        margin-bottom: 0.5rem;
        text-align: center;
    }}
    
    /* Navigation radio buttons */
    [data-testid="stSidebar"] .stRadio > div {{
        gap: 0.5rem;
    }}
    
    [data-testid="stSidebar"] .stRadio label {{
        background-color: transparent;
        padding: 0.875rem 1rem;
        border-radius: var(--radius-md);
        transition: var(--transition-smooth);
        border: 1px solid transparent;
        cursor: pointer;
    }}
    
    [data-testid="stSidebar"] .stRadio label:hover {{
        background-color: var(--color-primary-lighter);
        border-color: var(--color-primary-light);
    }}
    
    /* ==================== TYPOGRAPHY ==================== */
    h1, h2, h3 {{
        color: var(--color-text-dark);
        font-weight: 600;
        line-height: 1.3;
    }}
    
    h1 {{
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }}
    
    h2 {{
        font-size: 1.5rem;
        margin: 2rem 0 1rem 0;
    }}
    
    h3 {{
        font-size: 1.25rem;
        margin: 1.5rem 0 0.75rem 0;
    }}
    
    p {{
        color: var(--color-text-medium);
        line-height: 1.6;
    }}
    
    /* ==================== FORMS ==================== */
    
    /* Form container */
    .stForm {{
        background-color: var(--color-white);
        padding: 2rem;
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-md);
        margin: 1.5rem 0;
        border: 1px solid var(--color-neutral-light);
    }}
    
    /* Slider */
    .stSlider {{
        padding: 1rem 0 0.5rem 0;
    }}
    
    .stSlider > label {{
        font-weight: 500 !important;
        color: var(--color-text-dark) !important;
        font-size: 1rem !important;
    }}
    
    .stSlider [data-baseweb="slider"] {{
        margin-top: 0.5rem;
    }}
    
    .stSlider [role="slider"] {{
        background-color: var(--color-primary) !important;
        width: 22px !important;
        height: 22px !important;
        box-shadow: var(--shadow-sm);
        border: 2px solid var(--color-white);
    }}
    
    .stSlider [role="slider"]:hover {{
        box-shadow: 0 0 0 4px rgba(107, 144, 128, 0.15);
    }}
    
    /* Barre du slider */
    .stSlider [data-baseweb="slider"] > div:first-child {{
        background-color: var(--color-primary-light) !important;
    }}
    
    /* Text Area */
    .stTextArea > label {{
        font-weight: 500 !important;
        color: var(--color-text-dark) !important;
        margin-bottom: 0.5rem;
    }}
    
    .stTextArea textarea {{
        border-radius: var(--radius-md) !important;
        border: 2px solid var(--color-neutral-light) !important;
        padding: 0.875rem !important;
        font-size: 0.95rem !important;
        transition: var(--transition-smooth);
        background-color: var(--color-white);
        line-height: 1.5 !important;
    }}
    
    .stTextArea textarea:focus {{
        border-color: var(--color-primary) !important;
        box-shadow: 0 0 0 3px rgba(107, 144, 128, 0.1) !important;
        outline: none !important;
    }}
    
    /* Submit Button */
    .stForm button[kind="primary"] {{
        background-color: var(--color-primary) !important;
        color: white !important;
        border: none !important;
        padding: 0.875rem 2rem !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        border-radius: var(--radius-md) !important;
        transition: var(--transition-smooth) !important;
        box-shadow: var(--shadow-sm);
        width: 100%;
    }}
    
    .stForm button[kind="primary"]:hover {{
        background-color: var(--color-primary-dark) !important;
        box-shadow: var(--shadow-md);
        transform: translateY(-1px);
    }}
    
    .stForm button[kind="primary"]:active {{
        transform: translateY(0);
    }}
    
    /* ==================== DIVIDER ==================== */
    hr {{
        margin: 2.5rem 0;
        border: none;
        border-top: 2px solid var(--color-neutral-light);
        opacity: 0.6;
    }}
    
    /* ==================== SUCCESS/ERROR MESSAGES ==================== */
    .stSuccess {{
        background-color: rgba(72, 187, 120, 0.1) !important;
        border-left: 4px solid var(--color-success) !important;
        padding: 1rem !important;
        border-radius: var(--radius-md) !important;
        animation: fadeInDown 0.3s ease-out;
    }}
    
    .stSuccess p {{
        color: var(--color-text-dark) !important;
        font-weight: 500;
    }}
    
    .stError {{
        background-color: rgba(231, 111, 81, 0.1) !important;
        border-left: 4px solid var(--color-error) !important;
        padding: 1rem !important;
        border-radius: var(--radius-md) !important;
    }}
    
    /* ==================== RESPONSIVE ==================== */
    @media (max-width: 768px) {{
        .main {{
            padding: 1rem;
        }}
        
        .main .block-container {{
            padding-top: 1rem;
        }}
        
        h1 {{
            font-size: 1.5rem;
        }}
        
        .stForm {{
            padding: 1.5rem;
        }}
    }}
    
    /* ==================== SCROLLBAR ==================== */
    ::-webkit-scrollbar {{
        width: 10px;
        height: 10px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: var(--color-neutral-bg);
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: var(--color-primary-light);
        border-radius: 5px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: var(--color-primary);
    }}

    /* ==================== CHAT MESSAGES ==================== */
    .stChatMessage {{
        border-radius: var(--radius-md);
        padding: 1rem;
        margin-bottom: 0.75rem;
        box-shadow: var(--shadow-sm);
        animation: fadeInUp 0.3s ease-out;
    }}

    .stChatMessage[data-testid="chat-message-user"] {{
        background-color: var(--color-primary) !important;
        color: white !important;
        margin-left: 2rem;
    }}

    .stChatMessage[data-testid="chat-message-assistant"] {{
        background-color: var(--color-white) !important;
        color: var(--color-text-dark) !important;
        margin-right: 2rem;
        border: 1px solid var(--color-neutral-light);
    }}

    /* ==================== EXPANDER ==================== */
    .streamlit-expanderHeader {{
        background-color: var(--color-white);
        border-radius: var(--radius-md);
        padding: 0.875rem 1rem;
        font-weight: 500;
        transition: var(--transition-smooth);
        border: 1px solid var(--color-neutral-light);
    }}

    .streamlit-expanderHeader:hover {{
        background-color: var(--color-primary-lighter);
        border-color: var(--color-primary-light);
    }}

    /* ==================== METRICS ==================== */
    div[data-testid="stMetric"] {{
        background-color: var(--color-white);
        padding: 1.5rem;
        border-radius: var(--radius-md);
        box-shadow: var(--shadow-sm);
        transition: var(--transition-smooth);
        border: 1px solid var(--color-neutral-light);
    }}

    div[data-testid="stMetric"]:hover {{
        box-shadow: var(--shadow-md);
        transform: translateY(-2px);
    }}

    div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
        font-size: 2.25rem !important;
        font-weight: 600 !important;
        color: var(--color-primary);
    }}

    /* ==================== PLOTS & CHARTS ==================== */
    div[data-testid="stPlotlyChart"] {{
        background-color: var(--color-white);
        border-radius: var(--radius-md);
        padding: 1.5rem;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--color-neutral-light);
    }}

    /* ==================== ANIMATIONS SUPPLÉMENTAIRES ==================== */
    @keyframes shimmer {{
        0% {{ background-position: -1000px 0; }}
        100% {{ background-position: 1000px 0; }}
    }}

    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.7; }}
    }}

    @keyframes bounce {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-5px); }}
    }}

    /* ==================== ACCESSIBILITY ==================== */
    button:focus-visible,
    input:focus-visible,
    textarea:focus-visible,
    a:focus-visible {{
        outline: 3px solid var(--color-primary) !important;
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
            --color-primary: {COLORS['primary_dark']};
            --color-text-medium: #2D3748;
        }}

        button,
        input,
        textarea {{
            border-width: 2px !important;
        }}
    }}

    /* ==================== UTILITY CLASSES ==================== */

    /* Glassmorphism effect */
    .glass {{
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }}

    /* ==================== CARD COMPONENTS ==================== */

    /* Statistical cards for dashboard metrics */
    .stat-card {{
        background-color: #F7FAFC;
        padding: 1.5rem;
        border-radius: var(--radius-md);
        text-align: center;
        box-shadow: 0 1px 3px rgba(107, 70, 193, 0.1);
        transition: var(--transition-smooth);
    }}

    .stat-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(107, 70, 193, 0.12);
    }}

    /* Feature cards for home page */
    .feature-card {{
        background-color: #F7FAFC;
        padding: 2rem;
        border-radius: var(--radius-md);
        box-shadow: 0 1px 3px rgba(107, 70, 193, 0.1);
        transition: var(--transition-smooth);
    }}

    .feature-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(107, 70, 193, 0.15);
    }}

    /* Call-to-action cards */
    .cta-card {{
        background: linear-gradient(135deg, #EBF4FF 0%, #F7FAFC 100%);
        padding: 2rem;
        border-radius: var(--radius-lg);
        text-align: center;
        border-left: 4px solid var(--color-primary);
        box-shadow: 0 4px 12px rgba(107, 70, 193, 0.1);
        transition: var(--transition-smooth);
    }}

    .cta-card:hover {{
        transform: scale(1.02);
        box-shadow: 0 8px 24px rgba(107, 70, 193, 0.15);
    }}

    /* Gradient text */
    .gradient-text {{
        background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-light) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}

    /* Interactive card hover effect */
    .interactive-card {{
        transition: var(--transition-smooth);
        cursor: pointer;
    }}

    .interactive-card:hover {{
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
    }}

    .interactive-card:active {{
        transform: translateY(-2px);
    }}

    /* Status indicators */
    .status-dot {{
        width: 8px;
        height: 8px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 0.25rem;
    }}

    .status-dot.success {{
        background-color: var(--color-success);
        animation: pulse 2s infinite;
    }}

    .status-dot.warning {{
        background-color: {COLORS['warning']};
    }}

    .status-dot.error {{
        background-color: var(--color-error);
        animation: pulse 2s infinite;
    }}

    /* Loading skeleton */
    .skeleton {{
        background: linear-gradient(
            90deg,
            var(--color-neutral-light) 0%,
            var(--color-neutral-bg) 50%,
            var(--color-neutral-light) 100%
        );
        background-size: 1000px 100%;
        animation: shimmer 2s infinite linear;
        border-radius: var(--radius-md);
    }}

    /* ==================== RESPONSIVE MOBILE ==================== */
    @media (max-width: 768px) {{
        /* Stack columns on mobile */
        div[data-testid="column"] {{
            width: 100% !important;
            margin-bottom: 1rem;
        }}

        /* Reduce padding on cards */
        div[data-testid="stMetric"] {{
            padding: 1rem;
        }}

        .stForm {{
            padding: 1.5rem;
        }}

        /* Chat messages - reduce margins */
        .stChatMessage[data-testid="chat-message-user"] {{
            margin-left: 0.5rem;
        }}

        .stChatMessage[data-testid="chat-message-assistant"] {{
            margin-right: 0.5rem;
        }}
    }}

    /* Tablet adjustments */
    @media (min-width: 769px) and (max-width: 1024px) {{
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
