# 🔒 Security Policy - Serene

**Last Updated:** November 2025
**Version:** 1.0.0

## Overview

Serene is a mental wellness application that handles sensitive personal data including mood tracking, AI conversations, and personal insights. Security and privacy are paramount. This document outlines the security measures implemented to protect user data.

---

## 🛡️ Security Measures Implemented

### 1. Password Security

#### 1.1 Strong Password Requirements

All user passwords must meet the following criteria:

- **Minimum Length:** 8 characters (upgraded from 6)
- **Complexity Requirements:**
  - At least 1 uppercase letter (A-Z)
  - At least 1 lowercase letter (a-z)
  - At least 1 digit (0-9)
  - At least 1 special character (@#$%^&+=!?*()-_[]{}|;:,.<>/~`)

#### 1.2 Common Password Detection

Serene blocks **1000+ common passwords** including:
- `123456`, `password`, `qwerty`, `abc123`
- `password123`, `admin`, `letmein`, `welcome`
- All variations are case-insensitive

This prevents users from choosing easily guessable passwords that are vulnerable to dictionary attacks.

#### 1.3 Password Strength Scoring

Real-time password strength feedback with scoring (0-100):
- **0-30:** Very weak (rejected)
- **30-50:** Weak (rejected)
- **50-70:** Medium (rejected)
- **70-85:** Strong (✅ accepted)
- **85-100:** Very strong (✅ accepted)

Users receive clear, actionable feedback:
- ❌ "Trop court (minimum 8 caractères)"
- ❌ "Ajoutez au moins une majuscule"
- ❌ "Ce mot de passe est trop courant"
- ✅ "Mot de passe valide"

#### 1.4 Implementation

- **Module:** `src/utils/password_validator.py`
- **Blacklist:** `src/assets/common_passwords.txt`
- **UI Integration:**
  - Signup form (`src/ui/auth.py`)
  - Password change (`src/ui/profile.py`)
- **Tests:** `tests/test_password_validator.py` (36 tests, all passing ✅)

---

### 2. Session Timeout & Auto-Logout

#### 2.1 Automatic Logout After Inactivity

To prevent unauthorized access on abandoned sessions, Serene automatically logs out users after a period of inactivity.

**Default Configuration:**
- **Timeout:** 30 minutes of inactivity
- **Warning:** 2 minutes before expiration

#### 2.2 Activity Tracking

The system tracks user activity and updates the `last_activity_time` on:
- Page navigation
- Form submissions
- Button clicks
- Any user interaction with the application

#### 2.3 Warning System

**2 minutes before timeout**, users see:
- ⚠️ Warning notification with countdown
- 🔄 "Extend Session" button to reset the timer
- Clear expiration time remaining

**On timeout expiration:**
- ⏱️ User is automatically logged out
- All session data cleared (user_id, email, authentication status)
- Clear message explaining the auto-logout
- User must log in again to continue

#### 2.4 Configuration

Configurable via environment variables in `.env`:

```bash
# Session timeout in minutes (default: 30)
SESSION_TIMEOUT_MINUTES=30

# Warning time in minutes before expiration (default: 2)
SESSION_WARNING_MINUTES=2
```

**Examples:**
- High security environment: `SESSION_TIMEOUT_MINUTES=15`
- Low risk environment: `SESSION_TIMEOUT_MINUTES=60`
- No warning: `SESSION_WARNING_MINUTES=0`

#### 2.5 Implementation

- **Module:** `src/ui/auth.py` (session timeout functions)
- **Integration:** `app.py` (called on every page render)
- **Configuration:** `.env.example`
- **Tests:** `tests/test_session_timeout.py` (20 tests)

---

## 🔐 Additional Security Practices

### 3. Password Hashing

⚠️ **IMPORTANT:** The current implementation uses **SHA-256 hashing without salt**, which is **NOT secure** for password storage in production.

**Recommended Upgrade (Future):**
- Migrate to **bcrypt** or **argon2** with proper salting
- Implement password stretching (multiple rounds)
- Add per-user unique salts

### 4. Data Privacy

**Local-Only Storage:**
- All data stored locally in SQLite database (`serene.db`)
- No cloud storage by default
- User has full control over their data

**Data Minimization:**
- Only essential data is collected
- No third-party analytics or tracking
- Anthropic Claude API used for AI features (subject to Anthropic's privacy policy)

**GDPR Compliance:**
- User data export functionality (`Profile > Export données`)
- Right to be forgotten (users can delete accounts)
- Transparent data usage

### 5. Environment Variables

Sensitive configuration stored in `.env` (excluded from Git):

```bash
# Critical - Never commit this file
ANTHROPIC_API_KEY=your_api_key_here
DATABASE_PATH=serene.db
SESSION_TIMEOUT_MINUTES=30
```

**`.gitignore` Protection:**
```
.env
.env.local
*.db
*.backup
```

### 6. SQL Injection Protection

**Parameterized Queries:**
All database operations use parameterized queries:

```python
# Safe - parameterized
cursor.execute("SELECT * FROM users WHERE email = ?", (email,))

# Unsafe - NEVER do this
cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")
```

**Foreign Key Constraints:**
- Referential integrity enforced at database level
- CASCADE and SET NULL rules for data consistency

---

## 🚨 Known Limitations & Future Improvements

### Current Limitations

1. **Password Hashing:** SHA-256 without salt (vulnerable to rainbow tables)
2. **Database Encryption:** SQLite database stored in **plaintext** on filesystem
3. **No Rate Limiting:** Login attempts not limited (vulnerable to brute force)
4. **No 2FA/MFA:** Single-factor authentication only
5. **No Account Lockout:** No temporary account lockout after failed logins
6. **Session Tokens:** No JWT or refresh tokens (browser-only sessions)

### Recommended Future Enhancements

#### High Priority
- [ ] **Upgrade Password Hashing** to bcrypt/argon2 with salt
- [ ] **SQLite Encryption** with SQLCipher/pysqlcipher3
- [ ] **Rate Limiting** on login/signup endpoints
- [ ] **Account Lockout** after N failed login attempts (e.g., 5 attempts)

#### Medium Priority
- [ ] **Password History** (prevent password reuse)
- [ ] **Email Verification** on signup
- [ ] **Password Reset** functionality (forgot password)
- [ ] **Audit Logging** for security events (login, logout, password changes)
- [ ] **HTTPS Enforcement** in production deployments

#### Low Priority
- [ ] **Two-Factor Authentication** (TOTP, SMS)
- [ ] **Session Management Dashboard** (view active sessions)
- [ ] **IP Allowlist/Blocklist**
- [ ] **Security Headers** (CSP, X-Frame-Options, etc.)

---

## 📋 Security Best Practices for Users

### For Users

1. **Use a Strong Password**
   - Minimum 12 characters recommended
   - Mix uppercase, lowercase, numbers, and symbols
   - Avoid personal information (birthdate, pet names)
   - Use a password manager (1Password, Bitwarden, etc.)

2. **Enable Session Timeout**
   - Keep default 30-minute timeout
   - Manually log out on shared devices
   - Never save password in browser on shared computers

3. **Keep Browser Updated**
   - Use latest version of Chrome, Firefox, or Edge
   - Enable automatic browser updates

4. **Protect Your `.env` File**
   - Never share your ANTHROPIC_API_KEY
   - Keep `.env` file secure (file permissions 600)

### For Developers

1. **Environment Setup**
   ```bash
   # Never commit .env to version control
   cp .env.example .env
   chmod 600 .env

   # Add to .gitignore
   echo ".env" >> .gitignore
   ```

2. **Testing Security**
   ```bash
   # Run password validation tests
   pytest tests/test_password_validator.py -v

   # Run session timeout tests
   pytest tests/test_session_timeout.py -v
   ```

3. **Code Review Checklist**
   - [ ] No hardcoded passwords or API keys
   - [ ] All database queries use parameterized statements
   - [ ] User input properly validated and sanitized
   - [ ] Sensitive data not logged to console
   - [ ] Password validation enforced on all password changes

---

## 🐛 Reporting Security Vulnerabilities

If you discover a security vulnerability in Serene, please report it responsibly:

1. **Do NOT** open a public GitHub issue
2. **Do NOT** disclose the vulnerability publicly until patched
3. **Contact:** [Create a private security advisory on GitHub]

### What to Include

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Response Timeline

- **24 hours:** Acknowledgment of report
- **7 days:** Initial assessment and severity classification
- **30 days:** Patch development and testing
- **60 days:** Public disclosure (coordinated with reporter)

---

## 📚 References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [NIST Password Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)
- [GDPR Compliance](https://gdpr.eu/)
- [Anthropic Privacy Policy](https://www.anthropic.com/privacy)
- [SQLite Security Best Practices](https://www.sqlite.org/security.html)

---

## 📝 Changelog

### Version 1.0.0 (November 2025)

**Added:**
- ✅ Strong password requirements (8+ characters, complexity)
- ✅ Common password detection (1000+ blacklist)
- ✅ Password strength scoring and feedback
- ✅ Session timeout with auto-logout (30 minutes)
- ✅ Session expiration warning (2 minutes before)
- ✅ Configurable timeout via environment variables
- ✅ Comprehensive test suite (56 tests total)

**Security Status:**
- Password validation: ✅ Production-ready
- Session timeout: ✅ Production-ready
- Password hashing: ⚠️ Needs upgrade (SHA-256 → bcrypt)
- Database encryption: ❌ Not implemented
- Rate limiting: ❌ Not implemented

---

**For questions or concerns, contact the development team.**
