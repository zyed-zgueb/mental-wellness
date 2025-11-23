"""Composant UI pour le dashboard avec visualisations et insights IA - Gallery Minimalist Style"""

import streamlit as st
import plotly.express as px
import pandas as pd
import re
from datetime import datetime, timedelta
from src.database.db_manager import DatabaseManager
from src.ui.auth import get_current_user_id
from src.llm.insights_generator import InsightsGenerator
from src.ui.styles.serene_styles import (
    create_page_header,
    create_section_header,
    create_metric_card_large,
    create_metric_card_small,
    create_empty_state,
    create_divider,
    create_insight_content
)


def remove_emojis(text: str) -> str:
    """
    Supprime tous les emojis d'un texte pour un style épuré.

    Args:
        text: Le texte à nettoyer

    Returns:
        Le texte sans emojis
    """
    # Pattern pour détecter les emojis
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001F900-\U0001F9FF"  # supplemental symbols
        u"\U00002600-\U000026FF"  # misc symbols
        "]+", flags=re.UNICODE
    )
    return emoji_pattern.sub('', text).strip()


def strip_html_tags(text: str) -> str:
    """
    Supprime les balises HTML brutes du texte généré par l'IA.

    Cette fonction nettoie le HTML que l'IA pourrait générer malgré les instructions,
    en le convertissant en texte brut avant la conversion markdown.

    Args:
        text: Le texte potentiellement avec des balises HTML

    Returns:
        Le texte sans balises HTML
    """
    # Supprimer les balises HTML avec attributs style (ex: <div style="...">)
    text = re.sub(r'<(\w+)[^>]*style\s*=\s*["\'][^"\']*["\'][^>]*>', '', text)

    # Supprimer les balises HTML fermantes
    text = re.sub(r'</(\w+)>', '', text)

    # Supprimer les balises HTML simples restantes (ex: <div>, <p>)
    text = re.sub(r'<(\w+)[^>]*>', '', text)

    return text.strip()


def convert_markdown_to_html(text: str) -> str:
    """
    Convertit les marqueurs markdown en HTML pour un rendu correct.

    Args:
        text: Le texte markdown à convertir

    Returns:
        Le texte avec les marqueurs markdown convertis en HTML
    """
    # Convertir les titres H2 (##)
    text = re.sub(
        r'^## (.+)$',
        r"<h2 style='font-family: \"Cormorant Garamond\", serif; font-size: 1.5rem; font-weight: 400; color: var(--black); margin-bottom: 1rem; letter-spacing: 0.02em;'>\1</h2>",
        text,
        flags=re.MULTILINE
    )

    # Convertir les titres H3 (###)
    text = re.sub(
        r'^### (.+)$',
        r"<h3 style='font-family: \"Cormorant Garamond\", serif; font-size: 1.25rem; font-weight: 400; color: var(--black); margin: 1rem 0 0.75rem 0; letter-spacing: 0.02em;'>\1</h3>",
        text,
        flags=re.MULTILINE
    )

    # Convertir le texte en gras (**text**) - AVANT l'italique pour éviter les conflits
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)

    # Convertir le texte en italique (*text* ou _text_)
    # Gérer les cas avec espaces avant la fermeture (ex: "texte *")
    text = re.sub(r'\*([^*]+?)\s*\*', r'<em>\1</em>', text)
    text = re.sub(r'_([^_]+?)_', r'<em>\1</em>', text)

    # Convertir les listes numérotées (1. item, 2. item, etc.)
    text = re.sub(r'^\d+\.\s+(.+)$', r'<li-num style="margin-bottom: 0.75rem;">\1</li-num>', text, flags=re.MULTILINE)

    # Envelopper les groupes de <li-num> dans <ol>
    text = re.sub(
        r'(<li-num[^>]*>.*?</li-num>(?:\s*<li-num[^>]*>.*?</li-num>)*)',
        r'<ol style="margin: 1rem 0; padding-left: 1.5rem; line-height: 1.8;">\1</ol>',
        text,
        flags=re.DOTALL
    )

    # Remplacer <li-num> par <li>
    text = text.replace('<li-num', '<li').replace('</li-num>', '</li>')

    # Convertir les listes à puces (- item)
    text = re.sub(r'^- (.+)$', r'<li-bullet style="margin-bottom: 0.5rem;">\1</li-bullet>', text, flags=re.MULTILINE)

    # Envelopper les groupes de <li-bullet> dans <ul>
    text = re.sub(
        r'(<li-bullet[^>]*>.*?</li-bullet>(?:\s*<li-bullet[^>]*>.*?</li-bullet>)*)',
        r'<ul style="margin: 1rem 0; padding-left: 1.5rem;">\1</ul>',
        text,
        flags=re.DOTALL
    )

    # Remplacer <li-bullet> par <li>
    text = text.replace('<li-bullet', '<li').replace('</li-bullet>', '</li>')

    # Convertir les sauts de ligne en <br> pour les paragraphes
    text = text.replace('\n\n', '<br/><br/>')

    return text


@st.cache_resource
def get_database():
    """
    Singleton DatabaseManager pour toute l'application.

    Returns:
        Instance unique de DatabaseManager.
    """
    return DatabaseManager("serene.db")


def get_insights_generator(user_id: int):
    """
    Get InsightsGenerator for a specific user.

    Args:
        user_id: ID de l'utilisateur.

    Returns:
        Instance de InsightsGenerator pour cet utilisateur.
    """
    db = get_database()
    return InsightsGenerator(db, user_id)


def show_dashboard():
    """Afficher le dashboard - Gallery minimalist style."""

    # Header minimaliste
    st.markdown(
        create_page_header(
            "Dashboard",
            "Visualisez vos tendances de bien-être et recevez des insights personnalisés."
        ),
        unsafe_allow_html=True
    )

    db = get_database()

    # Section 1: Grande métrique centrale - Style minimaliste
    st.markdown(
        create_section_header("fa-regular fa-heart", "Votre Bien-être"),
        unsafe_allow_html=True
    )

    # Sélecteur de période avec style élégant
    period_options = {
        "Aujourd'hui": 1,
        "7 jours": 7,
        "30 jours": 30,
        "90 jours": 90
    }

    selected_period_label = st.radio(
        "Sélectionner la période de référence",
        options=list(period_options.keys()),
        index=2,  # 30 jours par défaut
        key="mood_period_selector",
        horizontal=True,
        label_visibility="hidden"
    )

    selected_days = period_options[selected_period_label]

    user_id = get_current_user_id()
    mood_data = db.get_mood_history(user_id, days=selected_days)

    if mood_data and len(mood_data) > 0:
        # Convertir en DataFrame pour Plotly
        df_mood = pd.DataFrame(mood_data)
        df_mood['timestamp'] = pd.to_datetime(df_mood['timestamp'])

        # Calculer statistiques pour grande métrique centrale
        avg_mood = df_mood['mood_score'].mean()
        latest_mood = df_mood.iloc[0]['mood_score']
        min_mood = df_mood['mood_score'].min()
        max_mood = df_mood['mood_score'].max()

        # Calculer le delta (comparaison avec la moyenne)
        delta = latest_mood - avg_mood

        # Grande métrique centrale - Style minimaliste
        st.markdown(
            create_metric_card_large(
                label="Score Actuel",
                value=f"{latest_mood:.1f}",
                unit="sur 10",
                delta=delta
            ),
            unsafe_allow_html=True
        )

        # Stats secondaires - Style minimaliste
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                create_metric_card_small(
                    label=f"Moyenne ({selected_period_label})",
                    value=f"{avg_mood:.1f}",
                    unit="sur 10",
                    animation_delay="0.5s"
                ),
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                create_metric_card_small(
                    label=f"Minimum ({selected_period_label})",
                    value=f"{min_mood}",
                    unit="sur 10",
                    animation_delay="0.6s"
                ),
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                create_metric_card_small(
                    label=f"Maximum ({selected_period_label})",
                    value=f"{max_mood}",
                    unit="sur 10",
                    animation_delay="0.7s"
                ),
                unsafe_allow_html=True
            )

        st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

        # Graphique minimaliste monochrome
        st.markdown(f"""
        <h3 style='font-family: "Cormorant Garamond", serif; font-size: 1.5rem;
                   font-weight: 400; color: var(--black); margin: var(--space-md) 0 var(--space-sm) 0;
                   letter-spacing: 0.02em;'>
            Tendance ({selected_period_label})
        </h3>
        """, unsafe_allow_html=True)

        # Graphique avec échelle de gris
        fig_mood = px.scatter(
            df_mood,
            x='timestamp',
            y='mood_score',
            color='mood_score',
            color_continuous_scale=[
                (0.0, '#4A4A4A'),   # Gris foncé pour valeurs basses
                (0.5, '#6B6B6B'),   # Gris moyen
                (1.0, '#2A2A2A')    # Quasi-noir pour valeurs hautes
            ],
            range_color=[0, 10]
        )

        # Style minimaliste - points géométriques
        fig_mood.update_traces(
            mode='markers',
            marker=dict(size=10, line=dict(color='#FAF8F3', width=1), opacity=0.9),
            hovertemplate='<b>%{x|%d/%m/%Y à %H:%M}</b><br>Score: %{y}/10<extra></extra>'
        )

        fig_mood.update_layout(
            hovermode='x unified',
            xaxis_title="",
            yaxis_title="Score",
            yaxis=dict(
                range=[0, 11],
                gridcolor='#E0E0E0',
                gridwidth=0.5,
                tickfont=dict(family='Inter', size=10, color='#6B6B6B')
            ),
            xaxis=dict(
                gridcolor='#E0E0E0',
                gridwidth=0.5,
                tickfont=dict(family='Inter', size=10, color='#6B6B6B')
            ),
            height=350,
            plot_bgcolor='#FAF8F3',
            paper_bgcolor='#FAF8F3',
            font=dict(family="Inter", color='#1A1A1A', size=12),
            margin=dict(l=40, r=20, t=20, b=40),
            coloraxis_showscale=False  # Masquer la barre de couleur
        )

        st.plotly_chart(fig_mood, use_container_width=True)

    else:
        # État vide minimaliste
        st.markdown(
            create_empty_state(
                "Commencez votre suivi",
                "Créez votre premier check-in pour visualiser vos tendances de bien-être"
            ),
            unsafe_allow_html=True
        )

    # Divider minimaliste
    st.markdown(create_divider(), unsafe_allow_html=True)

    # Section 2: Activité Conversations
    st.markdown(
        create_section_header("fa-regular fa-message", "Activité Conversations"),
        unsafe_allow_html=True
    )

    user_id = get_current_user_id()
    conv_history = db.get_conversation_history(user_id, limit=100)

    if conv_history and len(conv_history) > 0:
        # Statistiques conversations - Cards compactes
        total_conv = len(conv_history)

        # Grouper par jour
        df_conv = pd.DataFrame(conv_history)
        df_conv['timestamp'] = pd.to_datetime(df_conv['timestamp'])
        df_conv['date'] = df_conv['timestamp'].dt.date

        # Compter conversations par jour
        conv_per_day = df_conv.groupby('date').size().reset_index(name='count')
        days_with_conv = len(conv_per_day)
        avg_per_day = total_conv / days_with_conv if days_with_conv > 0 else 0

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                create_metric_card_small(
                    label="Total",
                    value=f"{total_conv}",
                    unit="conversations"
                ),
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                create_metric_card_small(
                    label="Moyenne",
                    value=f"{avg_per_day:.1f}",
                    unit="par jour"
                ),
                unsafe_allow_html=True
            )

    else:
        # État vide minimaliste
        st.markdown(
            create_empty_state(
                "Démarrez votre première conversation",
                "Partagez vos pensées avec votre compagnon IA empathique"
            ),
            unsafe_allow_html=True
        )

    # Divider minimaliste
    st.markdown(create_divider(), unsafe_allow_html=True)

    # Section 3: AI Insights
    st.markdown(
        create_section_header(
            "fa-solid fa-sparkles",
            "Vos Insights Personnalisés",
            "Découvrez des révélations actionnables sur votre bien-être mental"
        ),
        unsafe_allow_html=True
    )

    # Vérifier si des données existent (au moins 1 check-in ou 1 conversation)
    checkin_count = len(mood_data) if mood_data else 0
    conv_count = len(conv_history) if conv_history else 0

    if checkin_count > 0 or conv_count > 0:
        # Créer un conteneur pour tout le contenu de l'insight
        insight_container = st.container()

        with insight_container:
            # Loading skeleton pendant la génération
            loading_placeholder = st.empty()
            with loading_placeholder.container():
                # Afficher le conteneur avec skeleton
                st.markdown("""
                <div style='background-color: var(--white); padding: 2rem;
                            border: 1px solid var(--line-light); border-left: 2px solid var(--black);
                            box-shadow: var(--shadow-subtle); margin-bottom: 1rem;
                            animation: fadeInUp 0.5s ease-out;'>
                    <div style='margin-bottom: 1rem;'>
                        <div class='skeleton' style='height: 1.5rem; width: 70%; margin-bottom: 1rem;'></div>
                        <div class='skeleton' style='height: 1rem; width: 100%; margin-bottom: 0.5rem;'></div>
                        <div class='skeleton' style='height: 1rem; width: 95%; margin-bottom: 0.5rem;'></div>
                        <div class='skeleton' style='height: 1rem; width: 85%;'></div>
                    </div>
                    <p style='color: var(--color-primary); font-size: 0.9rem; text-align: center; margin-top: 1.5rem;'>
                        Génération de vos insights personnalisés...
                    </p>
                </div>
                """, unsafe_allow_html=True)

            # Générer les insights
            try:
                user_id = get_current_user_id()
                insights_gen = get_insights_generator(user_id)
                insight_content = insights_gen.get_adaptive_insight()

                # Effacer le skeleton
                loading_placeholder.empty()

                # Nettoyer le texte des emojis pour un style épuré
                clean_content = remove_emojis(insight_content)

                # Supprimer les balises HTML brutes que l'IA pourrait avoir générées
                clean_content = strip_html_tags(clean_content)

                # Convertir le markdown en HTML pour un rendu correct
                formatted_content = convert_markdown_to_html(clean_content)

                # Afficher l'insight avec conteneur complet
                st.markdown(f"""
                <div style='background-color: var(--white); padding: 2rem;
                            border: 1px solid var(--line-light); border-left: 2px solid var(--black);
                            box-shadow: var(--shadow-subtle); margin-bottom: 1rem;
                            animation: fadeInUp 0.5s ease-out;'>
                    <div style='font-family: "Inter", sans-serif; color: var(--charcoal);
                               line-height: 1.8; font-size: 0.9375rem; font-weight: 300;
                               animation: fadeIn 0.5s ease-out;'>
                        {formatted_content}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            except ValueError as e:
                loading_placeholder.empty()
                st.error(f"Configuration manquante: {e}")
                st.info("Assurez-vous que ANTHROPIC_API_KEY est définie dans votre fichier .env")
                return
            except Exception as e:
                loading_placeholder.empty()
                st.error(f"Erreur lors de la génération des insights: {e}")
                return

        # Metadata insight dans un expander subtil
        with st.expander("Détails de l'analyse", expanded=False):
            db = get_database()
            user_id = get_current_user_id()
            latest_insight = db.get_latest_insight(user_id, "weekly")

            if latest_insight:
                created_at = datetime.fromisoformat(latest_insight["created_at"])
                age = datetime.now() - created_at

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"""
                    <div style='font-size: 0.9rem; color: #4A5568;'>
                    <strong>Généré le:</strong><br/>
                    {created_at.strftime('%d/%m/%Y à %H:%M')}
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"""
                    <div style='font-size: 0.9rem; color: #4A5568;'>
                    <strong>Tokens utilisés:</strong><br/>
                    {latest_insight['tokens_used']}
                    </div>
                    """, unsafe_allow_html=True)

                # Afficher si cached ou frais
                if age < timedelta(hours=24):
                    st.success(f"Insight récent (généré il y a {age.seconds // 3600}h)")
                else:
                    st.warning("Insight ancien, rechargez la page pour en générer un nouveau")

    else:
        # Empty state minimaliste
        st.markdown(
            create_empty_state(
                "Aucune donnée disponible",
                "Commencez votre voyage vers le bien-être en créant votre premier check-in ou en ayant une conversation avec votre compagnon IA"
            ),
            unsafe_allow_html=True
        )
