# Projet-maison-eco-responsable

# Projet : Gestion de Consommation des Logements

## Description
Ce projet consiste en la conception et le développement d'une application web IoT éco-responsable. L'application permet aux utilisateurs de visualiser et de gérer leur consommation en électricité, eau, et déchets. Elle intègre également des capteurs et actionneurs, offrant des informations en temps réel sur leur état, leur configuration, et les économies réalisées grâce à l'optimisation des ressources.

Le projet est structuré autour d'une base de données SQLite (`logement.db`) et comprend des scripts SQL et Python pour la gestion et l'insertion des données.


## PARTIE 1: 
## fichiers concernés : logement.sql / remplissage.py / logement.db

## Structure des Fichiers

### 1. `logement.sql`
Ce fichier contient les scripts SQL nécessaires à :
- La création des tables de la base de données.
- L'insertion des données initiales dans les tables.
- La définition des relations entre les différentes entités.

#### Contenu principal :
- **Tables créées :**
  - `logement`
  - `Piece`
  - `capt_actionneur`
  - `mesure`
  - `Type_capt_act`
  - `facture`

- **Exemple de requêtes :**
```sql
-- Suppression et création de la table logement
DROP TABLE IF EXISTS logement; 
CREATE TABLE logement (
    id_logement INTEGER PRIMARY KEY AUTOINCREMENT,
    adresse TEXT NOT NULL,
    nombre_piece INTEGER,
    surface REAL,
    num_telephone TEXT,
    adresse_ip TEXT,
    consommation_electricite REAL,  
    consommation_eau REAL,         
    consommation_dechets REAL,
    date_insert DATE DEFAULT CURRENT_DATE
);

-- Insertion d'exemples de logements
INSERT INTO logement (adresse, nombre_piece, surface, num_telephone, adresse_ip, consommation_electricite, consommation_eau, consommation_dechets)
VALUES ('45 rue louise michel', 4, 100, '0123456789', '192.168.1.1', 500, 10, 50);
```

### 2. `remplissage.py`
Ce fichier Python permet de remplir dynamiquement la base de données avec des mesures et des factures aléatoires, en utilisant la bibliothèque `sqlite3`.

#### Fonctionnalités :
- Réinitialisation des tables `mesure` et `facture`.
- Insertion aléatoire de mesures pour les capteurs/actionneurs.
- Génération aléatoire de factures pour les logements.

#### Exemple de code :
```python
# Ajout de mesures pour les capteurs/actionneurs
def insert_measures():
    print("Ajout des mesures...")
    c.execute("SELECT id_capteur_actionneur FROM capt_actionneur WHERE type_device = 'capteur'")
    capteurs = c.fetchall()

    for capteur in capteurs:
        id_capteur = capteur['id_capteur_actionneur']
        for _ in range(2):
            valeur = round(random.uniform(20.0, 30.0), 2)  # Valeurs aléatoires
            date_mesure = generate_random_date(datetime(2024, 1, 1), datetime(2024, 12, 31))
            c.execute("""
                INSERT INTO mesure (id_capteur_actionneur, valeur, date_insertion)
                VALUES (?, ?, ?)
            """, (id_capteur, valeur, date_mesure.strftime('%Y-%m-%d')))
```

### 3. `logement.db`
Ce fichier SQLite est généré après l'exécution des scripts SQL et contient toutes les données nécessaires pour exécuter le projet. 

#### Création du fichier :
Pour générer la base de données, utilisez la commande suivante dans le terminal :
```bash
sqlite3 logement.db < logement.sql
```

## Prérequis
- Python 3.8 ou supérieur
- SQLite3
- Bibliothèques Python :
  - `sqlite3`
  - `random`
  - `datetime`

## Installation
1. Placez-vous dans le répertoire du projet :
   ```bash
   cd votre-projet
   ```
2. Exécutez le script SQL pour créer la base de données :
   ```bash
   sqlite3 logement.db < logement.sql
   ```
3. Remplissez la base de données avec des données aléatoires :
   ```bash
   python remplissage.py
   ```

## Sources
- ChatGPT (assisté pour la génération des scripts SQL et Python).
- Moodle (références pédagogiques).



----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## PARTIE 2:
## fichiers concernés : serveur_partie2.py / capt_temp.ino

### Structure des Fichiers

### 1. `serveur_partie2.py`
Ce fichier Python contient les fonctionnalités suivantes :
- **Remplissage automatique de la base de données :**
  - Le script connecte les données externes à la base SQLite existante (`logement.db`).
- **Création d'une page web affichant un camembert :**
  - Les données des factures (électricité, eau, déchets) sont extraites de la base de données et représentées graphiquement sous forme de camembert en utilisant la bibliothèque Matplotlib.
- **Création d'une page web affichant la météo :**
  - Une API météo (par exemple OpenWeatherMap) est utilisée pour afficher des informations météorologiques en temps réel.

#### Fonctionnement :
1. Créez un environnement virtuel Python et installez les dépendances nécessaires :
   ```bash
   python -m venv env
   .\env\Scripts\activate
   pip install fastapi uvicorn matplotlib sqlite3
   ```
2. Lancez le serveur avec la commande suivante :
   ```bash
   fastapi dev serveur_partie2.py
   ```
3. Accédez aux différentes fonctionnalités via un navigateur web :
   - Pour visualiser le camembert des factures : [http://127.0.0.1:8000/factures](http://127.0.0.1:8000/factures)
   - Pour accéder aux informations météo : [http://127.0.0.1:8000/weather](http://127.0.0.1:8000/weather)

### 2. `capt_temp.ino`
Ce fichier Arduino est utilisé pour :
- **Remplir la base de données :**
  - Le capteur de température connecté au microcontrôleur envoie les données collectées vers la base via une connexion réseau.
- **Activer des actions basées sur les données météo :**
  - Par exemple, si la température extérieure (obtenue via l'API météo) est de 15 °C, une LED est allumée automatiquement.

#### Instructions pour l'adaptation locale :
1. Changez le SSID et le mot de passe WiFi pour correspondre à votre réseau local :
   ```cpp
   const char* ssid = "Votre_SSID";
   const char* password = "Votre_MotDePasse";
   ```
2. Remplacez l'adresse du serveur dans le code par `http://<votre_adresse_ip>:8000/mesures/` :
   ```cpp
   const char* serverPath = "http://192.168.1.100:8000/mesures/";
   ```
3. Si la requête HTTP échoue, désactivez temporairement le pare-feu de votre machine pour autoriser les connexions entrantes.

## Prérequis
- Python 3.8 ou supérieur
- Arduino IDE
- SQLite3
- Bibliothèques Python :
  - `fastapi`
  - `sqlite3`
  - `matplotlib`
- Bibliothèques Arduino :
  - `DHT` pour le capteur de température

## Installation
1. Placez-vous dans le répertoire du projet :
   ```bash
   cd votre-projet
   ```
2. Lancez le serveur Python pour visualiser les pages web :
   ```bash
   fastapi dev serveur_partie2.py
   ```
3. Chargez et exécutez le code Arduino sur le microcontrôleur via l'IDE Arduino.

## Sources
- ChatGPT (assisté pour la génération des scripts Python et Arduino).
- Documentation Flask et Arduino.
- Moodle (références pédagogiques).

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## PARTIE 3:
##fichiers concernés : serveur.py / index.html / logement1.html / logement2.html / logement3.html / suivant.html / page_capteurs.html

### Structure des Fichiers

### 1. `serveur.py`
Ce fichier Python joue le rôle de serveur principal pour le projet. Il permet :
- **Récupération des données :**
  - Des requêtes GET sont utilisées pour extraire des informations spécifiques de la base de données, comme les détails des logements, qui seront affichés sur le site web.
- **Affichage des pages web :**
  - Les requêtes GET servent également à lier chaque page HTML à un code Python, rendant les pages interactives.

#### Fonctionnement :
1. Créez un environnement virtuel Python et installez les dépendances nécessaires :
   ```bash
   python -m venv env
   .\env\Scripts\activate
   pip install fastapi uvicorn sqlite3
   ```
2. Lancez le serveur avec la commande suivante :
   ```bash
   fastapi dev serveur.py
   ```
3. Accédez au site via un navigateur web à l'adresse suivante : [http://127.0.0.1:8000](http://127.0.0.1:8000)

### 2. `index.html`
La page d'accueil du site contient deux sections principales :
- **Modèles de logement :**
  - Présente plusieurs options de logement sous forme de cartes interactives.
  - En cliquant sur un modèle, l'utilisateur est redirigé vers une page dédiée au logement sélectionné.
- **Inscription :**
  - Un formulaire permet à l'utilisateur d'ajouter un nouveau logement dans la base de données en entrant les informations requises, puis en cliquant sur le bouton "Suivant".

### 3. `logement1.html`, `logement2.html`, `logement3.html`
Ces fichiers correspondent aux pages des différents modèles de logement. Chaque page inclut :
- **Liste des capteurs et actionneurs :**
  - Les capteurs et actionneurs dans les pièces sont affichés avec des noms cliquables. Cliquer sur un nom ouvre une popup avec des informations détaillées.
- **Graphique :**
  - Affiche la consommation et les économies réalisées pour le logement concerné.
- **Navigation :**
  - Un menu dans l'en-tête permet de naviguer facilement entre les sections de la page.

### 4. `suivant.html`
Cette page s'affiche après l'inscription d'un nouveau logement. Elle confirme l'ajout avec un résumé des informations saisies et un bouton de retour à la page d'accueil.

### 5. `page_capteurs.html`
Cette page est dédiée à l'ajout de capteurs personnalisés. Elle propose :
- **Compatibilité des actionneurs :**
  - Une liste des actionneurs compatibles est affichée en fonction des capteurs sélectionnés.
- **Navigation :**
  - Un bouton permet de revenir facilement à la page d'accueil.

## Prérequis
- Python 3.8 ou supérieur
- SQLite3
- Bibliothèques Python :
  - `fastapi`
  - `sqlite3`
- Navigateurs web récents (Chrome, Firefox, etc.)

## Installation
1. Placez-vous dans le répertoire du projet :
   ```bash
   cd votre-projet
   ```
2. Lancez le serveur Python :
   ```bash
   fastapi dev serveur.py
   ```
3. Ouvrez un navigateur et accédez à [http://127.0.0.1:8000](http://127.0.0.1:8000) pour interagir avec le site.

## Sources
- ChatGPT (assisté pour la génération des scripts Python et HTML).
- Moodle (références pédagogiques).
