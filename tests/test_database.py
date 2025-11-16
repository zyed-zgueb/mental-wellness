"""Tests unitaires pour le module DatabaseManager."""

import pytest
from datetime import datetime, timedelta
from src.database.db_manager import DatabaseManager


class TestDatabaseManagerInit:
    """Tests pour l'initialisation du DatabaseManager."""

    def test_init_creates_database(self, tmp_path):
        """Tester que l'initialisation crée une base de données."""
        db_path = tmp_path / "test.db"
        db = DatabaseManager(str(db_path))

        assert db_path.exists()
        db.close()

    def test_init_memory_database(self):
        """Tester l'initialisation avec base de données en mémoire."""
        db = DatabaseManager(":memory:")

        assert db.db_path == ":memory:"
        assert db.conn is not None
        db.close()


class TestSaveCheckin:
    """Tests pour la méthode save_checkin."""

    def test_save_checkin_success(self, mock_db):
        """Tester l'enregistrement réussi d'un check-in."""
        checkin_id = mock_db.save_checkin(mood_score=7, notes="Bonne journée")

        assert checkin_id > 0

    def test_save_checkin_returns_id(self, mock_db):
        """Tester que save_checkin retourne un ID valide."""
        id1 = mock_db.save_checkin(mood_score=5)
        id2 = mock_db.save_checkin(mood_score=8)

        assert id2 > id1

    def test_save_checkin_with_notes(self, mock_db):
        """Tester l'enregistrement avec notes."""
        checkin_id = mock_db.save_checkin(
            mood_score=6, notes="Journée productive"
        )

        history = mock_db.get_mood_history()
        assert len(history) == 1
        assert history[0]["notes"] == "Journée productive"

    def test_save_checkin_without_notes(self, mock_db):
        """Tester l'enregistrement sans notes (optionnel)."""
        checkin_id = mock_db.save_checkin(mood_score=5)

        history = mock_db.get_mood_history()
        assert len(history) == 1
        assert history[0]["notes"] == ""

    def test_save_checkin_invalid_mood_score_eleven(self, mock_db):
        """Tester validation: mood_score = 11 (invalide)."""
        with pytest.raises(ValueError, match="mood_score doit être"):
            mock_db.save_checkin(mood_score=11)

    def test_save_checkin_invalid_mood_score_negative(self, mock_db):
        """Tester validation: mood_score négatif (invalide)."""
        with pytest.raises(ValueError, match="mood_score doit être"):
            mock_db.save_checkin(mood_score=-5)

    def test_save_checkin_valid_boundaries(self, mock_db):
        """Tester les valeurs limites valides (0 et 10)."""
        id0 = mock_db.save_checkin(mood_score=0)
        id10 = mock_db.save_checkin(mood_score=10)

        assert id0 > 0
        assert id10 > 0

        history = mock_db.get_mood_history()
        assert len(history) == 2


class TestGetMoodHistory:
    """Tests pour la méthode get_mood_history."""

    def test_get_mood_history_empty(self, mock_db):
        """Tester historique vide (aucun check-in)."""
        history = mock_db.get_mood_history()

        assert history == []

    def test_get_mood_history_returns_recent(self, sample_checkins):
        """Tester que l'historique retourne les check-ins récents."""
        history = sample_checkins.get_mood_history()

        assert len(history) == 5

    def test_get_mood_history_sorted_desc(self, sample_checkins):
        """Tester que l'historique est trié du plus récent au plus ancien."""
        # Ajouter des check-ins avec délai pour garantir l'ordre
        db = DatabaseManager(":memory:")
        db.save_checkin(mood_score=3, notes="First")
        db.save_checkin(mood_score=7, notes="Second")
        db.save_checkin(mood_score=9, notes="Third")

        history = db.get_mood_history()

        # Le plus récent devrait être "Third"
        assert history[0]["notes"] == "Third"
        assert history[1]["notes"] == "Second"
        assert history[2]["notes"] == "First"

        db.close()

    def test_get_mood_history_filters_by_days(self, mock_db):
        """Tester filtrage par nombre de jours."""
        # Insérer un check-in "vieux" (40 jours)
        cutoff_date = datetime.now() - timedelta(days=40)
        mock_db.conn.execute(
            "INSERT INTO check_ins (mood_score, notes, timestamp) VALUES (?, ?, ?)",
            (5, "Old checkin", cutoff_date),
        )
        mock_db.conn.commit()

        # Insérer un check-in récent
        mock_db.save_checkin(mood_score=8, notes="Recent checkin")

        # Récupérer seulement les 30 derniers jours
        history = mock_db.get_mood_history(days=30)

        # Ne devrait avoir que le check-in récent
        assert len(history) == 1
        assert history[0]["notes"] == "Recent checkin"

    def test_get_mood_history_includes_all_fields(self, mock_db):
        """Tester que l'historique inclut tous les champs."""
        mock_db.save_checkin(mood_score=7, notes="Complete test")

        history = mock_db.get_mood_history()

        assert len(history) == 1
        checkin = history[0]

        # Vérifier que tous les champs sont présents
        assert "id" in checkin
        assert "timestamp" in checkin
        assert "mood_score" in checkin
        assert "notes" in checkin
        assert "created_at" in checkin

        # Vérifier les valeurs
        assert checkin["mood_score"] == 7
        assert checkin["notes"] == "Complete test"


class TestSaveConversation:
    """Tests pour la méthode save_conversation."""

    def test_save_conversation_success(self, mock_db):
        """Tester l'enregistrement réussi d'une conversation."""
        conv_id = mock_db.save_conversation(
            user_message="Bonjour",
            ai_response="Bonjour! Comment puis-je vous aider?",
            tokens_used=50
        )

        assert conv_id > 0

    def test_save_conversation_returns_id(self, mock_db):
        """Tester que save_conversation retourne un ID valide."""
        id1 = mock_db.save_conversation("Message 1", "Réponse 1", 30)
        id2 = mock_db.save_conversation("Message 2", "Réponse 2", 40)

        assert id2 > id1

    def test_save_conversation_with_tokens(self, mock_db):
        """Tester l'enregistrement avec tokens_used."""
        conv_id = mock_db.save_conversation(
            user_message="Test",
            ai_response="Réponse test",
            tokens_used=100
        )

        history = mock_db.get_conversation_history()
        assert len(history) == 1
        assert history[0]["tokens_used"] == 100

    def test_save_conversation_without_tokens(self, mock_db):
        """Tester l'enregistrement sans tokens_used (optionnel)."""
        conv_id = mock_db.save_conversation(
            user_message="Test",
            ai_response="Réponse"
        )

        history = mock_db.get_conversation_history()
        assert len(history) == 1
        assert history[0]["tokens_used"] == 0

    def test_save_conversation_empty_user_message(self, mock_db):
        """Tester validation: user_message vide (invalide)."""
        with pytest.raises(ValueError, match="Les messages ne peuvent pas être vides"):
            mock_db.save_conversation("", "Réponse", 10)

    def test_save_conversation_empty_ai_response(self, mock_db):
        """Tester validation: ai_response vide (invalide)."""
        with pytest.raises(ValueError, match="Les messages ne peuvent pas être vides"):
            mock_db.save_conversation("Message", "", 10)

    def test_save_conversation_both_empty(self, mock_db):
        """Tester validation: les deux messages vides (invalide)."""
        with pytest.raises(ValueError, match="Les messages ne peuvent pas être vides"):
            mock_db.save_conversation("", "", 10)


class TestGetConversationHistory:
    """Tests pour la méthode get_conversation_history."""

    def test_get_conversation_history_empty(self, mock_db):
        """Tester historique vide (aucune conversation)."""
        history = mock_db.get_conversation_history()

        assert history == []

    def test_get_conversation_history_returns_recent(self, mock_db):
        """Tester que l'historique retourne les conversations récentes."""
        mock_db.save_conversation("Message 1", "Réponse 1", 10)
        mock_db.save_conversation("Message 2", "Réponse 2", 20)
        mock_db.save_conversation("Message 3", "Réponse 3", 30)

        history = mock_db.get_conversation_history()

        assert len(history) == 3

    def test_get_conversation_history_sorted_desc(self, mock_db):
        """Tester que l'historique est trié du plus récent au plus ancien."""
        mock_db.save_conversation("First", "Réponse 1", 10)
        mock_db.save_conversation("Second", "Réponse 2", 20)
        mock_db.save_conversation("Third", "Réponse 3", 30)

        history = mock_db.get_conversation_history()

        # Le plus récent devrait être "Third"
        assert history[0]["user_message"] == "Third"
        assert history[1]["user_message"] == "Second"
        assert history[2]["user_message"] == "First"

    def test_get_conversation_history_respects_limit(self, mock_db):
        """Tester que la limite est respectée."""
        # Créer 10 conversations
        for i in range(10):
            mock_db.save_conversation(f"Message {i}", f"Réponse {i}", i * 10)

        # Récupérer seulement les 5 plus récentes
        history = mock_db.get_conversation_history(limit=5)

        assert len(history) == 5
        # Devrait avoir messages 9, 8, 7, 6, 5
        assert history[0]["user_message"] == "Message 9"
        assert history[4]["user_message"] == "Message 5"

    def test_get_conversation_history_includes_all_fields(self, mock_db):
        """Tester que l'historique inclut tous les champs."""
        mock_db.save_conversation(
            user_message="Test complet",
            ai_response="Réponse complète",
            tokens_used=75
        )

        history = mock_db.get_conversation_history()

        assert len(history) == 1
        conv = history[0]

        # Vérifier que tous les champs sont présents
        assert "id" in conv
        assert "timestamp" in conv
        assert "user_message" in conv
        assert "ai_response" in conv
        assert "tokens_used" in conv
        assert "created_at" in conv

        # Vérifier les valeurs
        assert conv["user_message"] == "Test complet"
        assert conv["ai_response"] == "Réponse complète"
        assert conv["tokens_used"] == 75


class TestGetConversationCount:
    """Tests pour la méthode get_conversation_count."""

    def test_get_conversation_count_empty(self, mock_db):
        """Tester comptage avec aucune conversation."""
        count = mock_db.get_conversation_count()

        assert count == 0

    def test_get_conversation_count_returns_correct_number(self, mock_db):
        """Tester que le comptage retourne le bon nombre."""
        mock_db.save_conversation("Message 1", "Réponse 1", 10)
        mock_db.save_conversation("Message 2", "Réponse 2", 20)
        mock_db.save_conversation("Message 3", "Réponse 3", 30)

        count = mock_db.get_conversation_count()

        assert count == 3

    def test_get_conversation_count_filters_by_days(self, mock_db):
        """Tester filtrage par nombre de jours."""
        # Insérer une conversation "vieille" (10 jours)
        old_date = datetime.now() - timedelta(days=10)
        mock_db.conn.execute(
            "INSERT INTO conversations (user_message, ai_response, tokens_used, timestamp) VALUES (?, ?, ?, ?)",
            ("Old message", "Old response", 10, old_date),
        )
        mock_db.conn.commit()

        # Insérer une conversation récente
        mock_db.save_conversation("Recent message", "Recent response", 20)

        # Compter seulement les 7 derniers jours
        count = mock_db.get_conversation_count(days=7)

        # Ne devrait avoir que la conversation récente
        assert count == 1

    def test_get_conversation_count_default_7_days(self, mock_db):
        """Tester que la valeur par défaut est 7 jours."""
        # Insérer conversations à différentes dates
        mock_db.save_conversation("Recent", "Response 1", 10)

        old_date = datetime.now() - timedelta(days=8)
        mock_db.conn.execute(
            "INSERT INTO conversations (user_message, ai_response, tokens_used, timestamp) VALUES (?, ?, ?, ?)",
            ("Old", "Response 2", 20, old_date),
        )
        mock_db.conn.commit()

        # Sans paramètre, devrait utiliser days=7
        count = mock_db.get_conversation_count()

        assert count == 1


class TestSaveInsight:
    """Tests pour la méthode save_insight."""

    def test_save_insight_success(self, mock_db):
        """Tester l'enregistrement réussi d'un insight."""
        insight_id = mock_db.save_insight(
            insight_type="weekly",
            content="Votre humeur s'améliore cette semaine!",
            based_on_data='{"checkins": 7, "avg_mood": 7.5}',
            tokens_used=150
        )

        assert insight_id > 0

    def test_save_insight_returns_id(self, mock_db):
        """Tester que save_insight retourne un ID valide."""
        id1 = mock_db.save_insight("weekly", "Insight 1", "", 100)
        id2 = mock_db.save_insight("monthly", "Insight 2", "", 200)

        assert id2 > id1

    def test_save_insight_with_optional_fields(self, mock_db):
        """Tester l'enregistrement avec champs optionnels."""
        insight_id = mock_db.save_insight(
            insight_type="weekly",
            content="Contenu de test"
        )

        latest = mock_db.get_latest_insight("weekly")
        assert latest is not None
        assert latest["based_on_data"] == ""
        assert latest["tokens_used"] == 0

    def test_save_insight_empty_type(self, mock_db):
        """Tester validation: insight_type vide (invalide)."""
        with pytest.raises(ValueError, match="insight_type et content ne peuvent pas être vides"):
            mock_db.save_insight("", "Contenu", "", 10)

    def test_save_insight_empty_content(self, mock_db):
        """Tester validation: content vide (invalide)."""
        with pytest.raises(ValueError, match="insight_type et content ne peuvent pas être vides"):
            mock_db.save_insight("weekly", "", "", 10)


class TestGetLatestInsight:
    """Tests pour la méthode get_latest_insight."""

    def test_get_latest_insight_empty(self, mock_db):
        """Tester récupération avec aucun insight."""
        latest = mock_db.get_latest_insight("weekly")

        assert latest is None

    def test_get_latest_insight_returns_most_recent(self, mock_db):
        """Tester que la méthode retourne le plus récent."""
        # Insérer avec des timestamps contrôlés pour garantir l'ordre
        old_date_1 = datetime.now() - timedelta(days=3)
        old_date_2 = datetime.now() - timedelta(days=2)
        recent_date = datetime.now() - timedelta(days=1)

        mock_db.conn.execute(
            "INSERT INTO insights_log (insight_type, content, tokens_used, created_at) VALUES (?, ?, ?, ?)",
            ("weekly", "Insight 1", 100, old_date_1),
        )
        mock_db.conn.execute(
            "INSERT INTO insights_log (insight_type, content, tokens_used, created_at) VALUES (?, ?, ?, ?)",
            ("weekly", "Insight 2", 200, old_date_2),
        )
        mock_db.conn.execute(
            "INSERT INTO insights_log (insight_type, content, tokens_used, created_at) VALUES (?, ?, ?, ?)",
            ("weekly", "Insight 3", 300, recent_date),
        )
        mock_db.conn.commit()

        latest = mock_db.get_latest_insight("weekly")

        assert latest is not None
        assert latest["content"] == "Insight 3"
        assert latest["tokens_used"] == 300

    def test_get_latest_insight_filters_by_type(self, mock_db):
        """Tester filtrage par type d'insight."""
        mock_db.save_insight("weekly", "Weekly insight", "", 100)
        mock_db.save_insight("monthly", "Monthly insight", "", 200)

        latest_weekly = mock_db.get_latest_insight("weekly")
        latest_monthly = mock_db.get_latest_insight("monthly")

        assert latest_weekly["content"] == "Weekly insight"
        assert latest_monthly["content"] == "Monthly insight"

    def test_get_latest_insight_includes_all_fields(self, mock_db):
        """Tester que l'insight inclut tous les champs."""
        mock_db.save_insight(
            insight_type="weekly",
            content="Insight complet",
            based_on_data='{"test": "data"}',
            tokens_used=250
        )

        latest = mock_db.get_latest_insight("weekly")

        assert latest is not None
        # Vérifier que tous les champs sont présents
        assert "id" in latest
        assert "created_at" in latest
        assert "insight_type" in latest
        assert "content" in latest
        assert "based_on_data" in latest
        assert "tokens_used" in latest

        # Vérifier les valeurs
        assert latest["insight_type"] == "weekly"
        assert latest["content"] == "Insight complet"
        assert latest["based_on_data"] == '{"test": "data"}'
        assert latest["tokens_used"] == 250
