"""Tests unitaires pour le module InsightsGenerator."""

import pytest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from src.llm.insights_generator import InsightsGenerator


class TestInsightsGeneratorInit:
    """Tests pour l'initialisation du InsightsGenerator."""

    def test_init_with_valid_api_key(self, mock_db, monkeypatch):
        """Tester que l'initialisation réussit avec une clé API valide."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

        generator = InsightsGenerator(mock_db)

        assert generator.db == mock_db
        assert generator.client is not None

    def test_init_without_api_key(self, mock_db, monkeypatch):
        """Tester que l'initialisation échoue sans clé API."""
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

        with pytest.raises(ValueError, match="ANTHROPIC_API_KEY not found"):
            InsightsGenerator(mock_db)


class TestDataMaturityLevel:
    """Tests pour la détection du niveau de maturité des données."""

    def test_data_maturity_level_early(self, mock_db, monkeypatch):
        """Tester détection niveau 'early' (<3 jours)."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
        generator = InsightsGenerator(mock_db)

        assert generator._get_data_maturity_level(0) == "early"
        assert generator._get_data_maturity_level(1) == "early"
        assert generator._get_data_maturity_level(2) == "early"

    def test_data_maturity_level_developing(self, mock_db, monkeypatch):
        """Tester détection niveau 'developing' (3-6 jours)."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
        generator = InsightsGenerator(mock_db)

        assert generator._get_data_maturity_level(3) == "developing"
        assert generator._get_data_maturity_level(4) == "developing"
        assert generator._get_data_maturity_level(5) == "developing"
        assert generator._get_data_maturity_level(6) == "developing"

    def test_data_maturity_level_mature(self, mock_db, monkeypatch):
        """Tester détection niveau 'mature' (≥7 jours)."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
        generator = InsightsGenerator(mock_db)

        assert generator._get_data_maturity_level(7) == "mature"
        assert generator._get_data_maturity_level(10) == "mature"
        assert generator._get_data_maturity_level(30) == "mature"


class TestCachingLogic:
    """Tests pour la logique de cache 24h."""

    def test_should_regenerate_no_existing_insight(self, mock_db, monkeypatch):
        """Tester que régénération est requise si aucun insight existant."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
        generator = InsightsGenerator(mock_db)

        assert generator._should_regenerate_insights() is True

    def test_should_regenerate_within_24h(self, mock_db, monkeypatch):
        """Tester que régénération n'est PAS requise si insight <24h."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

        # Créer un insight récent (<24h)
        recent_time = datetime.now() - timedelta(hours=12)
        mock_db.conn.execute(
            "INSERT INTO insights_log (insight_type, content, created_at) VALUES (?, ?, ?)",
            ("weekly", "Recent insight", recent_time.isoformat()),
        )
        mock_db.conn.commit()

        generator = InsightsGenerator(mock_db)

        assert generator._should_regenerate_insights() is False

    def test_should_regenerate_after_24h(self, mock_db, monkeypatch):
        """Tester que régénération est requise si insight >24h."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

        # Créer un insight vieux (>24h)
        old_time = datetime.now() - timedelta(hours=25)
        mock_db.conn.execute(
            "INSERT INTO insights_log (insight_type, content, created_at) VALUES (?, ?, ?)",
            ("weekly", "Old insight", old_time.isoformat()),
        )
        mock_db.conn.commit()

        generator = InsightsGenerator(mock_db)

        assert generator._should_regenerate_insights() is True


class TestGetAdaptiveInsight:
    """Tests pour la méthode get_adaptive_insight."""

    def test_get_adaptive_insight_returns_cached(self, mock_db, monkeypatch):
        """Tester que insight cached est retourné si <24h."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

        # Créer un insight récent
        recent_time = datetime.now() - timedelta(hours=1)
        mock_db.save_insight(
            insight_type="weekly",
            content="Cached insight content",
            based_on_data="{}",
            tokens_used=100
        )

        generator = InsightsGenerator(mock_db)
        result = generator.get_adaptive_insight()

        assert result == "Cached insight content"


class TestGenerateAdaptiveSummary:
    """Tests pour la génération d'insights adaptatifs."""

    def test_generate_adaptive_summary_early(self, mock_db, monkeypatch, mocker):
        """Tester génération insight avec données 'early' (<3 jours)."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

        # Mock Anthropic AVANT d'instancier InsightsGenerator
        mock_message = MagicMock()
        mock_message.content = [MagicMock(text="## Insight généré\nC'est un excellent début ! 🌱")]
        mock_message.usage = MagicMock(input_tokens=50, output_tokens=100)

        mock_client_instance = MagicMock()
        mock_client_instance.messages.create.return_value = mock_message

        mock_anthropic_class = mocker.patch('src.llm.insights_generator.Anthropic')
        mock_anthropic_class.return_value = mock_client_instance

        # Ajouter 2 check-ins (early)
        mock_db.save_checkin(7, "Note 1")
        mock_db.save_checkin(8, "Note 2")

        generator = InsightsGenerator(mock_db)
        result = generator.generate_adaptive_summary()

        assert "Insight généré" in result
        # Vérifier que l'insight a été sauvegardé
        latest = mock_db.get_latest_insight("weekly")
        assert latest is not None
        assert latest["tokens_used"] == 150

    def test_generate_adaptive_summary_developing(self, mock_db, monkeypatch, mocker):
        """Tester génération insight avec données 'developing' (3-6 jours)."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

        # Mock Anthropic
        mock_message = MagicMock()
        mock_message.content = [MagicMock(text="## Observations préliminaires\nBelle régularité !")]
        mock_message.usage = MagicMock(input_tokens=60, output_tokens=120)

        mock_client_instance = MagicMock()
        mock_client_instance.messages.create.return_value = mock_message

        mock_anthropic_class = mocker.patch('src.llm.insights_generator.Anthropic')
        mock_anthropic_class.return_value = mock_client_instance

        # Ajouter 5 check-ins (developing)
        for i in range(5):
            mock_db.save_checkin(5 + i, f"Note {i}")

        generator = InsightsGenerator(mock_db)
        result = generator.generate_adaptive_summary()

        assert "Observations" in result or "Belle" in result

    def test_generate_adaptive_summary_mature(self, mock_db, monkeypatch, mocker):
        """Tester génération insight avec données 'mature' (≥7 jours)."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

        # Mock Anthropic
        mock_message = MagicMock()
        mock_message.content = [MagicMock(text="## Analyse complète\nTendances et patterns")]
        mock_message.usage = MagicMock(input_tokens=70, output_tokens=150)

        mock_client_instance = MagicMock()
        mock_client_instance.messages.create.return_value = mock_message

        mock_anthropic_class = mocker.patch('src.llm.insights_generator.Anthropic')
        mock_anthropic_class.return_value = mock_client_instance

        # Ajouter 10 check-ins (mature)
        for i in range(10):
            mock_db.save_checkin(5 + (i % 5), f"Note {i}")

        generator = InsightsGenerator(mock_db)
        result = generator.generate_adaptive_summary()

        assert "Analyse" in result or "Tendances" in result

    def test_insights_saved_to_db(self, mock_db, monkeypatch, mocker):
        """Tester que les insights sont bien sauvegardés en DB."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

        # Mock Anthropic
        mock_message = MagicMock()
        mock_message.content = [MagicMock(text="## Insight généré\nC'est un excellent début ! 🌱")]
        mock_message.usage = MagicMock(input_tokens=50, output_tokens=100)

        mock_client_instance = MagicMock()
        mock_client_instance.messages.create.return_value = mock_message

        mock_anthropic_class = mocker.patch('src.llm.insights_generator.Anthropic')
        mock_anthropic_class.return_value = mock_client_instance

        # Ajouter des données
        mock_db.save_checkin(7, "Test note")

        generator = InsightsGenerator(mock_db)
        generator.generate_adaptive_summary()

        # Vérifier sauvegarde
        latest = mock_db.get_latest_insight("weekly")
        assert latest is not None
        assert latest["insight_type"] == "weekly"
        assert latest["content"] == "## Insight généré\nC'est un excellent début ! 🌱"
        assert "based_on_data" in latest

    def test_api_error_handling(self, mock_db, monkeypatch, mocker):
        """Tester gestion des erreurs API."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

        # Mock erreur API
        mock_client_instance = MagicMock()
        mock_client_instance.messages.create.side_effect = Exception("API Error")

        mock_anthropic_class = mocker.patch('src.llm.insights_generator.Anthropic')
        mock_anthropic_class.return_value = mock_client_instance

        # Ajouter des données
        mock_db.save_checkin(7, "Test note")

        generator = InsightsGenerator(mock_db)
        result = generator.generate_adaptive_summary()

        # Vérifier message d'erreur convivial
        assert "désolée" in result.lower()
        assert "réessayer" in result.lower()


class TestBuildDataContext:
    """Tests pour la construction du contexte des données."""

    def test_build_data_context_with_notes(self, mock_db, monkeypatch):
        """Tester construction du contexte avec notes."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

        mock_db.save_checkin(7, "Bonne journée")
        mock_db.save_checkin(8, "Excellent")

        generator = InsightsGenerator(mock_db)
        mood_data = mock_db.get_mood_history(days=30)
        conv_count = 5

        context = generator._build_data_context(mood_data, conv_count, len(mood_data))

        assert "Nombre de jours de données: 2" in context
        assert "Nombre de conversations: 5" in context
        assert "Score d'humeur moyen" in context
        assert "Bonne journée" in context

    def test_build_data_context_with_conversations(self, mock_db, monkeypatch):
        """Tester construction du contexte avec conversations."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

        # Ajouter des check-ins
        mock_db.save_checkin(7, "Bonne journée")

        # Ajouter des conversations
        mock_db.save_conversation("Je me sens anxieux aujourd'hui", "Je comprends...", 50)
        mock_db.save_conversation("J'ai du mal à dormir", "C'est difficile...", 60)
        mock_db.save_conversation("Je suis content de mes progrès", "C'est génial!", 40)

        generator = InsightsGenerator(mock_db)
        mood_data = mock_db.get_mood_history(days=30)
        conv_count = 3
        conv_history = mock_db.get_conversation_history(limit=10)

        context = generator._build_data_context(mood_data, conv_count, len(mood_data), conv_history)

        # Vérifier que les conversations sont incluses
        assert "Extraits de conversations récentes" in context
        assert "anxieux" in context
        assert "dormir" in context
        assert "progrès" in context

    def test_build_data_context_truncates_long_messages(self, mock_db, monkeypatch):
        """Tester que les messages longs sont tronqués à 200 caractères."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

        # Message de plus de 200 caractères
        long_message = "A" * 250
        mock_db.save_conversation(long_message, "Réponse courte", 50)

        generator = InsightsGenerator(mock_db)
        conv_history = mock_db.get_conversation_history(limit=10)

        context = generator._build_data_context([], 1, 0, conv_history)

        # Vérifier que le message est tronqué
        assert "A" * 200 in context
        assert "..." in context
        # Vérifier qu'il n'y a pas 250 'A'
        assert "A" * 250 not in context

    def test_calculate_avg_mood(self, mock_db, monkeypatch):
        """Tester calcul du score moyen."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

        mock_db.save_checkin(6, "Note 1")
        mock_db.save_checkin(8, "Note 2")
        mock_db.save_checkin(10, "Note 3")

        generator = InsightsGenerator(mock_db)
        mood_data = mock_db.get_mood_history(days=30)

        avg = generator._calculate_avg_mood(mood_data)

        assert avg == 8.0  # (6 + 8 + 10) / 3
