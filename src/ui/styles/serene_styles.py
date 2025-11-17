"""
Styles CSS centralisés pour l'application Serene
Design system cohérent avec palette apaisante pour santé mentale
"""

# Palette de couleurs - Light Theme
COLORS_LIGHT = {
    # Primaires - Tons apaisants vert sauge
    "primary": "#6B9080",
    "primary_light": "#A4C3B2",
    "primary_lighter": "#CCE3DE",
    "primary_dark": "#557568",
    "primary_glow": "rgba(107, 144, 128, 0.15)",

    # Backgrounds
    "bg_primary": "#FAFBFC",
    "bg_secondary": "#FFFFFF",
    "bg_tertiary": "#F7FAFC",
    "bg_elevated": "#FFFFFF",

    # Borders
    "border_primary": "#E2E8F0",
    "border_secondary": "#EDF2F7",
    "border_accent": "#CCE3DE",

    # Texte
    "text_primary": "#1A202C",
    "text_secondary": "#4A5568",
    "text_tertiary": "#718096",
    "text_inverse": "#FFFFFF",

    # Mood colors
    "mood_excellent": "#48BB78",
    "mood_bien": "#6B9080",
    "mood_neutre": "#718096",
    "mood_difficile": "#ED8936",
    "mood_tres_difficile": "#E76F51",

    # Feedback
    "success": "#48BB78",
    "error": "#E76F51",
    "warning": "#ED8936",
    "info": "#4299E1",

    # Ombres
    "shadow_sm": "0 1px 3px rgba(0, 0, 0, 0.06)",
    "shadow_md": "0 4px 16px rgba(0, 0, 0, 0.08)",
    "shadow_lg": "0 12px 32px rgba(0, 0, 0, 0.12)",
    "shadow_xl": "0 20px 48px rgba(0, 0, 0, 0.16)",
}

# Palette de couleurs - Dark Theme
COLORS_DARK = {
    # Primaires - Tons apaisants vert sauge (ajustés pour dark)
    "primary": "#7BA896",
    "primary_light": "#98C4B0",
    "primary_lighter": "#B5D9C9",
    "primary_dark": "#5D8575",
    "primary_glow": "rgba(123, 168, 150, 0.25)",

    # Backgrounds - Dark elevated surfaces
    "bg_primary": "#0F1419",
    "bg_secondary": "#1A1F26",
    "bg_tertiary": "#242A33",
    "bg_elevated": "#2D3440",

    # Borders
    "border_primary": "#2D3440",
    "border_secondary": "#3A4250",
    "border_accent": "#5D8575",

    # Texte
    "text_primary": "#E8EBF0",
    "text_secondary": "#A0AEC0",
    "text_tertiary": "#718096",
    "text_inverse": "#1A202C",

    # Mood colors (brightened for dark theme)
    "mood_excellent": "#5ECFA0",
    "mood_bien": "#7BA896",
    "mood_neutre": "#8A95A5",
    "mood_difficile": "#F59E6C",
    "mood_tres_difficile": "#F08A73",

    # Feedback
    "success": "#5ECFA0",
    "error": "#F08A73",
    "warning": "#F59E6C",
    "info": "#63B3ED",

    # Ombres (plus prononcées pour dark theme)
    "shadow_sm": "0 1px 3px rgba(0, 0, 0, 0.3)",
    "shadow_md": "0 4px 16px rgba(0, 0, 0, 0.4)",
    "shadow_lg": "0 12px 32px rgba(0, 0, 0, 0.5)",
    "shadow_xl": "0 20px 48px rgba(0, 0, 0, 0.6)",
}

# Default to light theme
COLORS = COLORS_LIGHT


def get_theme_colors(theme="light"):
    """Retourne la palette de couleurs pour le thème spécifié."""
    return COLORS_DARK if theme == "dark" else COLORS_LIGHT


def get_main_css(theme="light"):
    """Retourne le CSS principal de l'application avec support du thème."""
    colors = get_theme_colors(theme)

    return f"""
    <style>
    /* ==================== ROOT VARIABLES - THEME DYNAMIC ==================== */
    :root {{
        /* Colors */
        --color-primary: {colors['primary']};
        --color-primary-light: {colors['primary_light']};
        --color-primary-lighter: {colors['primary_lighter']};
        --color-primary-dark: {colors['primary_dark']};
        --color-primary-glow: {colors['primary_glow']};

        /* Backgrounds */
        --bg-primary: {colors['bg_primary']};
        --bg-secondary: {colors['bg_secondary']};
        --bg-tertiary: {colors['bg_tertiary']};
        --bg-elevated: {colors['bg_elevated']};

        /* Borders */
        --border-primary: {colors['border_primary']};
        --border-secondary: {colors['border_secondary']};
        --border-accent: {colors['border_accent']};

        /* Text */
        --text-primary: {colors['text_primary']};
        --text-secondary: {colors['text_secondary']};
        --text-tertiary: {colors['text_tertiary']};
        --text-inverse: {colors['text_inverse']};

        /* Feedback */
        --color-success: {colors['success']};
        --color-error: {colors['error']};
        --color-warning: {colors['warning']};
        --color-info: {colors['info']};

        /* Shadows */
        --shadow-sm: {colors['shadow_sm']};
        --shadow-md: {colors['shadow_md']};
        --shadow-lg: {colors['shadow_lg']};
        --shadow-xl: {colors['shadow_xl']};

        /* Radius */
        --radius-sm: 8px;
        --radius-md: 14px;
        --radius-lg: 18px;
        --radius-xl: 24px;

        /* Transitions */
        --transition-smooth: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        --transition-fast: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
        --transition-bounce: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
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
    * {{
        transition: background-color 0.3s ease, border-color 0.3s ease, color 0.3s ease;
    }}

    .main {{
        background-color: var(--bg-primary);
        padding: 2rem 3rem;
    }}

    .main .block-container {{
        padding-top: 2rem;
        max-width: 1000px;
    }}

    /* Réduire l'espacement entre éléments */
    .element-container {{
        margin-bottom: 0.75rem;
    }}

    /* Smooth scroll */
    html {{
        scroll-behavior: smooth;
    }}

    body {{
        background-color: var(--bg-primary);
    }}
    
    /* ==================== SIDEBAR - MODERN DESIGN ==================== */
    [data-testid="stSidebar"] {{
        background: var(--bg-secondary);
        padding: 1.5rem 1rem;
        min-width: 280px !important;
        border-right: 1px solid var(--border-primary);
        backdrop-filter: blur(20px);
    }}

    [data-testid="stSidebar"]::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 200px;
        background: linear-gradient(180deg, var(--color-primary-glow) 0%, transparent 100%);
        pointer-events: none;
        z-index: 0;
    }}

    [data-testid="stSidebar"] > div {{
        position: relative;
        z-index: 1;
    }}

    [data-testid="stSidebar"] h1 {{
        font-size: 1.75rem;
        color: var(--color-primary);
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-align: center;
    }}

    /* Navigation radio buttons - Modern cards */
    [data-testid="stSidebar"] .stRadio > div {{
        gap: 0.5rem;
    }}

    [data-testid="stSidebar"] .stRadio label {{
        background: var(--bg-tertiary);
        padding: 1rem 1.25rem;
        border-radius: var(--radius-md);
        transition: var(--transition-smooth);
        border: 1px solid var(--border-primary);
        cursor: pointer;
        font-weight: 500;
        color: var(--text-secondary);
        position: relative;
        overflow: hidden;
    }}

    [data-testid="stSidebar"] .stRadio label::before {{
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 3px;
        background: var(--color-primary);
        transform: scaleY(0);
        transition: transform 0.3s ease;
    }}

    [data-testid="stSidebar"] .stRadio label:hover {{
        background: var(--bg-elevated);
        border-color: var(--border-accent);
        transform: translateX(4px);
        box-shadow: var(--shadow-sm);
    }}

    [data-testid="stSidebar"] .stRadio label:has(input:checked) {{
        background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
        border-color: var(--color-primary);
        color: var(--text-inverse);
        box-shadow: var(--shadow-md), 0 0 20px var(--color-primary-glow);
    }}

    [data-testid="stSidebar"] .stRadio label:has(input:checked)::before {{
        transform: scaleY(1);
    }}
    
    /* ==================== TYPOGRAPHY - ENHANCED ==================== */
    h1, h2, h3 {{
        color: var(--text-primary);
        font-weight: 700;
        line-height: 1.2;
        letter-spacing: -0.02em;
    }}

    h1 {{
        font-size: 2.25rem;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-light) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}

    h2 {{
        font-size: 1.75rem;
        margin: 2.5rem 0 1.25rem 0;
        color: var(--text-primary);
    }}

    h3 {{
        font-size: 1.25rem;
        margin: 2rem 0 1rem 0;
        font-weight: 600;
        color: var(--text-primary);
    }}

    h4 {{
        font-size: 1.1rem;
        margin: 1.5rem 0 0.75rem 0;
        font-weight: 600;
        color: var(--text-primary);
    }}

    p {{
        color: var(--text-secondary);
        line-height: 1.7;
        font-size: 1rem;
    }}

    /* Enhanced text */
    .text-gradient {{
        background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-light) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    }}
    
    /* ==================== FORMS ==================== */
    
    /* Form container - Modern glassmorphism */
    .stForm {{
        background: var(--bg-elevated);
        padding: 2.5rem;
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-lg);
        margin: 2rem 0;
        border: 1px solid var(--border-primary);
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }}

    .stForm::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--color-primary) 0%, var(--color-primary-light) 100%);
    }}
    
    /* Slider */
    .stSlider {{
        padding: 1rem 0 0.5rem 0;
    }}

    .stSlider > label {{
        font-weight: 600 !important;
        color: var(--text-primary) !important;
        font-size: 1.05rem !important;
    }}

    .stSlider [data-baseweb="slider"] {{
        margin-top: 1rem;
    }}

    .stSlider [role="slider"] {{
        background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-light) 100%) !important;
        width: 24px !important;
        height: 24px !important;
        box-shadow: var(--shadow-md), 0 0 0 4px var(--color-primary-glow);
        border: 3px solid var(--bg-elevated);
        cursor: grab;
    }}

    .stSlider [role="slider"]:hover {{
        box-shadow: var(--shadow-lg), 0 0 0 6px var(--color-primary-glow);
        transform: scale(1.1);
    }}

    .stSlider [role="slider"]:active {{
        cursor: grabbing;
        transform: scale(0.95);
    }}

    /* Barre du slider - with gradient track */
    .stSlider [data-baseweb="slider"] > div:first-child {{
        background: linear-gradient(90deg,
            var(--color-error) 0%,
            var(--color-warning) 40%,
            var(--color-primary) 70%,
            var(--color-success) 100%) !important;
        height: 6px !important;
        border-radius: 3px;
    }}


    [data-testid="stSliderThumbValue"], [data-testid="stSliderTickBar"] {{
        font-size: 2.00rem !important;  /* Taille de base augmentée de 50% */
        font-weight: 500 !important;
        color: var(--color-text-dark) !important;
    }}

    

    /* Text Area - Modern design */
    .stTextArea > label {{
        font-weight: 600 !important;
        color: var(--text-primary) !important;
        margin-bottom: 0.75rem;
        font-size: 1.05rem !important;
    }}

    .stTextArea textarea {{
        border-radius: var(--radius-md) !important;
        border: 2px solid var(--border-primary) !important;
        padding: 1rem 1.25rem !important;
        font-size: 1rem !important;
        transition: var(--transition-smooth);
        background-color: var(--bg-tertiary);
        color: var(--text-primary);
        line-height: 1.6 !important;
    }}

    .stTextArea textarea:focus {{
        border-color: var(--color-primary) !important;
        box-shadow: 0 0 0 4px var(--color-primary-glow), var(--shadow-md) !important;
        outline: none !important;
        background-color: var(--bg-elevated);
    }}

    .stTextArea textarea::placeholder {{
        color: var(--text-tertiary);
        opacity: 0.7;
    }}
    
    /* Submit Button - Premium design */
    .stForm button[kind="primary"] {{
        background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%) !important;
        color: var(--text-inverse) !important;
        border: none !important;
        padding: 1rem 2.5rem !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        border-radius: var(--radius-md) !important;
        transition: var(--transition-smooth) !important;
        box-shadow: var(--shadow-md), 0 4px 20px var(--color-primary-glow);
        width: 100%;
        position: relative;
        overflow: hidden;
    }}

    .stForm button[kind="primary"]::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s ease;
    }}

    .stForm button[kind="primary"]:hover {{
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg), 0 8px 30px var(--color-primary-glow);
    }}

    .stForm button[kind="primary"]:hover::before {{
        left: 100%;
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

    /* Statistical cards - Modern glassmorphism */
    .stat-card {{
        background: var(--bg-elevated);
        padding: 2rem;
        border-radius: var(--radius-lg);
        text-align: center;
        box-shadow: var(--shadow-md);
        transition: var(--transition-smooth);
        border: 1px solid var(--border-primary);
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }}

    .stat-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--color-primary) 0%, var(--color-primary-light) 100%);
    }}

    .stat-card:hover {{
        transform: translateY(-4px);
        box-shadow: var(--shadow-xl);
        border-color: var(--border-accent);
    }}

    /* Feature cards - Premium design */
    .feature-card {{
        background: var(--bg-elevated);
        padding: 2.5rem;
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-md);
        transition: var(--transition-smooth);
        border: 1px solid var(--border-primary);
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }}

    .feature-card::after {{
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, var(--color-primary-glow) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.5s ease;
        pointer-events: none;
    }}

    .feature-card:hover {{
        transform: translateY(-6px);
        box-shadow: var(--shadow-xl);
        border-color: var(--color-primary);
    }}

    .feature-card:hover::after {{
        opacity: 1;
    }}

    /* Call-to-action cards - Enhanced gradient */
    .cta-card {{
        background: linear-gradient(135deg, var(--bg-elevated) 0%, var(--bg-tertiary) 100%);
        padding: 3rem 2rem;
        border-radius: var(--radius-xl);
        text-align: center;
        border: 2px solid var(--border-accent);
        box-shadow: var(--shadow-lg), 0 0 40px var(--color-primary-glow);
        transition: var(--transition-smooth);
        position: relative;
        overflow: hidden;
    }}

    .cta-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(107, 144, 128, 0.1), transparent);
        transition: left 0.6s ease;
    }}

    .cta-card:hover {{
        transform: scale(1.02);
        box-shadow: var(--shadow-xl), 0 0 60px var(--color-primary-glow);
    }}

    .cta-card:hover::before {{
        left: 100%;
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
