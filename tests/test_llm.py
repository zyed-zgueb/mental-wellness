"""Tests unitaires pour le module ConversationManager."""

import pytest
import os
from unittest.mock import MagicMock, patch
from src.llm.conversation_manager import ConversationManager
from src.database.db_manager import DatabaseManager
import anthropic


@pytest.fixture
def mock_db():
    """Fixture pour une base de données en mémoire."""
    db = DatabaseManager(":memory:")
    yield db
    db.close()


@pytest.fixture
def mock_env_api_key(monkeypatch):
    """Mock ANTHROPIC_API_KEY dans l'environnement."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test-key")


@pytest.fixture
def mock_anthropic_stream(mocker):
    """Mock Anthropic streaming response."""
    def create_mock_stream():
        """Créer un nouveau mock stream pour chaque appel."""
        mock_stream = MagicMock()
        mock_stream.text_stream = iter(["Bonjour", " comment", " vas-tu", "?"])

        mock_usage = MagicMock()
        mock_usage.input_tokens = 10
        mock_usage.output_tokens = 20
        mock_stream.get_final_message.return_value.usage = mock_usage
        return mock_stream

    # Mock le context manager
    mock_client = mocker.patch('src.llm.conversation_manager.Anthropic')
    mock_client.return_value.messages.stream.return_value.__enter__.side_effect = create_mock_stream
    mock_client.return_value.messages.stream.return_value.__exit__.return_value = None

    return mock_client


class TestConversationManagerInit:
    """Tests pour l'initialisation du ConversationManager."""

    def test_init_success(self, mock_db, mock_env_api_key):
        """Tester initialisation réussie avec API key valide."""
        manager = ConversationManager(mock_db)

        assert manager.db == mock_db
        assert manager.system_prompt is not None

    def test_init_missing_api_key(self, mock_db, monkeypatch):
        """Tester que ValueError est levée si API key manquante."""
        # Supprimer la variable d'environnement
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

        with pytest.raises(ValueError, match="ANTHROPIC_API_KEY not found"):
            ConversationManager(mock_db)


class TestSendMessage:
    """Tests pour la méthode send_message."""

    def test_send_message_success(self, mock_db, mock_env_api_key, mock_anthropic_stream):
        """Tester envoi message avec streaming."""
        manager = ConversationManager(mock_db)

        response_chunks = list(manager.send_message("Hello"))

        assert response_chunks == ["Bonjour", " comment", " vas-tu", "?"]

    def test_send_message_saves_to_db(self, mock_db, mock_env_api_key, mock_anthropic_stream):
        """Tester que le message est sauvegardé dans la DB."""
        manager = ConversationManager(mock_db)

        # Envoyer un message
        response_chunks = list(manager.send_message("Hello"))

        # Vérifier que la conversation est sauvegardée
        history = mock_db.get_conversation_history()
        assert len(history) == 1
        assert history[0]["user_message"] == "Hello"
        assert history[0]["ai_response"] == "Bonjour comment vas-tu?"
        assert history[0]["tokens_used"] == 30  # 10 input + 20 output

    def test_send_message_api_error(self, mock_db, mock_env_api_key, mocker):
        """Tester gestion d'erreur API."""
        # Mock pour lever une exception
        mock_client = mocker.patch('src.llm.conversation_manager.Anthropic')
        mock_client.return_value.messages.stream.side_effect = Exception("API Error")

        manager = ConversationManager(mock_db)
        response = list(manager.send_message("Hello"))

        # Vérifier qu'un message d'erreur convivial est retourné
        assert len(response) == 1
        assert "difficultés techniques" in response[0]

    def test_send_message_includes_system_prompt(self, mock_db, mock_env_api_key, mock_anthropic_stream):
        """Tester que le system prompt est inclus dans l'appel API."""
        manager = ConversationManager(mock_db)

        list(manager.send_message("Test message"))

        # Vérifier que stream a été appelé avec le system prompt
        call_args = mock_anthropic_stream.return_value.messages.stream.call_args
        assert call_args[1]['system'] == manager.system_prompt
        assert call_args[1]['model'] == "claude-3-5-sonnet-20241022"
        assert call_args[1]['max_tokens'] == 1024


class TestDetectCrisis:
    """Tests pour la méthode detect_crisis."""

    def test_detect_crisis_keywords(self, mock_db, mock_env_api_key):
        """Tester détection de tous les mots-clés de crise."""
        manager = ConversationManager(mock_db)

        # Tester tous les keywords
        assert manager.detect_crisis("Je veux me suicider") is True
        assert manager.detect_crisis("Je vais me tuer") is True
        assert manager.detect_crisis("Je veux en finir") is True
        assert manager.detect_crisis("Je veux mourir") is True
        assert manager.detect_crisis("Je veux disparaître") is True
        assert manager.detect_crisis("Je veux me faire du mal") is True
        assert manager.detect_crisis("self-harm") is True
        assert manager.detect_crisis("automutilation") is True

    def test_detect_crisis_case_insensitive(self, mock_db, mock_env_api_key):
        """Tester que la détection est insensible à la casse."""
        manager = ConversationManager(mock_db)

        assert manager.detect_crisis("SUICIDE") is True
        assert manager.detect_crisis("SuIcIdE") is True
        assert manager.detect_crisis("Me Tuer") is True

    def test_detect_crisis_false_positive(self, mock_db, mock_env_api_key):
        """Tester que les messages normaux ne déclenchent pas de détection."""
        manager = ConversationManager(mock_db)

        assert manager.detect_crisis("Je me sens bien") is False
        assert manager.detect_crisis("Bonjour") is False
        assert manager.detect_crisis("Je suis un peu triste") is False
        assert manager.detect_crisis("Comment ça va?") is False

    def test_detect_crisis_partial_match(self, mock_db, mock_env_api_key):
        """Tester détection avec correspondance partielle dans phrase."""
        manager = ConversationManager(mock_db)

        assert manager.detect_crisis("Je pense parfois au suicide") is True
        assert manager.detect_crisis("J'ai des pensées de me faire du mal") is True


class TestIntegration:
    """Tests d'intégration pour le flux complet."""

    def test_full_conversation_flow(self, mock_db, mock_env_api_key, mock_anthropic_stream):
        """Tester le flux complet: envoi message + sauvegarde + récupération."""
        manager = ConversationManager(mock_db)

        # Envoyer un message
        list(manager.send_message("Bonjour"))

        # Vérifier historique
        history = manager.db.get_conversation_history()
        assert len(history) == 1
        assert history[0]["user_message"] == "Bonjour"
        assert history[0]["tokens_used"] > 0

    def test_multiple_conversations(self, mock_db, mock_env_api_key, mock_anthropic_stream):
        """Tester plusieurs conversations successives."""
        manager = ConversationManager(mock_db)

        # Envoyer plusieurs messages
        list(manager.send_message("Message 1"))
        list(manager.send_message("Message 2"))
        list(manager.send_message("Message 3"))

        # Vérifier historique
        history = manager.db.get_conversation_history()
        assert len(history) == 3
        assert history[0]["user_message"] == "Message 3"  # Plus récent en premier
        assert history[2]["user_message"] == "Message 1"  # Plus ancien en dernier
