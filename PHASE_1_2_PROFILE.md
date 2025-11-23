# Phase 1.2 : Profil Utilisateur

## Vue d'ensemble

Implémentation complète de la gestion du profil utilisateur pour Serene, permettant aux utilisateurs de personnaliser leur expérience et d'exercer leurs droits RGPD.

## Fonctionnalités implémentées

### 1. Informations personnelles

**Localisation**: Page "Profil" > Onglet "Informations personnelles"

Permet aux utilisateurs de gérer leurs informations :
- **Email** (lecture seule)
- **Nom d'affichage** : nom utilisé dans l'application
- **Nom complet** : nom complet de l'utilisateur (optionnel)
- **Année de naissance** : pour personnaliser l'expérience (optionnel)
- **Zone géographique / Fuseau horaire** : pour les rappels personnalisés (optionnel)

### 2. Préférences

**Localisation**: Page "Profil" > Onglet "Préférences"

Personnalisation de l'expérience utilisateur :

#### Fréquence des rappels de check-in
- Quotidien (1x par jour)
- Bi-quotidien (2x par jour)
- Hebdomadaire
- Aucun rappel

#### Objectifs personnels
Zone de texte libre pour définir des objectifs de bien-être mental qui peuvent être utilisés pour personnaliser les insights IA.

#### Ton de conversation préféré
- Empathique (par défaut)
- Professionnel
- Décontracté
- Motivant

#### Fréquence des insights personnalisés
- Hebdomadaire
- Bi-hebdomadaire
- Mensuel

### 3. Sécurité

**Localisation**: Page "Profil" > Onglet "Sécurité"

Permet de changer le mot de passe :
- Vérification du mot de passe actuel
- Validation du nouveau mot de passe (minimum 6 caractères)
- Confirmation du nouveau mot de passe

### 4. Export des données (RGPD)

**Localisation**: Page "Profil" > Onglet "Données (RGPD)"

Export complet des données utilisateur au format JSON :
- Profil utilisateur (email, nom, préférences)
- Tous les check-ins d'humeur
- Toutes les conversations avec l'IA
- Tous les insights générés
- Horodatage de l'export

**Note** : Le mot de passe hashé est exclu de l'export pour des raisons de sécurité.

## Modifications de la base de données

### Schéma mis à jour (schema.sql)

Nouvelles colonnes ajoutées à la table `users` :
```sql
full_name TEXT,     -- Nom complet de l'utilisateur
birth_year INTEGER, -- Année de naissance
timezone TEXT,      -- Fuseau horaire / zone géographique
```

### Migration

Pour les bases de données existantes, utilisez le script de migration :
```bash
python migrate_db_profile.py
```

Le script :
- Vérifie les colonnes existantes
- Ajoute uniquement les colonnes manquantes
- Affiche un rapport détaillé de la migration

## Nouvelles méthodes DatabaseManager

### `update_user_profile()`
Met à jour les informations de profil de l'utilisateur.

```python
db.update_user_profile(
    user_id=1,
    display_name="John",
    full_name="John Doe",
    birth_year=1990,
    timezone="Europe/Paris"
)
```

### `export_user_data()`
Exporte toutes les données utilisateur pour la conformité RGPD.

```python
data = db.export_user_data(user_id=1)
# Retourne un dict avec: user_profile, check_ins, conversations, insights
```

## Structure des fichiers

```
mental-wellness/
├── src/
│   ├── database/
│   │   ├── schema.sql           # ✨ Mis à jour avec nouvelles colonnes
│   │   └── db_manager.py        # ✨ Nouvelles méthodes ajoutées
│   └── ui/
│       └── profile.py           # 🆕 Nouvelle page de profil
├── app.py                        # ✨ Navigation mise à jour
├── migrate_db_profile.py        # 🆕 Script de migration
└── PHASE_1_2_PROFILE.md         # 🆕 Cette documentation
```

## Navigation

La page "Profil" a été ajoutée au menu de navigation :
- Home
- Check-in
- Conversation
- Dashboard
- **Profil** 🆕

## Style

L'interface du profil suit le style "Gallery Minimalist" cohérent avec le reste de l'application :
- Typographie : Cormorant Garamond (titres) + Inter (texte)
- Palette de couleurs : Noir, gris, ivoire
- Navigation par onglets épurée
- Boutons et formulaires minimalistes

## Tests

Pour tester les nouvelles fonctionnalités :

1. Lancez l'application :
   ```bash
   streamlit run app.py
   ```

2. Connectez-vous ou créez un compte

3. Accédez à la page "Profil" dans le menu

4. Testez chaque onglet :
   - Modifier vos informations personnelles
   - Configurer vos préférences
   - Changer votre mot de passe
   - Exporter vos données

## Conformité RGPD

Cette implémentation respecte les principes RGPD :

- ✅ **Droit d'accès** : Les utilisateurs peuvent voir toutes leurs données
- ✅ **Droit de rectification** : Les utilisateurs peuvent modifier leurs données
- ✅ **Droit à la portabilité** : Export complet au format JSON
- ✅ **Transparence** : Information claire sur les données collectées
- ✅ **Sécurité** : Mot de passe hashé (SHA-256), données stockées localement

## Prochaines étapes

Phase 1 maintenant complète ! Prochaines phases suggérées :
- Phase 2 : Améliorations IA et personnalisation
- Phase 3 : Fonctionnalités sociales et communauté
- Phase 4 : Notifications et rappels
- Phase 5 : Analyses avancées et visualisations

---

**Date de complétion** : 2025-11-23
**Status** : ✅ Phase 1.2 - TERMINÉE
