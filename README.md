# Serene - Mental Wellness AI Companion

Application de bien-être mental qui aide à prévenir le burnout et maintenir un équilibre optimal grâce à des check-ins réguliers, de l'écoute empathique, et des insights personnalisés.

## À propos

Serene est une application Streamlit développée avec Python pour offrir un accompagnement au bien-être mental, respectueux de la vie privée avec stockage local des données.

## Fonctionnalités

**Actuellement disponible (Story 1.1) :**
- Interface de base avec navigation
- Écran de disclaimer avec ressources d'urgence

**En développement :**
- **Quick Check-in** (Story 1.2) : Enregistrement de l'humeur quotidienne
- **Conversation Empathique** (Story 1.3) : Discussion avec un compagnon IA
- **Dashboard** (Story 1.4) : Visualisation des tendances de bien-être
- **Insights** (Story 1.4) : Analyses personnalisées basées sur les données

## Technologies

**Actuellement utilisées :**
- Python 3.11+
- Streamlit 1.40+

**À venir :**
- Anthropic Claude API (Story 1.3)
- SQLite (Story 1.2)
- Plotly (Story 1.4)

## Installation

### Story 1.1 (Version actuelle)

```bash
# Cloner le repository
git clone https://github.com/zyed-zgueb/mental-wellness.git
cd mental-wellness

# Créer un environnement virtuel
python3.11 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer pip-tools (si pas déjà installé)
pip install pip-tools

# Compiler les dépendances depuis requirements.in
pip-compile requirements.in

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run app.py
```

L'application sera accessible sur `http://localhost:8501`

### Gestion des dépendances

Ce projet utilise `pip-tools` pour gérer les dépendances Python de manière déterministe.

**Fichiers :**
- `requirements.in` : Liste des dépendances directes (à éditer manuellement)
- `requirements.txt` : Fichier généré avec toutes les dépendances (avec versions fixées)

**Ajouter une nouvelle dépendance :**

```bash
# 1. Ajouter la dépendance dans requirements.in
echo "nouvelle-package" >> requirements.in

# 2. Recompiler requirements.txt
pip-compile requirements.in

# 3. Installer les nouvelles dépendances
pip install -r requirements.txt
```

**Mettre à jour les dépendances :**

```bash
# Mettre à jour toutes les dépendances
pip-compile --upgrade requirements.in

# Mettre à jour une dépendance spécifique
pip-compile --upgrade-package streamlit requirements.in
```

### Configuration (pour stories futures)

À partir de Story 1.3, vous devrez configurer les variables d'environnement :

```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer .env et ajouter votre clé API Anthropic
# ANTHROPIC_API_KEY=votre_clé_api_ici
```

## Statut du Projet

**En développement actif** - MVP en cours de construction (7 jours)

**Avancement :**
- Story 1.1 (Foundation + Disclaimers) : Terminée
- Story 1.2 (Quick Check-in + Database) : À venir
- Story 1.3 (Conversation) : À venir
- Story 1.4 (Dashboard + Insights) : À venir

## Avertissement

Serene est un compagnon IA, **pas un professionnel de santé mentale**. Il ne remplace pas une thérapie ou un traitement médical.

En cas de crise, contactez :
- **3114** : Numéro national de prévention du suicide (24/7)
- **15** : SAMU (urgences médicales)

## Licence

Projet de démonstration - Tous droits réservés
