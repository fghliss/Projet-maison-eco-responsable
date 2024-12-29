#PARTIE 1.2:
#source en bas de la page



import sqlite3
import random
from datetime import datetime, timedelta

# ouverture/initialisation de la base de donnee
conn = sqlite3.connect('logement.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Fonction pour réinitialiser les tables
def reset_tables():
    print("Réinitialisation des tables...")
    tables = ['mesure', 'facture']  # Liste des tables à réinitialiser
    for table in tables:
        c.execute(f"DELETE FROM {table}")  # Supprimer toutes les lignes de chaque table
        c.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}'")  # Réinitialiser les IDs auto-incrémentés (optionnel)


# Fonction pour générer des dates aléatoires dans une plage donnée
def generate_random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

# Ajout de mesures pour les capteurs/actionneurs
def insert_measures():
    print("Ajout des mesures...")
    c.execute("SELECT id_capteur_actionneur FROM capt_actionneur WHERE type_device = 'capteur'")
    capteurs = c.fetchall()

    for capteur in capteurs:
        id_capteur = capteur['id_capteur_actionneur']
        for _ in range(2):  # Ajouter 2 mesures par capteur
            valeur = round(random.uniform(20.0, 30.0), 2)  # Valeurs aléatoires entre 20 et 30
            date_mesure = generate_random_date(datetime(2024, 1, 1), datetime(2024, 12, 31))
            c.execute("""
                INSERT INTO mesure (id_capteur_actionneur, valeur, date_insertion)
                VALUES (?, ?, ?)
            """, (id_capteur, valeur, date_mesure.strftime('%Y-%m-%d')))

# Ajout de factures pour les logements
def insert_factures():
    print("Ajout des factures...")
    c.execute("SELECT id_logement FROM logement")
    logements = c.fetchall()

    types_factures = ['eau', 'électricité', 'déchets']
    for logement in logements:
        id_logement = logement['id_logement']
        for _ in range(2):  # Ajouter 2 factures par logement
            type_facture = random.choice(types_factures)
            date_facture = generate_random_date(datetime(2024, 1, 1), datetime(2024, 12, 31))
            montant = round(random.uniform(50.0, 150.0), 2)  # Montant aléatoire entre 50 et 150
            valeur_consommation = round(random.uniform(100.0, 500.0), 2)  # Consommation aléatoire
            c.execute("""
                INSERT INTO facture (id_logement, type_facture, date_facture, montant, valeur_consommation)
                VALUES (?, ?, ?, ?, ?)
            """, (id_logement, type_facture, date_facture.strftime('%Y-%m-%d'), montant, valeur_consommation))

# Appel des fonctions pour remplir les données
reset_tables()
insert_measures()
insert_factures()

# fermeture
conn.commit()
conn.close()


#Sources : moodle / chatgpt