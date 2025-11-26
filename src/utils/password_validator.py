"""
Password validation and strength checking module.

Provides comprehensive password validation including:
- Length requirements (minimum 8 characters)
- Complexity requirements (uppercase, lowercase, digit, special character)
- Common password detection
- Password strength scoring
- User-friendly feedback generation
"""

import re
import os
from typing import Tuple, Dict, List


# Password requirements
MIN_PASSWORD_LENGTH = 8
SPECIAL_CHARACTERS = "@#$%^&+=!?*()-_[]{}|;:,.<>/~`"

# Path to common passwords file
COMMON_PASSWORDS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "assets", "common_passwords.txt"
)


def validate_password_strength(password: str) -> Tuple[bool, str]:
    """
    Validate password against all security requirements.

    Requirements:
    - Minimum 8 characters
    - At least 1 uppercase letter
    - At least 1 lowercase letter
    - At least 1 digit
    - At least 1 special character
    - Not in common passwords list

    Args:
        password: Password string to validate

    Returns:
        Tuple of (is_valid, message)
        - is_valid: True if password meets all requirements
        - message: Descriptive message about validation result
    """
    # Handle None or empty password
    if password is None:
        raise TypeError("Password cannot be None")

    if not password or not password.strip():
        return False, "Le mot de passe ne peut pas être vide"

    # Check minimum length
    if len(password) < MIN_PASSWORD_LENGTH:
        return False, f"Le mot de passe doit contenir au moins {MIN_PASSWORD_LENGTH} caractères"

    # Check for uppercase letter
    if not re.search(r'[A-Z]', password):
        return False, "Le mot de passe doit contenir au moins une majuscule"

    # Check for lowercase letter
    if not re.search(r'[a-z]', password):
        return False, "Le mot de passe doit contenir au moins une minuscule"

    # Check for digit
    if not re.search(r'\d', password):
        return False, "Le mot de passe doit contenir au moins un chiffre"

    # Check for special character
    if not re.search(f'[{re.escape(SPECIAL_CHARACTERS)}]', password):
        return False, f"Le mot de passe doit contenir au moins un caractère spécial ({SPECIAL_CHARACTERS})"

    # Check against common passwords
    if check_common_passwords(password):
        return False, "Ce mot de passe est trop courant et facilement devinable"

    return True, "Mot de passe valide"


def calculate_password_score(password: str) -> int:
    """
    Calculate password strength score (0-100).

    Scoring factors:
    - Length (up to 30 points)
    - Uppercase letters (up to 15 points)
    - Lowercase letters (up to 15 points)
    - Digits (up to 15 points)
    - Special characters (up to 20 points)
    - All requirements met bonus (up to 10 points)

    Args:
        password: Password string to score

    Returns:
        Integer score between 0 and 100
    """
    if not password:
        return 0

    score = 0

    # Length score (up to 30 points)
    # 8 chars = 15, 12 chars = 22, 16+ chars = 30
    length = len(password)
    if length >= 16:
        score += 30
    elif length >= 12:
        score += 22
    elif length >= 10:
        score += 18
    elif length >= 8:
        score += 15
    else:
        score += max(0, length * 1.5)

    # Uppercase letters (up to 15 points)
    uppercase_count = sum(1 for c in password if c.isupper())
    if uppercase_count > 0:
        score += min(15, 8 + uppercase_count * 2)

    # Lowercase letters (up to 15 points)
    lowercase_count = sum(1 for c in password if c.islower())
    if lowercase_count > 0:
        score += min(15, 8 + lowercase_count * 1.5)

    # Digits (up to 15 points)
    digit_count = sum(1 for c in password if c.isdigit())
    if digit_count > 0:
        score += min(15, 8 + digit_count * 2)

    # Special characters (up to 20 points)
    special_count = sum(1 for c in password if c in SPECIAL_CHARACTERS)
    if special_count > 0:
        score += min(20, 12 + special_count * 3)

    # Bonus for meeting all requirements (up to 10 points)
    has_all_requirements = (
        length >= MIN_PASSWORD_LENGTH and
        uppercase_count > 0 and
        lowercase_count > 0 and
        digit_count > 0 and
        special_count > 0 and
        not check_common_passwords(password)
    )
    if has_all_requirements:
        score += 10

    # Penalty for common passwords
    if check_common_passwords(password):
        score = min(score, 40)  # Cap at 40 if common

    # Ensure score is within bounds
    return max(0, min(100, score))


def check_common_passwords(password: str) -> bool:
    """
    Check if password is in the list of common passwords.

    The check is case-insensitive to catch variations like "PASSWORD" or "PaSsWoRd".

    Args:
        password: Password string to check

    Returns:
        True if password is in common passwords list, False otherwise
    """
    if not password:
        return False

    # Normalize to lowercase for comparison
    password_lower = password.lower()

    # Try to load common passwords from file
    try:
        if os.path.exists(COMMON_PASSWORDS_FILE):
            with open(COMMON_PASSWORDS_FILE, 'r', encoding='utf-8') as f:
                common_passwords = {line.strip().lower() for line in f if line.strip()}
                return password_lower in common_passwords
    except Exception:
        # If file doesn't exist or can't be read, fall back to basic list
        pass

    # Fallback: hardcoded list of most common passwords
    basic_common_passwords = {
        "123456", "password", "123456789", "12345678", "12345", "1234567",
        "password1", "123123", "1234567890", "qwerty", "abc123", "111111",
        "monkey", "dragon", "letmein", "baseball", "iloveyou", "trustno1",
        "1234", "sunshine", "master", "welcome", "shadow", "ashley",
        "football", "jesus", "michael", "ninja", "mustang", "password123",
        "qwerty123", "admin", "root", "pass", "test", "guest"
    }

    return password_lower in basic_common_passwords


def get_password_feedback(password: str) -> Dict[str, any]:
    """
    Generate comprehensive feedback for password strength.

    Provides:
    - Numerical score (0-100)
    - Strength level (weak/medium/strong/very_strong)
    - Color indicator for UI (red/orange/yellow/green)
    - List of specific improvement messages

    Args:
        password: Password string to analyze

    Returns:
        Dictionary with keys:
        - score: int (0-100)
        - strength_level: str
        - color: str
        - messages: List[str]
    """
    if not password:
        return {
            "score": 0,
            "strength_level": "weak",
            "color": "red",
            "messages": ["Le mot de passe ne peut pas être vide"]
        }

    score = calculate_password_score(password)
    messages = []

    # Check each requirement and build messages
    if len(password) < MIN_PASSWORD_LENGTH:
        messages.append(f"Trop court (minimum {MIN_PASSWORD_LENGTH} caractères)")

    if not re.search(r'[A-Z]', password):
        messages.append("Ajoutez au moins une majuscule")

    if not re.search(r'[a-z]', password):
        messages.append("Ajoutez au moins une minuscule")

    if not re.search(r'\d', password):
        messages.append("Ajoutez au moins un chiffre")

    if not re.search(f'[{re.escape(SPECIAL_CHARACTERS)}]', password):
        messages.append("Ajoutez au moins un caractère spécial")

    if check_common_passwords(password):
        messages.append("Ce mot de passe est trop courant")

    # Determine strength level and color
    if score >= 85:
        strength_level = "very_strong"
        color = "green"
        if not messages:
            messages = []  # No negative messages for very strong passwords
    elif score >= 70:
        strength_level = "strong"
        color = "yellow"
        if not messages:
            messages = []
    elif score >= 50:
        strength_level = "medium"
        color = "orange"
    else:
        strength_level = "weak"
        color = "red"

    return {
        "score": score,
        "strength_level": strength_level,
        "color": color,
        "messages": messages
    }


def get_password_strength_label(score: int) -> str:
    """
    Get human-readable strength label for a score.

    Args:
        score: Password score (0-100)

    Returns:
        French label: "Très faible", "Faible", "Moyen", "Fort", "Très fort"
    """
    if score >= 85:
        return "Très fort"
    elif score >= 70:
        return "Fort"
    elif score >= 50:
        return "Moyen"
    elif score >= 30:
        return "Faible"
    else:
        return "Très faible"


def get_password_requirements() -> List[str]:
    """
    Get list of password requirements for display to users.

    Returns:
        List of requirement strings
    """
    return [
        f"Au moins {MIN_PASSWORD_LENGTH} caractères",
        "Au moins une majuscule (A-Z)",
        "Au moins une minuscule (a-z)",
        "Au moins un chiffre (0-9)",
        f"Au moins un caractère spécial ({SPECIAL_CHARACTERS})",
        "Ne doit pas être un mot de passe courant"
    ]
