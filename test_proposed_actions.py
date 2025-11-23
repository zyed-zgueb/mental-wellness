#!/usr/bin/env python3
"""
Script de test pour le système d'approbation des actions proposées.
"""

import sys
from src.database.db_manager import DatabaseManager


def test_proposed_actions_system():
    """Tester le système de propositions d'actions."""
    print("🧪 Test du système d'approbation des actions proposées\n")

    # Créer une base de données de test en mémoire
    print("1️⃣  Création de la base de données de test...")
    db = DatabaseManager(":memory:")
    print("✅ Base de données créée\n")

    # Utiliser un user_id fictif pour les tests
    print("2️⃣  Configuration de l'ID utilisateur de test...")
    user_id = 1  # ID fictif pour les tests
    print(f"✅ ID utilisateur de test: {user_id}\n")

    # Test 1: Créer une proposition d'action
    print("3️⃣  Test: Création d'une proposition d'action...")
    try:
        proposal_id = db.save_proposed_action(
            user_id=user_id,
            title="Méditer 10 minutes chaque matin",
            description="Commencer la journée par une méditation courte pour réduire le stress",
            conversation_id=None,
        )
        print(f"✅ Proposition créée (ID: {proposal_id})\n")
    except Exception as e:
        print(f"❌ Erreur: {e}\n")
        return False

    # Test 2: Récupérer les propositions en attente
    print("4️⃣  Test: Récupération des propositions en attente...")
    try:
        proposals = db.get_proposed_actions(user_id, status="pending")
        print(f"✅ {len(proposals)} proposition(s) en attente trouvée(s)")
        if proposals:
            print(f"   - Titre: {proposals[0]['title']}")
            print(f"   - Description: {proposals[0]['description']}")
            print(f"   - Statut: {proposals[0]['status']}\n")
    except Exception as e:
        print(f"❌ Erreur: {e}\n")
        return False

    # Test 3: Compter les propositions en attente
    print("5️⃣  Test: Comptage des propositions en attente...")
    try:
        count = db.get_proposed_actions_count(user_id, status="pending")
        print(f"✅ {count} proposition(s) en attente\n")
    except Exception as e:
        print(f"❌ Erreur: {e}\n")
        return False

    # Test 4: Accepter une proposition
    print("6️⃣  Test: Acceptation d'une proposition...")
    try:
        action_id = db.accept_proposed_action(proposal_id)
        print(f"✅ Proposition acceptée, action créée (ID: {action_id})")

        # Vérifier que l'action a été créée
        action = db.get_action_item_by_id(action_id)
        if action:
            print(f"   - Titre de l'action: {action['title']}")
            print(f"   - Source: {action['source']}")
            print(f"   - Statut: {action['status']}\n")

        # Vérifier que la proposition a été marquée comme acceptée
        updated_proposal = db.get_proposed_actions(user_id, status="accepted")
        if updated_proposal:
            print(f"✅ Proposition marquée comme acceptée\n")
    except Exception as e:
        print(f"❌ Erreur: {e}\n")
        return False

    # Test 5: Créer et rejeter une proposition
    print("7️⃣  Test: Création et rejet d'une proposition...")
    try:
        proposal_id_2 = db.save_proposed_action(
            user_id=user_id,
            title="Faire du yoga tous les soirs",
            description="Pratiquer 15 minutes de yoga avant de dormir",
        )
        print(f"✅ Proposition créée (ID: {proposal_id_2})")

        db.reject_proposed_action(proposal_id_2)
        print("✅ Proposition rejetée")

        # Vérifier le statut
        rejected = db.get_proposed_actions(user_id, status="rejected")
        if rejected:
            print(f"   - Proposition rejetée trouvée: {rejected[0]['title']}\n")
    except Exception as e:
        print(f"❌ Erreur: {e}\n")
        return False

    # Test 6: Vérifier qu'on ne peut pas accepter une proposition déjà traitée
    print("8️⃣  Test: Tentative d'acceptation d'une proposition déjà acceptée...")
    try:
        db.accept_proposed_action(proposal_id)
        print("❌ ERREUR: Devrait échouer pour une proposition déjà acceptée\n")
        return False
    except ValueError as e:
        print(f"✅ Erreur correctement levée: {e}\n")

    # Test 7: Supprimer une proposition
    print("9️⃣  Test: Suppression d'une proposition...")
    try:
        proposal_id_3 = db.save_proposed_action(
            user_id=user_id,
            title="Action à supprimer",
            description="Test de suppression",
        )
        db.delete_proposed_action(proposal_id_3)
        print("✅ Proposition supprimée avec succès\n")
    except Exception as e:
        print(f"❌ Erreur: {e}\n")
        return False

    print("=" * 60)
    print("✅ TOUS LES TESTS ONT RÉUSSI!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_proposed_actions_system()
    sys.exit(0 if success else 1)
