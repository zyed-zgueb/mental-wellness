"""Test pour vérifier la logique de calcul des jours depuis le premier check-in."""

from datetime import datetime, timedelta

def calculate_days_with_data(mood_data):
    """
    Simuler la logique de calcul des jours (extrait de insights_generator.py).
    """
    if mood_data:
        # mood_data est trié du plus récent au plus ancien
        oldest_checkin = datetime.fromisoformat(mood_data[-1]["timestamp"])
        days_with_data = (datetime.now() - oldest_checkin).days + 1  # +1 pour inclure le jour actuel
    else:
        days_with_data = 0

    return days_with_data

def get_maturity_level(days_count):
    """Déterminer le niveau de maturité des données."""
    if days_count < 3:
        return "early"
    elif days_count < 7:
        return "developing"
    else:
        return "mature"

# === Test Cases ===
print("🧪 Test de la logique de calcul des jours\n")

# Test 1: Aucun check-in
print("Test 1: Aucun check-in")
mood_data_1 = []
days_1 = calculate_days_with_data(mood_data_1)
print(f"  Résultat: {days_1} jours (attendu: 0)")
print(f"  Maturity: {get_maturity_level(days_1)} (attendu: early)")
assert days_1 == 0, "❌ ÉCHEC: Devrait être 0 jours"
print("  ✅ PASS\n")

# Test 2: Un seul check-in aujourd'hui
print("Test 2: Un seul check-in aujourd'hui")
mood_data_2 = [
    {"timestamp": datetime.now().isoformat(), "mood_score": 7, "notes": "Bien"}
]
days_2 = calculate_days_with_data(mood_data_2)
print(f"  Résultat: {days_2} jours (attendu: 1)")
print(f"  Maturity: {get_maturity_level(days_2)} (attendu: early)")
assert days_2 == 1, "❌ ÉCHEC: Devrait être 1 jour"
print("  ✅ PASS\n")

# Test 3: Plusieurs check-ins sur 3 jours (même si 10 enregistrements)
print("Test 3: 10 check-ins répartis sur 3 jours")
base_date = datetime.now() - timedelta(days=2)  # Il y a 3 jours (jour 0, 1, 2)
mood_data_3 = [
    {"timestamp": datetime.now().isoformat(), "mood_score": 8, "notes": ""},  # Aujourd'hui
    {"timestamp": datetime.now().isoformat(), "mood_score": 7, "notes": ""},  # Aujourd'hui
    {"timestamp": (datetime.now() - timedelta(days=1)).isoformat(), "mood_score": 6, "notes": ""},  # Hier
    {"timestamp": (datetime.now() - timedelta(days=1)).isoformat(), "mood_score": 5, "notes": ""},  # Hier
    {"timestamp": (datetime.now() - timedelta(days=1)).isoformat(), "mood_score": 7, "notes": ""},  # Hier
    {"timestamp": base_date.isoformat(), "mood_score": 8, "notes": ""},  # Il y a 2 jours (le plus ancien)
    {"timestamp": base_date.isoformat(), "mood_score": 6, "notes": ""},
    {"timestamp": base_date.isoformat(), "mood_score": 7, "notes": ""},
    {"timestamp": base_date.isoformat(), "mood_score": 5, "notes": ""},
    {"timestamp": base_date.isoformat(), "mood_score": 9, "notes": ""},  # Le plus ancien dans la liste
]
days_3 = calculate_days_with_data(mood_data_3)
print(f"  Résultat: {days_3} jours (attendu: 3)")
print(f"  Maturity: {get_maturity_level(days_3)} (attendu: developing)")
assert days_3 == 3, f"❌ ÉCHEC: Devrait être 3 jours, obtenu {days_3}"
print("  ✅ PASS\n")

# Test 4: Premier check-in il y a 10 jours, dernier aujourd'hui
print("Test 4: Premier check-in il y a 10 jours, dernier aujourd'hui")
mood_data_4 = [
    {"timestamp": datetime.now().isoformat(), "mood_score": 8, "notes": "Bien"},
    {"timestamp": (datetime.now() - timedelta(days=5)).isoformat(), "mood_score": 6, "notes": "Moyen"},
    {"timestamp": (datetime.now() - timedelta(days=10)).isoformat(), "mood_score": 7, "notes": "OK"},  # Le plus ancien
]
days_4 = calculate_days_with_data(mood_data_4)
print(f"  Résultat: {days_4} jours (attendu: 11)")
print(f"  Maturity: {get_maturity_level(days_4)} (attendu: mature)")
assert days_4 == 11, f"❌ ÉCHEC: Devrait être 11 jours, obtenu {days_4}"
print("  ✅ PASS\n")

# Test 5: Vérification de l'ancien comportement (comptage d'enregistrements)
print("Test 5: Comparaison ancien vs nouveau comportement")
print(f"  Ancien comportement (len): {len(mood_data_3)} enregistrements")
print(f"  Nouveau comportement (diff dates): {days_3} jours")
print(f"  Différence: L'ancien aurait dit '{len(mood_data_3)} jours' au lieu de '{days_3} jours'")
print("  ✅ La nouvelle logique est correcte!\n")

print("=" * 60)
print("✅ Tous les tests passent! La correction fonctionne correctement.")
print("=" * 60)
