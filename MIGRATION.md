# Migration du schéma de base de données

## Changement du range de mood_score : 1-10 → 0-10

Si vous avez une base de données existante (`serene.db`), vous devez migrer le schéma pour permettre des valeurs de `mood_score` entre 0 et 10.

### Pour les utilisateurs avec une base existante

Exécutez le script de migration :

```bash
python migrate_mood_score_range.py
```

Ou spécifiez un chemin personnalisé :

```bash
python migrate_mood_score_range.py /chemin/vers/votre/base.db
```

### Pour les nouvelles installations

Rien à faire ! Le nouveau schéma sera automatiquement appliqué lors de la création de la base de données.

### Alternative simple (développement uniquement)

Si vous êtes en développement et que vous n'avez pas de données importantes, vous pouvez simplement supprimer la base existante :

```bash
rm serene.db
```

La base sera recréée automatiquement avec le nouveau schéma au prochain lancement de l'application.

### Ce que fait la migration

Le script :
1. Vérifie si la migration est nécessaire
2. Crée une nouvelle table `check_ins` avec la contrainte `CHECK(mood_score BETWEEN 0 AND 10)`
3. Copie toutes les données existantes
4. Supprime l'ancienne table
5. Renomme la nouvelle table
6. Recrée les index

### Sécurité

- Le script utilise une transaction SQLite
- En cas d'erreur, toutes les modifications sont annulées (rollback)
- Les données existantes ne sont jamais perdues
