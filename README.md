# Serene - Mental Wellness AI Companion

Un assistant IA bienveillant qui aide à prévenir le burnout et maintenir un bien-être mental optimal grâce à des check-ins réguliers, de l'écoute empathique, et des insights personnalisés.

## À propos

Serene est une application Streamlit développée avec Python et l'API Claude (Anthropic) pour offrir un accompagnement au bien-être mental, respectueux de la vie privée.

## Fonctionnalités

- 🌸 **Conversation Empathique** : Discutez avec un compagnon IA bienveillant
- 📊 **Quick Check-in** : Enregistrez votre humeur quotidienne
- 📈 **Dashboard** : Visualisez vos tendances de bien-être
- 💡 **AI Insights** : Recevez des insights personnalisés basés sur vos données
- 🔒 **Vie Privée** : Toutes les données sont stockées localement (SQLite)

## Technologies

- Python 3.11+
- Streamlit 1.40+
- Anthropic Claude API (claude-3-5-sonnet-20241022)
- SQLite
- Plotly

## Installation

```bash
# Cloner le repository
git clone https://github.com/zyed-zgueb/mental-wellness.git
cd mental-wellness

# Créer un environnement virtuel
python3.11 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env et ajouter votre ANTHROPIC_API_KEY

# Lancer l'application
streamlit run app.py
```

## Configuration

Créez un fichier `.env` à la racine du projet:

```bash
ANTHROPIC_API_KEY=votre_clé_api_ici
DATABASE_PATH=serene.db
```

## Statut du Projet

🚧 **En développement actif** - MVP en cours de construction (7 jours)

## Avertissement

⚠️ Serene est un compagnon IA, **pas un professionnel de santé mentale**. Il ne remplace pas une thérapie ou un traitement médical.

En cas de crise, contactez:
- **3114** : Numéro national de prévention du suicide (24/7)
- **15** : SAMU (urgences médicales)

## Licence

Projet de démonstration - Tous droits réservés
