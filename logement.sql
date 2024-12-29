-- PARTIE 1.1
-- source en bas de la page 
-- database: logement.db


--QUESTION 2/3 :

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



-- Suppression et création de la table Piece
DROP TABLE IF EXISTS Piece;
CREATE TABLE Piece (
    id_piece INTEGER PRIMARY KEY AUTOINCREMENT,
    id_logement INTEGER,
    nbre_capteurs_actionneurs INTEGER,
    coordonnees_x INTEGER,
    coordonnees_y INTEGER,
    coordonnees_z INTEGER,
    FOREIGN KEY (id_logement) REFERENCES logement(id_logement)
);

-- Suppression et création de la table capt_actionneur
DROP TABLE IF EXISTS capt_actionneur;
CREATE TABLE capt_actionneur (
    id_capteur_actionneur INTEGER PRIMARY KEY AUTOINCREMENT,
    id_logement INTEGER,
    ref_piece INTEGER,
    type_device TEXT CHECK(type_device IN ('capteur', 'actionneur')) NOT NULL,
    type_capt_act TEXT,
    ref_commercial TEXT,
    port_communication TEXT,
    FOREIGN KEY (ref_piece) REFERENCES Piece(id_piece),
    FOREIGN KEY (id_logement) REFERENCES logement(id_logement)
);

-- Suppression et création de la table mesure
DROP TABLE IF EXISTS mesure;
CREATE TABLE mesure (
    id_mesure INTEGER PRIMARY KEY AUTOINCREMENT,
    id_capteur_actionneur INTEGER,
    valeur REAL NOT NULL,
    date_insertion DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (id_capteur_actionneur) REFERENCES capt_actionneur(id_capteur_actionneur)
);

-- Suppression et création de la table Type_capt_act
DROP TABLE IF EXISTS Type_capt_act;
CREATE TABLE Type_capt_act (
    id_type INTEGER PRIMARY KEY AUTOINCREMENT,
    type_device TEXT CHECK(type_device IN ('capteur', 'actionneur')) NOT NULL,
    describe TEXT,
    unite_mesure TEXT,
    plage_precision TEXT
);

-- Suppression et création de la table facture
DROP TABLE IF EXISTS Facture;
CREATE TABLE facture (
    id_facture INTEGER PRIMARY KEY AUTOINCREMENT,
    id_logement INTEGER,
    type_facture TEXT NOT NULL,
    date_facture DATE,
    montant REAL NOT NULL,
    valeur_consommation REAL,
    FOREIGN KEY (id_logement) REFERENCES logement(id_logement)
);


-- QUESTION 4:

-- Insertion d'un logement1 avec les nouvelles données
INSERT INTO logement (adresse, nombre_piece, surface, num_telephone, adresse_ip, consommation_electricite, consommation_eau, consommation_dechets)
VALUES ('45 rue louise michel', 4, 100, '0123456789', '192.168.1.1', 500, 10, 50);

-- Insertion d'un logement2 avec les nouvelles données
INSERT INTO logement (adresse, nombre_piece, surface, num_telephone, adresse_ip, consommation_electricite, consommation_eau, consommation_dechets)
VALUES ('21 rue la marsa', 5, 200, '0707070707', '193.168.1.1', 300, 240, 150);


-- Insertion d'un logement3 avec les nouvelles données
INSERT INTO logement (adresse, nombre_piece, surface, num_telephone, adresse_ip, consommation_electricite, consommation_eau, consommation_dechets)
VALUES ('4 rue de la paix ', 6, 250, '0753354169', '193.168.2.1', 500, 240, 150);



-- Insertion des pièces associées au logement
INSERT INTO Piece (id_logement, nbre_capteurs_actionneurs, coordonnees_x, coordonnees_y, coordonnees_z)
VALUES (1, 0, 0, 0, 0);

INSERT INTO Piece (id_logement, nbre_capteurs_actionneurs, coordonnees_x, coordonnees_y, coordonnees_z)
VALUES (1, 0, 1, 0, 0);

INSERT INTO Piece (id_logement, nbre_capteurs_actionneurs, coordonnees_x, coordonnees_y, coordonnees_z)
VALUES (1, 0, 0, 1, 0);

INSERT INTO Piece (id_logement, nbre_capteurs_actionneurs, coordonnees_x, coordonnees_y, coordonnees_z)
VALUES (1, 0, 1, 1, 0);



--QUESTION 5:
-- Insertion des types de capteurs/actionneurs
INSERT INTO Type_capt_act (type_device, describe, unite_mesure, plage_precision)
VALUES ('capteur', 'Capteur de température', '°C', '-10°C à 50°C');

INSERT INTO Type_capt_act (type_device, describe, unite_mesure, plage_precision)
VALUES ('capteur', 'Capteur humidité', '%', '0% à 100%');

INSERT INTO Type_capt_act (type_device, describe, unite_mesure, plage_precision)
VALUES ('actionneur', 'Actionneur lumière', 'Lux', '0 à 1000 Lux');

INSERT INTO Type_capt_act (type_device, describe, unite_mesure, plage_precision)
VALUES ('actionneur', 'Actionneur chauffage', '°C', '5°C à 30°C');

-- Insertion des capteurs/actionneurs (logement1)
INSERT INTO capt_actionneur (id_logement, ref_piece, type_device, type_capt_act, ref_commercial, port_communication)
VALUES (1, 1, 'capteur', 'température', 'DHT22', 'COM1');

INSERT INTO capt_actionneur (id_logement, ref_piece, type_device, type_capt_act, ref_commercial, port_communication)
VALUES (1, 1, 'capteur', 'température', 'Thermostat Intelligent', 'COM1');

INSERT INTO capt_actionneur (id_logement, ref_piece, type_device, type_capt_act, ref_commercial, port_communication)
VALUES (1, 2, 'actionneur', 'chauffage', 'HEAT456', 'COM2');

INSERT INTO capt_actionneur (id_logement, ref_piece, type_device, type_capt_act, ref_commercial, port_communication)
VALUES (1, 2, 'actionneur', 'chauffage', 'Déshumidificateur', 'COM2');

-- Insertion des capteurs/actionneurs (logement2)
INSERT INTO capt_actionneur (id_logement, ref_piece, type_device, type_capt_act, ref_commercial, port_communication)
VALUES (2, 1, 'capteur', 'lumiere', 'BH1750', 'COM1');

INSERT INTO capt_actionneur (id_logement, ref_piece, type_device, type_capt_act, ref_commercial, port_communication)
VALUES (2, 1, 'capteur', 'CO2', 'MH-Z19', 'COM1');

INSERT INTO capt_actionneur (id_logement, ref_piece, type_device, type_capt_act, ref_commercial, port_communication)
VALUES (2, 2, 'actionneur', 'lampe', 'Lampe LED Intelligente', 'COM2');

INSERT INTO capt_actionneur (id_logement, ref_piece, type_device, type_capt_act, ref_commercial, port_communication)
VALUES (2, 2, 'actionneur', 'ventilateur', 'Ventillateur connecté', 'COM2');

-- Insertion des capteurs/actionneurs (logement3)
INSERT INTO capt_actionneur (id_logement, ref_piece, type_device, type_capt_act, ref_commercial, port_communication)
VALUES (3, 1, 'capteur', 'température et humidité', 'DHT22', 'COM1');

INSERT INTO capt_actionneur (id_logement, ref_piece, type_device, type_capt_act, ref_commercial, port_communication)
VALUES (3, 1, 'capteur', 'CO2', 'MH-Z14', 'COM1');

INSERT INTO capt_actionneur (id_logement, ref_piece, type_device, type_capt_act, ref_commercial, port_communication)
VALUES (3, 1, 'capteur', 'Présence', 'HC-SR501', 'COM1');


INSERT INTO capt_actionneur (id_logement, ref_piece, type_device, type_capt_act, ref_commercial, port_communication)
VALUES (3, 2, 'actionneur', 'volets', 'Volets Roulants Automatique', 'COM2');

INSERT INTO capt_actionneur (id_logement, ref_piece, type_device, type_capt_act, ref_commercial, port_communication)
VALUES (3, 2, 'actionneur', 'chauffage', 'chauffage Intelligent', 'COM2');

INSERT INTO capt_actionneur (id_logement, ref_piece, type_device, type_capt_act, ref_commercial, port_communication)
VALUES (3, 2, 'actionneur', 'purificateur', 'purificateur d air connecté', 'COM2');


--QUESTION 6:
-- Insertion des mesures associées aux capteurs/actionneurs
INSERT INTO mesure (id_capteur_actionneur, valeur, date_insertion)
VALUES (1, 22.5, '2024-11-08');

INSERT INTO mesure (id_capteur_actionneur, valeur, date_insertion)
VALUES (1, 23.0, '2024-11-09');

INSERT INTO mesure (id_capteur_actionneur, valeur, date_insertion)
VALUES (2, 20.0, '2024-11-08');

INSERT INTO mesure (id_capteur_actionneur, valeur, date_insertion)
VALUES (2, 22.0, '2024-11-09');


--QUESTION 8:
-- Insertion des factures associées au logement
INSERT INTO facture (id_logement, type_facture, date_facture, montant, valeur_consommation)
VALUES (1, 'eau', '2024-11-01', 50.75, 100.5);

INSERT INTO facture (id_logement, type_facture, date_facture, montant, valeur_consommation)
VALUES (1, 'électricité', '2024-11-05', 120.40, 250.3);

INSERT INTO facture (id_logement, type_facture, date_facture, montant, valeur_consommation)
VALUES (1, 'déchets', '2024-11-02', 30.00, 5.0);

INSERT INTO facture (id_logement, type_facture, date_facture, montant, valeur_consommation)
VALUES (1, 'électricité', '2024-11-06', 85.20, 180.7);



--source : chatgpt