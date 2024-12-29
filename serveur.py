#PARTIE 3 : SERVEUR
#source en bas de la page


from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import sqlite3
from fastapi.responses import HTMLResponse
import sqlite3
from typing import List
import requests
import json
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Form






# Création de l'application FastAPI
app = FastAPI()

# Chemin vers la base de données SQLite
DB_PATH = "C:\\Users\\FarahGhliss\\Desktop\\IOT_2\\TP_iot\\logement.db"

#specifier l'encodage
@app.get("/", response_class=HTMLResponse)
async def home():
    content = open("index.html", encoding="utf-8").read()
    return HTMLResponse(content=content, media_type="text/html; charset=utf-8")

# Modèle Pydantic pour représenter une mesure
class Mesure(BaseModel):
    id_capteur_actionneur: int
    valeur: float
    date_insertion: str  # Format : 'YYYY-MM-DD'

# Route pour récupérer toutes les mesures
@app.get("/mesures/")
def get_mesures():
    print("test mesures")
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM mesure")
        mesures = c.fetchall()
        conn.close()
        return {
            "mesures": [
                {
                    "id_mesure": m[0],
                    "id_capteur_actionneur": m[1],
                    "valeur": m[2],
                    "date_insertion": m[3],
                }
                for m in mesures
            ]
        }
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Erreur SQLite : {e}")

# Route pour ajouter une nouvelle mesure
@app.post("/mesures/")
def add_mesure(mesure: Mesure):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(
            "INSERT INTO mesure (id_capteur_actionneur, valeur, date_insertion) VALUES (?, ?, ?)",
            (mesure.id_capteur_actionneur, mesure.valeur, mesure.date_insertion),
        )
        conn.commit()
        conn.close()
        return {"message": "Mesure ajoutée avec succès"}
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400, detail="Violation d'intégrité. Vérifiez les IDs."
        )
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Erreur SQLite : {e}")

# Route pour récupérer les capteurs/actionneurs
@app.get("/capt_actionneur/")
def get_capt_actionneur():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM capt_actionneur")
        capt_actionneurs = c.fetchall()
        conn.close()
        return {
            "capt_actionneurs": [
                {
                    "id_capteur_actionneur": ca[0],
                    "id_logement": ca[1],
                    "ref_piece": ca[2],
                    "type_device": ca[3],
                    "type_capt_act": ca[4],
                    "ref_commercial": ca[5],
                    "port_communication": ca[6],
                }
                for ca in capt_actionneurs
            ]
        }
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Erreur SQLite : {e}")

# Route pour ajouter un nouveau capteur/actionneur
class CaptActionneur(BaseModel):
    id_logement: int
    ref_piece: int
    type_device: str
    type_capt_act: str
    ref_commercial: str
    port_communication: str

@app.get("/capteurs/")
def get_capteurs():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT ref_commercial FROM capt_actionneur WHERE type_capt_act = 'capteur'")
        capteurs = c.fetchall()
        conn.close()
        
        # Retourne la liste des capteurs sous forme de réponse JSON
        return {"capteurs": [capteur[0] for capteur in capteurs]}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Erreur SQLite : {e}")





def get_logements():
    try:
        # Connexion à la base de données SQLite
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Requête pour récupérer 3 logements seulement
        c.execute("SELECT id_logement, adresse, surface, nombre_piece, consommation_electricite, consommation_eau, consommation_dechets FROM logement LIMIT 3")
        
        # Récupération des lignes de la requête
        logements = c.fetchall()
        
        # Fermeture de la connexion à la base de données
        conn.close()
        
        # Retourner les données sous forme de liste de dictionnaires
        return [
            {
                "id_logement": row[0],
                "adresse": row[1],
                "surface": row[2],
                "nombre_piece": row[3],
                "consommation_electricite": row[4],
                "consommation_eau": row[5],
                "consommation_dechets": row[6]
            }
            for row in logements
        ]
    except sqlite3.Error as e:
        # Si une erreur survient lors de la requête SQLite
        raise HTTPException(status_code=500, detail=f"Erreur SQLite : {e}")
  
    

@app.get("/logements", response_class=JSONResponse)
async def logements():
    # Récupérer les données des logements
    logements = get_logements()
    
    # Convertir les données en JSON
    return JSONResponse(content=logements)




# Route pour la page d'accueil
@app.get("/", response_class=HTMLResponse)
def home():
    return HTMLResponse(content=open("index.html").read(), status_code=200)


# Serve static files (images, CSS, JS, etc.)
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

# Routes pour les logements
#logement1
@app.get("/logement1", response_class=HTMLResponse)
async def logement1():
    with open("logement1.html", "r", encoding="utf-8") as file:
        return file.read()
    
@app.get("/logement2", response_class=HTMLResponse)
async def logement1():
    with open("logement2.html", "r", encoding="utf-8") as file:
        return file.read()
    
@app.get("/logement3", response_class=HTMLResponse)
async def logement1():
    with open("logement3.html", "r", encoding="utf-8") as file:
        return file.read()
    
# Route pour les fichiers statiques
@app.get("/assets/{file_path:path}")
async def serve_assets(file_path: str):
    return FileResponse(f"assets/{file_path}")






def get_factures():
    try:
        # Connexion à la base de données SQLite
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT type_facture, montant FROM facture")
        factures = c.fetchall()
        conn.close()
        
        # Retourner les données sous forme de liste de dictionnaires
        return [{"type_facture": row[0], "montant": row[1]} for row in factures]
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Erreur SQLite : {e}")

# Route pour récupérer les données des factures en JSON
@app.get("/factures")
def factures():
    # Récupérer les données des factures
    factures = get_factures()

    # Retourner les données sous forme de JSON
    return JSONResponse(content=factures)



# Modèle Pydantic pour l'inscription
class LogementForm(BaseModel):
    address: str
    surface: int
    rooms: int
    electricity: float
    water: float
    waste: float

# # Route POST pour le formulaire d'inscription
@app.post("/suivant")
async def suivant(
        address: str = Form(...),
        surface: int = Form(...),
        rooms: int = Form(...),
        electricity: float = Form(...),
        water: float = Form(...),
        waste: float = Form(...),
    ):
        try:
            # Traitement des données et insertion dans la base de données
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute(
                """
                INSERT INTO logement (adresse, surface, nombre_piece, consommation_electricite, consommation_eau, consommation_dechets)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (address, surface, rooms, electricity, water, waste),
            )
            conn.commit()
            conn.close()

            # Rediriger vers la page suivante
            return RedirectResponse(url="/suivant.html", status_code=303)

        except sqlite3.Error as e:
            raise HTTPException(status_code=500, detail=f"Erreur de base de données : {e}")

@app.get("/suivant.html", response_class=HTMLResponse)
async def afficher_suivant():
    with open("suivant.html", "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content=content)


# Modèle pour les mesures de capteurs
class Mesure(BaseModel):
    temperature: float
    humidite: float

# Liste pour stocker temporairement les données de capteurs
mesures: List[Mesure] = []


# Endpoint pour afficher la page HTML
@app.get("/page_capteurs.html", response_class=HTMLResponse)
async def afficher_page():
    with open("page_capteurs.html", "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content=content)



#Source : chatgpt / https://fastapi.tiangolo.com/deployment/manually/#run-the-server-program