"""Composant UI pour le dashboard avec visualisations et insights IA - Gallery Minimalist Style"""

import streamlit as st
import plotly.express as px
import pandas as pd
import re
from datetime import datetime, timedelta
from src.database.db_manager import DatabaseManager
from src.llm.insights_generator import InsightsGenerator


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


@st.cache_resource
def get_database():
    """
    Singleton DatabaseManager pour toute l'application.

    Returns:
        Instance unique de DatabaseManager.
    """
    return DatabaseManager("serene.db")


@st.cache_resource
def get_insights_generator():
    """
    Singleton InsightsGenerator pour toute l'application.

    Returns:
        Instance unique de InsightsGenerator.
    """
    db = get_database()
    return InsightsGenerator(db)


def show_dashboard():
    """Afficher le dashboard - Gallery minimalist style."""

    # Header minimaliste
    st.markdown("""
    <div style='animation: fadeInDown 0.4s ease-out; margin-bottom: 3rem;
                padding-bottom: 2rem; border-bottom: 1px solid var(--line-light);'>
        <h1 style='font-family: "Cormorant Garamond", serif; font-size: 3rem;
                   color: var(--black); font-weight: 300; margin-bottom: 1rem;
                   letter-spacing: 0.02em; line-height: 1.1;'>
            Dashboard
        </h1>
        <p style='font-family: "Inter", sans-serif; font-size: 0.9375rem;
                 color: var(--gray-dark); margin: 0; line-height: 1.8;
                 font-weight: 300; max-width: 600px;'>
            Visualisez vos tendances de bien-être et recevez des insights personnalisés.
        </p>
    </div>
    """, unsafe_allow_html=True)

    db = get_database()

    # Section 1: Grande métrique centrale - Style minimaliste
    st.markdown("""
    <h2 style='font-family: "Cormorant Garamond", serif; font-size: 2rem;
               font-weight: 300; color: var(--black); margin-bottom: 2rem;
               letter-spacing: 0.02em;'>
        <i class="fa-regular fa-heart" style='margin-right: 0.75rem; opacity: 0.65; font-size: 1.75rem;'></i>
        Votre Bien-être
    </h2>
    """, unsafe_allow_html=True)

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

    mood_data = db.get_mood_history(days=selected_days)

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
        st.markdown(f"""
        <div style='background-color: var(--white); padding: 3rem 2rem;
                    border: 1px solid var(--line-light); text-align: center;
                    margin-bottom: 2rem; box-shadow: var(--shadow-subtle);'>
            <div style='font-family: "Inter", sans-serif; color: var(--gray-medium);
                       font-size: 0.75rem; font-weight: 400; letter-spacing: 0.1em;
                       text-transform: uppercase; margin-bottom: 1rem;'>
                Score Actuel
            </div>
            <div style='font-family: "Cormorant Garamond", serif; color: var(--black);
                       font-size: 5rem; font-weight: 300; line-height: 1; margin-bottom: 0.5rem;'>
                {latest_mood:.1f}
            </div>
            <div style='font-family: "Inter", sans-serif; color: var(--gray-medium);
                       font-size: 0.875rem; font-weight: 300; margin-bottom: 1.5rem;'>
                sur 10
            </div>
            <div style='width: 60px; height: 1px; background-color: var(--line-dark); margin: 1.5rem auto;'></div>
            <div style='font-family: "Inter", sans-serif; color: var(--charcoal);
                       font-size: 0.875rem; margin-top: 1rem; font-weight: 300;'>
                {'+' if delta >= 0 else ''}{delta:.1f} vs moyenne
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Stats secondaires - Style minimaliste
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div style='background-color: var(--white); padding: 1.5rem; text-align: center;
                        border: 1px solid var(--line-light); box-shadow: var(--shadow-subtle);
                        animation: fadeInUp 0.5s ease-out;'>
                <div style='font-family: "Inter", sans-serif; color: var(--gray-light);
                           font-size: 0.6875rem; text-transform: uppercase; letter-spacing: 0.1em;
                           margin-bottom: 0.75rem; font-weight: 400;'>
                    Moyenne ({selected_period_label})
                </div>
                <div style='font-family: "Cormorant Garamond", serif; color: var(--black);
                           font-size: 2.5rem; font-weight: 300;'>
                    {avg_mood:.1f}
                </div>
                <div style='font-family: "Inter", sans-serif; color: var(--gray-medium);
                           font-size: 0.75rem; font-weight: 300;'>
                    sur 10
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style='background-color: var(--white); padding: 1.5rem; text-align: center;
                        border: 1px solid var(--line-light); box-shadow: var(--shadow-subtle);
                        animation: fadeInUp 0.6s ease-out;'>
                <div style='font-family: "Inter", sans-serif; color: var(--gray-light);
                           font-size: 0.6875rem; text-transform: uppercase; letter-spacing: 0.1em;
                           margin-bottom: 0.75rem; font-weight: 400;'>
                    Minimum ({selected_period_label})
                </div>
                <div style='font-family: "Cormorant Garamond", serif; color: var(--black);
                           font-size: 2.5rem; font-weight: 300;'>
                    {min_mood}
                </div>
                <div style='font-family: "Inter", sans-serif; color: var(--gray-medium);
                           font-size: 0.75rem; font-weight: 300;'>
                    sur 10
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div style='background-color: var(--white); padding: 1.5rem; text-align: center;
                        border: 1px solid var(--line-light); box-shadow: var(--shadow-subtle);
                        animation: fadeInUp 0.7s ease-out;'>
                <div style='font-family: "Inter", sans-serif; color: var(--gray-light);
                           font-size: 0.6875rem; text-transform: uppercase; letter-spacing: 0.1em;
                           margin-bottom: 0.75rem; font-weight: 400;'>
                    Maximum ({selected_period_label})
                </div>
                <div style='font-family: "Cormorant Garamond", serif; color: var(--black);
                           font-size: 2.5rem; font-weight: 300;'>
                    {max_mood}
                </div>
                <div style='font-family: "Inter", sans-serif; color: var(--gray-medium);
                           font-size: 0.75rem; font-weight: 300;'>
                    sur 10
                </div>
            </div>
            """, unsafe_allow_html=True)

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
        st.markdown("""
        <div style='background-color: var(--ivory-dark); padding: 4rem 3rem;
                    border: 1px solid var(--line-light); text-align: center;
                    animation: fadeInUp 0.5s ease-out;'>
            <div style='font-family: "Cormorant Garamond", serif; font-size: 1.75rem;
                       font-weight: 300; color: var(--black); margin-bottom: 1rem;
                       letter-spacing: 0.02em;'>
                Commencez votre suivi
            </div>
            <div style='font-family: "Inter", sans-serif; font-size: 0.875rem;
                       color: var(--gray-dark); font-weight: 300; line-height: 1.7;'>
                Créez votre premier check-in pour visualiser vos tendances de bien-être
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Divider minimaliste
    st.markdown("<hr style='border: none; border-top: 1px solid var(--line-light); margin: 3rem 0;'>", unsafe_allow_html=True)

    # Section 2: Activité Conversations
    st.markdown("""
    <h2 style='font-family: "Cormorant Garamond", serif; font-size: 2rem;
               font-weight: 300; color: var(--black); margin-bottom: 2rem;
               letter-spacing: 0.02em;'>
        <i class="fa-regular fa-message" style='margin-right: 0.75rem; opacity: 0.65; font-size: 1.75rem;'></i>
        Activité Conversations
    </h2>
    """, unsafe_allow_html=True)

    conv_history = db.get_conversation_history(limit=100)

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
            st.markdown(f"""
            <div style='background-color: var(--white); padding: 1.5rem; text-align: center;
                        border: 1px solid var(--line-light); box-shadow: var(--shadow-subtle);'>
                <div style='font-family: "Inter", sans-serif; color: var(--gray-light);
                           font-size: 0.6875rem; text-transform: uppercase; letter-spacing: 0.1em;
                           margin-bottom: 0.75rem; font-weight: 400;'>
                    Total
                </div>
                <div style='font-family: "Cormorant Garamond", serif; color: var(--black);
                           font-size: 2.5rem; font-weight: 300;'>
                    {total_conv}
                </div>
                <div style='font-family: "Inter", sans-serif; color: var(--gray-medium);
                           font-size: 0.75rem; font-weight: 300;'>
                    conversations
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style='background-color: var(--white); padding: 1.5rem; text-align: center;
                        border: 1px solid var(--line-light); box-shadow: var(--shadow-subtle);'>
                <div style='font-family: "Inter", sans-serif; color: var(--gray-light);
                           font-size: 0.6875rem; text-transform: uppercase; letter-spacing: 0.1em;
                           margin-bottom: 0.75rem; font-weight: 400;'>
                    Moyenne
                </div>
                <div style='font-family: "Cormorant Garamond", serif; color: var(--black);
                           font-size: 2.5rem; font-weight: 300;'>
                    {avg_per_day:.1f}
                </div>
                <div style='font-family: "Inter", sans-serif; color: var(--gray-medium);
                           font-size: 0.75rem; font-weight: 300;'>
                    par jour
                </div>
            </div>
            """, unsafe_allow_html=True)

    else:
        # État vide minimaliste
        st.markdown("""
        <div style='background-color: var(--ivory-dark); padding: 4rem 3rem;
                    border: 1px solid var(--line-light); text-align: center;
                    animation: fadeInUp 0.5s ease-out;'>
            <div style='font-family: "Cormorant Garamond", serif; font-size: 1.75rem;
                       font-weight: 300; color: var(--black); margin-bottom: 1rem;
                       letter-spacing: 0.02em;'>
                Démarrez votre première conversation
            </div>
            <div style='font-family: "Inter", sans-serif; font-size: 0.875rem;
                       color: var(--gray-dark); font-weight: 300; line-height: 1.7;'>
                Partagez vos pensées avec votre compagnon IA empathique
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Divider minimaliste
    st.markdown("<hr style='border: none; border-top: 1px solid var(--line-light); margin: 3rem 0;'>", unsafe_allow_html=True)

    # Section 3: AI Insights
    st.markdown("""
    <h2 style='font-family: "Cormorant Garamond", serif; font-size: 2rem;
               font-weight: 300; color: var(--black); margin-bottom: 1rem;
               letter-spacing: 0.02em;'>
        <i class="fa-solid fa-sparkles" style='margin-right: 0.75rem; opacity: 0.65; font-size: 1.75rem;'></i>
        Vos Insights Personnalisés
    </h2>
    <p style='font-family: "Inter", sans-serif; color: var(--gray-dark);
             margin-bottom: 2rem; font-size: 0.875rem; font-weight: 300; line-height: 1.7;'>
        Découvrez des révélations actionnables sur votre bien-être mental
    </p>
    """, unsafe_allow_html=True)

    # Vérifier si des données existent (au moins 1 check-in ou 1 conversation)
    checkin_count = len(mood_data) if mood_data else 0
    conv_count = len(conv_history) if conv_history else 0

    if checkin_count > 0 or conv_count > 0:
        # Card minimaliste pour insights
        st.markdown("""
        <div style='background-color: var(--white); padding: 2rem;
                    border: 1px solid var(--line-light); border-left: 2px solid var(--black);
                    box-shadow: var(--shadow-subtle); margin-bottom: 1rem;
                    animation: fadeInUp 0.5s ease-out;'>
        """, unsafe_allow_html=True)

        # Loading skeleton pendant la génération
        loading_placeholder = st.empty()
        with loading_placeholder.container():
            st.markdown("""
            <div style='margin-bottom: 1rem;'>
                <div class='skeleton' style='height: 1.5rem; width: 70%; margin-bottom: 1rem;'></div>
                <div class='skeleton' style='height: 1rem; width: 100%; margin-bottom: 0.5rem;'></div>
                <div class='skeleton' style='height: 1rem; width: 95%; margin-bottom: 0.5rem;'></div>
                <div class='skeleton' style='height: 1rem; width: 85%;'></div>
            </div>
            <p style='color: var(--color-primary); font-size: 0.9rem; text-align: center; margin-top: 1.5rem;'>
                Génération de vos insights personnalisés...
            </p>
            """, unsafe_allow_html=True)

        # Générer les insights
        try:
            insights_gen = get_insights_generator()
            insight_content = insights_gen.get_adaptive_insight()

            # Effacer le skeleton et afficher le contenu
            loading_placeholder.empty()

            # Nettoyer le texte des emojis pour un style épuré
            clean_content = remove_emojis(insight_content)

            # Afficher l'insight avec style minimaliste
            st.markdown(f"""
            <div style='font-family: "Inter", sans-serif; color: var(--charcoal);
                       line-height: 1.8; font-size: 0.9375rem; font-weight: 300;
                       animation: fadeIn 0.5s ease-out;'>
                {clean_content}
            </div>
            """, unsafe_allow_html=True)

        except ValueError as e:
            loading_placeholder.empty()
            st.markdown("</div>", unsafe_allow_html=True)
            st.error(f"Configuration manquante: {e}")
            st.info("Assurez-vous que ANTHROPIC_API_KEY est définie dans votre fichier .env")
            return
        except Exception as e:
            loading_placeholder.empty()
            st.markdown("</div>", unsafe_allow_html=True)
            st.error(f"Erreur lors de la génération des insights: {e}")
            return

        st.markdown("</div>", unsafe_allow_html=True)

        # Metadata insight dans un expander subtil
        with st.expander("Détails de l'analyse", expanded=False):
            db = get_database()
            latest_insight = db.get_latest_insight("weekly")

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
        st.markdown("""
        <div style='background-color: var(--ivory-dark); padding: 4rem 3rem;
                    border: 1px solid var(--line-light); text-align: center;
                    animation: fadeInUp 0.5s ease-out;'>
            <div style='font-family: "Cormorant Garamond", serif; font-size: 1.75rem;
                       font-weight: 300; color: var(--black); margin-bottom: 1rem;
                       letter-spacing: 0.02em;'>
                Aucune donnée disponible
            </div>
            <div style='font-family: "Inter", sans-serif; font-size: 0.875rem;
                       color: var(--gray-dark); margin-bottom: 2rem; line-height: 1.8;
                       font-weight: 300; max-width: 500px; margin-left: auto; margin-right: auto;'>
                Commencez votre voyage vers le bien-être en créant votre premier check-in
                ou en ayant une conversation avec votre compagnon IA
            </div>
            <div style='width: 80px; height: 1px; background-color: var(--line-dark); margin: 0 auto;'></div>
        </div>
        """, unsafe_allow_html=True)
