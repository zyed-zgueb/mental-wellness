# Phase 2.1 : Suivi Contextuel & Mémoire de l'IA - Goals & Actions

## Vue d'ensemble

Cette phase implémente un système de suivi d'objectifs et d'actions pour l'application Serene. Le système permet de :
- Capturer automatiquement les objectifs et intentions mentionnés pendant les conversations
- Suivre manuellement des actions de bien-être
- Gérer le statut des actions (en attente, en cours, complété, abandonné)
- Visualiser les progrès et statistiques

## Architecture

### 1. Base de données

#### Table `action_items`

```sql
CREATE TABLE IF NOT EXISTS action_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'in_progress', 'completed', 'abandoned')),
    source TEXT DEFAULT 'manual',  -- 'manual' ou 'ai_extracted'
    conversation_id INTEGER,  -- Référence à la conversation d'origine si extrait par l'IA
    deadline DATETIME,  -- Date limite optionnelle
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE SET NULL
);
```

**Indexes créés :**
- `idx_action_items_user_id` : Pour les requêtes par utilisateur
- `idx_action_items_status` : Pour filtrer par statut
- `idx_action_items_created_at` : Pour trier par date de création

### 2. Backend (DatabaseManager)

**Fichier :** `src/database/db_manager.py`

#### Méthodes ajoutées :

```python
def save_action_item(user_id, title, description="", source="manual",
                     conversation_id=None, deadline=None) -> int
```
Crée une nouvelle action.

```python
def get_action_items(user_id, status=None, limit=100) -> List[Dict]
```
Récupère les actions d'un utilisateur avec filtrage optionnel par statut.

```python
def update_action_item(action_id, title=None, description=None,
                       status=None, deadline=None) -> None
```
Met à jour une action existante. Gère automatiquement `completed_at` lors du changement de statut.

```python
def delete_action_item(action_id) -> None
```
Supprime une action.

```python
def get_action_item_by_id(action_id) -> Optional[Dict]
```
Récupère une action par son ID.

```python
def get_action_items_stats(user_id) -> Dict[str, int]
```
Retourne les statistiques (nombre d'actions par statut).

#### Export de données (RGPD)

La méthode `export_user_data()` a été mise à jour pour inclure les `action_items`.

### 3. Extraction automatique par IA

**Fichier :** `src/llm/action_extractor.py`

#### Classe `ActionExtractor`

```python
class ActionExtractor:
    def __init__(self, db_manager: DatabaseManager)

    def extract_actions_from_message(user_message: str, user_id: int,
                                     conversation_id: Optional[int]) -> List[Dict]
```

**Fonctionnement :**
1. Analyse le message utilisateur avec Claude API
2. Utilise un prompt spécialisé (`ACTION_EXTRACTION_PROMPT`)
3. Extrait les intentions actionnables (format JSON)
4. Sauvegarde automatiquement dans la base de données
5. Retourne la liste des actions extraites

#### Prompt d'extraction (`src/utils/prompts.py`)

Le prompt `ACTION_EXTRACTION_PROMPT` est configuré pour :
- Détecter les verbes d'action future ("je vais", "je veux", "j'ai décidé", etc.)
- Identifier les habitudes à développer (méditation, sport, etc.)
- Capturer les actions relationnelles
- Ignorer les réflexions vagues ou négatives

**Format de réponse attendu :**
```json
{
  "actions": [
    {
      "title": "Méditer 10 minutes chaque matin",
      "description": "Commencer par une simple respiration consciente"
    }
  ]
}
```

### 4. Intégration avec les conversations

**Fichier :** `src/llm/conversation_manager.py`

**Modifications :**
- Ajout du paramètre `enable_action_extraction: bool = True`
- Lazy loading de l'`ActionExtractor` pour éviter les imports circulaires
- Après chaque conversation sauvegardée, extraction automatique des actions
- Gestion d'erreur robuste (l'échec d'extraction n'affecte pas la conversation)

```python
# Extraire les actions automatiquement
if self.enable_action_extraction and self.action_extractor:
    try:
        self.action_extractor.extract_actions_from_message(
            user_message, user_id, conversation_id
        )
    except Exception as e:
        print(f"Erreur extraction d'actions: {e}")
```

### 5. Interface utilisateur

**Fichier :** `src/ui/action_items.py`

#### Page "Mes Objectifs & Actions"

**Fonctionnalités :**

1. **Statistiques** : Affichage du nombre total, à faire, en cours, complétés
2. **Formulaire de création manuelle** :
   - Titre (requis)
   - Description (optionnel)
   - Échéance (optionnel)
3. **Filtrage** : Par statut (toutes, à faire, en cours, complétées, abandonnées)
4. **Cartes d'actions** :
   - Badge de statut (couleur selon état)
   - Badge "Détecté par l'IA" pour les actions extraites automatiquement
   - Dates (création, échéance, complétion)
   - Description si disponible
5. **Actions rapides** :
   - ✓ Marquer comme complété
   - ▶ Commencer (passage en "en cours")
   - ✕ Abandonner
   - 🗑 Supprimer

**Design :**
- Cohérent avec le style Gallery Minimalist de Serene
- Utilisation de la palette de couleurs définie dans `serene_styles.py`
- Animations subtiles au survol
- État vide avec instructions claires

#### Navigation

**Fichier :** `app.py`

- Ajout de l'import `from src.ui.action_items import show_action_items`
- Nouvelle entrée dans le menu : "Mes Actions"
- Routage vers `show_action_items()` quand sélectionné
- Ajout d'une carte sur la page d'accueil présentant la fonctionnalité

### 6. Migration de base de données

**Fichier :** `migrate_db_action_items.py`

Script de migration pour créer la table `action_items` et ses indexes dans une base de données existante.

**Usage :**
```bash
python3 migrate_db_action_items.py [chemin_db]
```

**Note :** Si la base de données n'existe pas encore, la table sera créée automatiquement au premier lancement via `schema.sql`.

## Flux utilisateur

### Scénario 1 : Extraction automatique

1. L'utilisateur a une conversation : "Je vais essayer de méditer 10 minutes chaque matin"
2. `ConversationManager.send_message()` sauvegarde la conversation
3. `ActionExtractor.extract_actions_from_message()` est appelé
4. Claude analyse le message et extrait : `{"title": "Méditer 10 minutes chaque matin"}`
5. L'action est sauvegardée avec `source='ai_extracted'`
6. L'utilisateur peut ensuite la voir dans "Mes Actions" avec le badge "✨ Détecté par l'IA"

### Scénario 2 : Création manuelle

1. L'utilisateur va dans "Mes Actions"
2. Remplit le formulaire avec titre, description, échéance
3. Clique sur "Ajouter l'action"
4. L'action est créée avec `source='manual'`
5. Elle apparaît immédiatement dans la liste

### Scénario 3 : Gestion d'actions

1. L'utilisateur voit ses actions filtrées par statut
2. Clique sur "▶ Commencer" pour une action → `status='in_progress'`
3. Plus tard, clique sur "✓ Marquer comme complété" → `status='completed'`, `completed_at=now()`
4. Peut également abandonner ou supprimer

## Fichiers modifiés/créés

### Créés
- `src/llm/action_extractor.py` : Extraction automatique d'actions
- `src/ui/action_items.py` : Interface de gestion
- `migrate_db_action_items.py` : Script de migration
- `PHASE_2_1_ACTION_ITEMS.md` : Cette documentation

### Modifiés
- `src/database/schema.sql` : Ajout de la table `action_items`
- `src/database/db_manager.py` : Méthodes CRUD + export RGPD
- `src/llm/conversation_manager.py` : Intégration extraction automatique
- `src/utils/prompts.py` : Ajout du prompt `ACTION_EXTRACTION_PROMPT`
- `app.py` : Navigation + page d'accueil

## Tests recommandés

1. **Test extraction automatique** :
   - Conversations avec intentions claires ("je vais...", "j'ai décidé de...")
   - Vérifier que les actions sont extraites et sauvegardées
   - Vérifier le badge "Détecté par l'IA"

2. **Test création manuelle** :
   - Créer action avec tous les champs
   - Créer action avec seulement titre
   - Vérifier validation (titre requis)

3. **Test gestion de statuts** :
   - Commencer une action → vérifier `status='in_progress'`
   - Compléter une action → vérifier `completed_at`
   - Abandonner une action
   - Filtrer par statut

4. **Test statistiques** :
   - Vérifier les compteurs après création/modification

5. **Test export RGPD** :
   - Exporter les données utilisateur
   - Vérifier présence des `action_items`

## Améliorations futures possibles

1. **Rappels** : Notifications pour actions avec échéance proche
2. **Récurrence** : Actions répétitives (quotidien, hebdomadaire)
3. **Catégories** : Grouper par thème (santé, social, travail)
4. **Graphiques** : Visualisation de complétion au fil du temps
5. **Partage** : Exporter actions vers calendrier externe
6. **Suggestions IA** : Recommandations d'actions basées sur insights

## Notes techniques

- **Gestion d'erreurs** : L'échec d'extraction ne bloque jamais la conversation
- **Performance** : Indexes optimisés pour requêtes fréquentes
- **RGPD** : Cascade DELETE sur `user_id`, SET NULL sur `conversation_id`
- **Validation** : CHECK constraint sur `status` dans la base de données
- **Timestamps** : Automatiques via DEFAULT CURRENT_TIMESTAMP
