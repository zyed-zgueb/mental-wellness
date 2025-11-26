"""
Unit tests for password validation functionality.

Tests password strength validation, complexity requirements,
common password detection, and password scoring.
"""

import pytest
import os
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.password_validator import (
    validate_password_strength,
    calculate_password_score,
    check_common_passwords,
    get_password_feedback
)


class TestPasswordStrengthValidation:
    """Test password strength validation rules."""

    def test_valid_strong_password(self):
        """Test that a strong password is accepted."""
        password = "Serene2024!"
        is_valid, message = validate_password_strength(password)
        assert is_valid is True
        assert "valide" in message.lower() or "fort" in message.lower()

    def test_another_valid_password(self):
        """Test another strong password combination."""
        password = "MyP@ssw0rd123"
        is_valid, message = validate_password_strength(password)
        assert is_valid is True

    def test_password_too_short(self):
        """Test that passwords under 8 characters are rejected."""
        password = "Pass1!"
        is_valid, message = validate_password_strength(password)
        assert is_valid is False
        assert "8 caractères" in message or "trop court" in message.lower()

    def test_password_exactly_8_chars(self):
        """Test that 8 character password with all requirements is valid."""
        password = "Pass123!"
        is_valid, message = validate_password_strength(password)
        assert is_valid is True

    def test_password_no_uppercase(self):
        """Test that password without uppercase is rejected."""
        password = "password123!"
        is_valid, message = validate_password_strength(password)
        assert is_valid is False
        assert "majuscule" in message.lower()

    def test_password_no_lowercase(self):
        """Test that password without lowercase is rejected."""
        password = "PASSWORD123!"
        is_valid, message = validate_password_strength(password)
        assert is_valid is False
        assert "minuscule" in message.lower()

    def test_password_no_digit(self):
        """Test that password without digit is rejected."""
        password = "Password!"
        is_valid, message = validate_password_strength(password)
        assert is_valid is False
        assert "chiffre" in message.lower()

    def test_password_no_special_char(self):
        """Test that password without special character is rejected."""
        password = "Password123"
        is_valid, message = validate_password_strength(password)
        assert is_valid is False
        assert "spécial" in message.lower()

    def test_password_empty_string(self):
        """Test that empty password is rejected."""
        password = ""
        is_valid, message = validate_password_strength(password)
        assert is_valid is False

    def test_password_only_spaces(self):
        """Test that password with only spaces is rejected."""
        password = "        "
        is_valid, message = validate_password_strength(password)
        assert is_valid is False


class TestCommonPasswords:
    """Test common password detection."""

    def test_common_password_123456(self):
        """Test that '123456' is detected as common."""
        is_valid, message = validate_password_strength("123456")
        assert is_valid is False
        assert check_common_passwords("123456") is True

    def test_common_password_password(self):
        """Test that 'password' is detected as common."""
        is_valid, message = validate_password_strength("password")
        assert is_valid is False
        assert check_common_passwords("password") is True

    def test_common_password_qwerty(self):
        """Test that 'qwerty' is detected as common."""
        is_valid, message = validate_password_strength("qwerty")
        assert is_valid is False
        assert check_common_passwords("qwerty") is True

    def test_common_password_password123(self):
        """Test that 'password123' is detected as common."""
        is_valid, message = validate_password_strength("password123")
        assert is_valid is False
        assert check_common_passwords("password123") is True

    def test_not_common_password(self):
        """Test that a unique password is not flagged as common."""
        password = "Serene2024!"
        assert check_common_passwords(password) is False

    def test_common_password_case_insensitive(self):
        """Test that common password detection is case-insensitive."""
        assert check_common_passwords("PASSWORD") is True
        assert check_common_passwords("PaSsWoRd") is True
        assert check_common_passwords("QWERTY") is True


class TestPasswordScoring:
    """Test password strength scoring system."""

    def test_weak_password_low_score(self):
        """Test that weak passwords get low scores."""
        score = calculate_password_score("pass")
        assert score < 30

    def test_medium_password_medium_score(self):
        """Test that medium passwords get medium scores."""
        score = calculate_password_score("password123")
        assert 20 <= score <= 60

    def test_strong_password_high_score(self):
        """Test that strong passwords get high scores."""
        score = calculate_password_score("Serene2024!")
        assert score >= 70

    def test_very_strong_password_very_high_score(self):
        """Test that very strong passwords get very high scores."""
        score = calculate_password_score("MyV3ry$tr0ng&C0mpl3xP@ssw0rd!")
        assert score >= 85

    def test_score_increases_with_length(self):
        """Test that longer passwords get higher scores."""
        score_short = calculate_password_score("Pass123!")
        score_long = calculate_password_score("Pass123!ExtraChars")
        assert score_long > score_short

    def test_score_range(self):
        """Test that scores are always between 0 and 100."""
        passwords = ["a", "Pass123!", "Serene2024!", "MyV3ry$tr0ng&C0mpl3xP@ssw0rd!"]
        for password in passwords:
            score = calculate_password_score(password)
            assert 0 <= score <= 100


class TestPasswordFeedback:
    """Test password feedback generation."""

    def test_feedback_contains_score(self):
        """Test that feedback includes score."""
        feedback = get_password_feedback("Serene2024!")
        assert "score" in feedback
        assert isinstance(feedback["score"], int)

    def test_feedback_contains_strength_level(self):
        """Test that feedback includes strength level."""
        feedback = get_password_feedback("Serene2024!")
        assert "strength_level" in feedback
        assert feedback["strength_level"] in ["weak", "medium", "strong", "very_strong"]

    def test_feedback_contains_color(self):
        """Test that feedback includes color for UI."""
        feedback = get_password_feedback("Serene2024!")
        assert "color" in feedback
        assert feedback["color"] in ["red", "orange", "yellow", "green"]

    def test_feedback_contains_messages(self):
        """Test that feedback includes messages."""
        feedback = get_password_feedback("pass")
        assert "messages" in feedback
        assert isinstance(feedback["messages"], list)
        assert len(feedback["messages"]) > 0

    def test_feedback_weak_password(self):
        """Test feedback for weak password."""
        feedback = get_password_feedback("pass")
        assert feedback["strength_level"] == "weak"
        assert feedback["color"] == "red"

    def test_feedback_strong_password(self):
        """Test feedback for strong password."""
        feedback = get_password_feedback("Serene2024!")
        assert feedback["strength_level"] in ["strong", "very_strong"]
        assert feedback["color"] in ["yellow", "green"]

    def test_feedback_empty_messages_for_valid(self):
        """Test that valid passwords have no error messages."""
        feedback = get_password_feedback("Serene2024!")
        # Messages should be empty or contain only positive feedback
        assert len(feedback["messages"]) == 0 or all("✓" in msg for msg in feedback["messages"])


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_password_with_unicode(self):
        """Test password with unicode characters."""
        password = "Pâssw0rd!éà"
        is_valid, message = validate_password_strength(password)
        # Should handle unicode gracefully
        assert isinstance(is_valid, bool)

    def test_password_very_long(self):
        """Test very long password."""
        password = "A1!" + "x" * 100
        is_valid, message = validate_password_strength(password)
        assert is_valid is True

    def test_password_all_special_chars(self):
        """Test password that meets requirements with lots of special chars."""
        password = "P@ss123!#$%^&*()"
        is_valid, message = validate_password_strength(password)
        assert is_valid is True

    def test_score_consistency(self):
        """Test that scoring is consistent for same password."""
        password = "Serene2024!"
        score1 = calculate_password_score(password)
        score2 = calculate_password_score(password)
        assert score1 == score2

    def test_none_password(self):
        """Test handling of None as password."""
        with pytest.raises((TypeError, AttributeError)):
            validate_password_strength(None)


class TestIntegration:
    """Integration tests for complete validation flow."""

    def test_complete_validation_flow_valid(self):
        """Test complete validation flow with valid password."""
        password = "Serene2024!"

        # Check validation
        is_valid, message = validate_password_strength(password)
        assert is_valid is True

        # Check not common
        assert check_common_passwords(password) is False

        # Check score
        score = calculate_password_score(password)
        assert score >= 70

        # Check feedback
        feedback = get_password_feedback(password)
        assert feedback["strength_level"] in ["strong", "very_strong"]

    def test_complete_validation_flow_invalid(self):
        """Test complete validation flow with invalid password."""
        password = "password"

        # Check validation
        is_valid, message = validate_password_strength(password)
        assert is_valid is False

        # Check common
        assert check_common_passwords(password) is True

        # Check score
        score = calculate_password_score(password)
        assert score < 50

        # Check feedback
        feedback = get_password_feedback(password)
        assert feedback["strength_level"] in ["weak", "medium"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
