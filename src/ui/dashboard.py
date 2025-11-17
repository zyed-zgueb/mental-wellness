"""Composant UI pour le dashboard avec visualisations et insights IA."""

import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
from src.database.db_manager import DatabaseManager
from src.llm.insights_generator import InsightsGenerator


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
    """Afficher le dashboard avec charts et insights IA - Style Apple Santé."""
    st.title("📊 Dashboard")
    st.markdown("""
    <p style='font-size: 1.05rem; color: var(--color-text-medium); margin-bottom: 2rem; line-height: 1.6;'>
    Visualisez vos tendances de bien-être et recevez des insights personnalisés.
    </p>
    """, unsafe_allow_html=True)

    db = get_database()

    # Section 1: Grande métrique centrale - Style Apple Santé
    st.markdown("### 💜 Votre Bien-être")

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

        # Grande métrique centrale - Style Apple Santé
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
                    padding: 2.5rem; border-radius: 16px; text-align: center; margin-bottom: 1.5rem;
                    box-shadow: 0 4px 12px rgba(107, 144, 128, 0.15);'>
            <div style='color: rgba(255, 255, 255, 0.9); font-size: 0.9rem; font-weight: 500; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 0.5rem;'>
                Score Actuel
            </div>
            <div style='color: white; font-size: 3.5rem; font-weight: 700; line-height: 1; margin-bottom: 0.25rem;'>
                {latest_mood:.1f}
            </div>
            <div style='color: rgba(255, 255, 255, 0.85); font-size: 1rem;'>
                sur 10
            </div>
            <div style='color: {"rgba(72, 187, 120, 1)" if delta >= 0 else "rgba(245, 101, 101, 1)"};
                        font-size: 0.95rem; margin-top: 1rem; font-weight: 500;'>
                {'+' if delta >= 0 else ''}{delta:.1f} vs moyenne
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Stats secondaires - Cards élégantes
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div class='stat-card' style='animation: fadeInUp 0.5s ease-out;'>
                <div style='color: var(--color-text-light); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;'>
                    Moyenne ({selected_period_label})
                </div>
                <div style='color: var(--color-primary); font-size: 2rem; font-weight: 600;'>
                    {avg_mood:.1f}
                </div>
                <div style='color: var(--color-text-light); font-size: 0.85rem;'>
                    sur 10
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class='stat-card' style='animation: fadeInUp 0.6s ease-out;'>
                <div style='color: var(--color-text-light); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;'>
                    Minimum ({selected_period_label})
                </div>
                <div style='color: var(--color-error); font-size: 2rem; font-weight: 600;'>
                    {min_mood}
                </div>
                <div style='color: var(--color-text-light); font-size: 0.85rem;'>
                    sur 10
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class='stat-card' style='animation: fadeInUp 0.7s ease-out;'>
                <div style='color: var(--color-text-light); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;'>
                    Maximum ({selected_period_label})
                </div>
                <div style='color: var(--color-success); font-size: 2rem; font-weight: 600;'>
                    {max_mood}
                </div>
                <div style='color: var(--color-text-light); font-size: 0.85rem;'>
                    sur 10
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

        # Graphique avec style Apple Santé - points individuels avec gradient de couleur
        st.markdown(f"### 📈 Tendance ({selected_period_label})")

        fig_mood = px.scatter(
            df_mood,
            x='timestamp',
            y='mood_score',
            color='mood_score',
            color_continuous_scale=[
                (0.0, '#F56565'),   # Rouge pour valeurs basses (0)
                (0.3, '#ED8936'),   # Orange
                (0.5, '#ECC94B'),   # Jaune
                (0.7, '#9AE6B4'),   # Vert clair
                (1.0, '#48BB78')    # Vert pour valeurs hautes (10)
            ],
            range_color=[0, 10]
        )

        # Style Apple Santé - points individuels sans ligne continue
        fig_mood.update_traces(
            mode='markers',
            marker=dict(size=14, line=dict(color='white', width=2), opacity=0.9),
            hovertemplate='<b>%{x|%d/%m/%Y à %H:%M}</b><br>Score: %{y}/10<extra></extra>'
        )

        fig_mood.update_layout(
            hovermode='x unified',
            xaxis_title="",
            yaxis_title="Score d'humeur",
            yaxis=dict(range=[0, 11], gridcolor='#E2E8F0'),
            xaxis=dict(gridcolor='#E2E8F0'),
            height=350,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="system-ui", color='#2D3748'),
            margin=dict(l=20, r=20, t=20, b=20),
            coloraxis_showscale=False  # Masquer la barre de couleur
        )

        st.plotly_chart(fig_mood, use_container_width=True)

    else:
        # État vide amélioré pour les données d'humeur
        st.markdown("""
        <div style='background: linear-gradient(135deg, #F7FAFC 0%, #F0FFF4 100%);
                    padding: 2rem; border-radius: 12px;
                    text-align: center; border-left: 4px solid #48BB78;
                    animation: fadeInUp 0.5s ease-out;'>
            <div style='font-size: 3rem; margin-bottom: 1rem; animation: bounce 2s infinite;'>🌸</div>
            <div style='font-size: 1.1rem; font-weight: 600; color: #2F855A; margin-bottom: 0.5rem;'>
                Commencez votre suivi d'humeur
            </div>
            <div style='font-size: 0.95rem; color: #4A5568;'>
                Créez votre premier check-in pour visualiser vos tendances de bien-être
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Divider élégant
    st.markdown("<div style='margin: 3rem 0;'></div>", unsafe_allow_html=True)

    # Section 2: Activité Conversations
    st.markdown("### 💬 Activité Conversations")

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
            <div style='background-color: var(--color-neutral-bg); padding: 1.5rem; border-radius: 12px; text-align: center;
                        box-shadow: var(--shadow-sm);'>
                <div style='color: var(--color-text-light); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;'>
                    Total
                </div>
                <div style='color: var(--color-primary); font-size: 2rem; font-weight: 600;'>
                    {total_conv}
                </div>
                <div style='color: var(--color-text-light); font-size: 0.85rem;'>
                    conversations
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style='background-color: var(--color-neutral-bg); padding: 1.5rem; border-radius: 12px; text-align: center;
                        box-shadow: var(--shadow-sm);'>
                <div style='color: var(--color-text-light); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;'>
                    Moyenne
                </div>
                <div style='color: var(--color-primary-dark); font-size: 2rem; font-weight: 600;'>
                    {avg_per_day:.1f}
                </div>
                <div style='color: var(--color-text-light); font-size: 0.85rem;'>
                    par jour
                </div>
            </div>
            """, unsafe_allow_html=True)

    else:
        # État vide amélioré pour les conversations
        st.markdown("""
        <div style='background: linear-gradient(135deg, #F7FAFC 0%, #EBF4FF 100%);
                    padding: 2rem; border-radius: 12px;
                    text-align: center; border-left: 4px solid var(--color-primary);
                    animation: fadeInUp 0.5s ease-out;'>
            <div style='font-size: 3rem; margin-bottom: 1rem; animation: pulse 2s infinite;'>💬</div>
            <div style='font-size: 1.1rem; font-weight: 600; color: var(--color-primary); margin-bottom: 0.5rem;'>
                Démarrez votre première conversation
            </div>
            <div style='font-size: 0.95rem; color: #4A5568;'>
                Partagez vos pensées avec votre compagnon IA empathique
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Divider élégant
    st.markdown("<div style='margin: 3rem 0;'></div>", unsafe_allow_html=True)

    # Section 3: AI Insights - L'expérience signature
    st.markdown("### ✨ Vos Insights Personnalisés")
    st.markdown("""
    <p style='color: #4A5568; margin-bottom: 1.5rem; font-size: 0.95rem;'>
    Découvrez des révélations actionnables sur votre bien-être mental
    </p>
    """, unsafe_allow_html=True)

    # Vérifier si des données existent (au moins 1 check-in ou 1 conversation)
    checkin_count = len(mood_data) if mood_data else 0
    conv_count = len(conv_history) if conv_history else 0

    if checkin_count > 0 or conv_count > 0:
        # Card premium pour insights avec animation subtile
        st.markdown("""
        <div style='background: linear-gradient(135deg, #EBF4FF 0%, #F7FAFC 100%);
                    padding: 2rem; border-radius: 16px; border-left: 4px solid var(--color-primary);
                    box-shadow: 0 4px 12px rgba(107, 70, 193, 0.12); margin-bottom: 1rem;
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
                ✨ Génération de vos insights personnalisés...
            </p>
            """, unsafe_allow_html=True)

        # Générer les insights
        try:
            insights_gen = get_insights_generator()
            insight_content = insights_gen.get_adaptive_insight()

            # Effacer le skeleton et afficher le contenu
            loading_placeholder.empty()

            # Afficher l'insight avec style élégant et animation
            st.markdown(f"""
            <div style='color: #2D3748; line-height: 1.8; font-size: 1.05rem; animation: fadeIn 0.5s ease-out;'>
            {insight_content}
            </div>
            """, unsafe_allow_html=True)

        except ValueError as e:
            loading_placeholder.empty()
            st.markdown("</div>", unsafe_allow_html=True)
            st.error(f"❌ Configuration manquante: {e}")
            st.info("💡 Assurez-vous que ANTHROPIC_API_KEY est définie dans votre fichier .env")
            return
        except Exception as e:
            loading_placeholder.empty()
            st.markdown("</div>", unsafe_allow_html=True)
            st.error(f"❌ Erreur lors de la génération des insights: {e}")
            return

        st.markdown("</div>", unsafe_allow_html=True)

        # Metadata insight dans un expander subtil
        with st.expander("ℹ️ Détails de l'analyse", expanded=False):
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
                    st.success(f"✨ Insight récent (généré il y a {age.seconds // 3600}h)")
                else:
                    st.warning("⚠️ Insight ancien, rechargez la page pour en générer un nouveau")

    else:
        # Empty state élégant avec animation
        st.markdown("""
        <div style='background: linear-gradient(135deg, #F7FAFC 0%, #EBF4FF 100%);
                    padding: 3rem 2rem; border-radius: 16px;
                    text-align: center; border: 2px dashed #CBD5E0;
                    animation: fadeInUp 0.5s ease-out;
                    box-shadow: 0 4px 12px rgba(107, 70, 193, 0.05);'>
            <div style='font-size: 4rem; margin-bottom: 1.5rem; animation: pulse 2s infinite;'>📊</div>
            <div style='font-size: 1.2rem; font-weight: 600; color: var(--color-primary); margin-bottom: 0.75rem;'>
                Aucune donnée disponible
            </div>
            <div style='font-size: 1rem; color: #4A5568; margin-bottom: 1.5rem; line-height: 1.6;'>
                Commencez votre voyage vers le bien-être en créant votre premier check-in<br/>
                ou en ayant une conversation avec votre compagnon IA
            </div>
            <div style='display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;'>
                <div style='background-color: white; padding: 1rem 1.5rem; border-radius: 8px;
                            box-shadow: 0 2px 8px rgba(107, 70, 193, 0.1); flex: 1; min-width: 200px; max-width: 250px;'>
                    <div style='font-size: 2rem; margin-bottom: 0.5rem;'>🌸</div>
                    <div style='color: var(--color-primary); font-weight: 500; font-size: 0.9rem;'>Quick Check-in</div>
                </div>
                <div style='background-color: white; padding: 1rem 1.5rem; border-radius: 8px;
                            box-shadow: 0 2px 8px rgba(107, 70, 193, 0.1); flex: 1; min-width: 200px; max-width: 250px;'>
                    <div style='font-size: 2rem; margin-bottom: 0.5rem;'>💬</div>
                    <div style='color: var(--color-primary); font-weight: 500; font-size: 0.9rem;'>Conversation</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
