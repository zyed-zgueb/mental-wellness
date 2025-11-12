"""Fixtures pytest partagées pour les tests."""

import pytest
from src.database.db_manager import DatabaseManager


@pytest.fixture
def mock_db():
    """
    Fixture: DatabaseManager avec SQLite in-memory.

    Yields:
        Instance de DatabaseManager avec base de données en mémoire.
    """
    db = DatabaseManager(":memory:")
    yield db
    db.close()


@pytest.fixture
def sample_checkins(mock_db):
    """
    Fixture: DB pré-remplie avec données de test.

    Args:
        mock_db: Fixture DatabaseManager.

    Returns:
        Instance de DatabaseManager avec 5 check-ins pré-remplis.
    """
    for i in range(5):
        mock_db.save_checkin(mood_score=5 + i % 6, notes=f"Test note {i}")
    return mock_db
