"""Script pour vérifier le nombre réel de jours de données."""

from datetime import datetime
from src.database.db_manager import DatabaseManager

db = DatabaseManager("serene.db")

# Récupérer l'utilisateur (supposons user_id=1 pour le moment)
user_id = 1
mood_data = db.get_mood_history(user_id, days=365)  # Récupérer toutes les données

print("=" * 60)
print("ANALYSE DES DONNÉES UTILISATEUR")
print("=" * 60)

if mood_data:
    print(f"\n📊 Nombre d'enregistrements de check-ins: {len(mood_data)}")

    # Calculer le nombre de jours réels (nouvelle logique)
    oldest_checkin = datetime.fromisoformat(mood_data[-1]["timestamp"])
    newest_checkin = datetime.fromisoformat(mood_data[0]["timestamp"])
    days_with_data = (datetime.now() - oldest_checkin).days + 1

    print(f"📅 Premier check-in: {oldest_checkin.strftime('%d/%m/%Y à %H:%M')}")
    print(f"📅 Dernier check-in: {newest_checkin.strftime('%d/%m/%Y à %H:%M')}")
    print(f"⏱️  Nombre de JOURS RÉELS depuis le début: {days_with_data}")

    # Ancienne logique (pour comparaison)
    print(f"\n❌ Ancienne logique (len): {len(mood_data)} jours")
    print(f"✅ Nouvelle logique (diff dates): {days_with_data} jours")

    # Vérifier l'insight en cache
    print("\n" + "=" * 60)
    print("INSIGHT EN CACHE")
    print("=" * 60)

    latest_insight = db.get_latest_insight(user_id, "weekly")
    if latest_insight:
        import json
        created_at = datetime.fromisoformat(latest_insight["created_at"])
        metadata = json.loads(latest_insight["based_on_data"])

        print(f"\n📝 Insight généré le: {created_at.strftime('%d/%m/%Y à %H:%M')}")
        print(f"📊 Days_count dans l'insight en cache: {metadata.get('days_count', 'N/A')}")
        print(f"🏷️  Maturity level: {metadata.get('maturity_level', 'N/A')}")

        age_hours = (datetime.now() - created_at).total_seconds() / 3600
        print(f"⏱️  Âge de l'insight: {age_hours:.1f} heures")

        if metadata.get('days_count') != days_with_data:
            print(f"\n⚠️  PROBLÈME DÉTECTÉ!")
            print(f"   L'insight en cache utilise {metadata.get('days_count')} jours")
            print(f"   Mais tu as réellement {days_with_data} jours de données")
            print(f"\n💡 Solution: Supprime l'insight en cache pour forcer la régénération")
    else:
        print("\nℹ️  Aucun insight en cache trouvé")
else:
    print("\nℹ️  Aucun check-in trouvé pour cet utilisateur")

print("\n" + "=" * 60)
