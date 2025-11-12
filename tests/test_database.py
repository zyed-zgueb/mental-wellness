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

    def test_save_checkin_invalid_mood_score_zero(self, mock_db):
        """Tester validation: mood_score = 0 (invalide)."""
        with pytest.raises(ValueError, match="mood_score doit être"):
            mock_db.save_checkin(mood_score=0)

    def test_save_checkin_invalid_mood_score_eleven(self, mock_db):
        """Tester validation: mood_score = 11 (invalide)."""
        with pytest.raises(ValueError, match="mood_score doit être"):
            mock_db.save_checkin(mood_score=11)

    def test_save_checkin_invalid_mood_score_negative(self, mock_db):
        """Tester validation: mood_score négatif (invalide)."""
        with pytest.raises(ValueError, match="mood_score doit être"):
            mock_db.save_checkin(mood_score=-5)

    def test_save_checkin_valid_boundaries(self, mock_db):
        """Tester les valeurs limites valides (1 et 10)."""
        id1 = mock_db.save_checkin(mood_score=1)
        id2 = mock_db.save_checkin(mood_score=10)

        assert id1 > 0
        assert id2 > 0

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
