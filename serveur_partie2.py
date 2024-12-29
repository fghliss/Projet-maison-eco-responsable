#PARTIE 2 
#source en bas de la page

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from fastapi.responses import HTMLResponse
import sqlite3
from typing import List
import requests
import json
from fastapi.responses import HTMLResponse 



#Question 1 : les fonctions add_mesure et add_capt_actionneur permettent le remplissage de la base de donnée


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

@app.post("/capt_actionneur/")
def add_capt_actionneur(capt: CaptActionneur):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(
            "INSERT INTO capt_actionneur (id_logement, ref_piece, type_device, type_capt_act, ref_commercial, port_communication) VALUES (?, ?, ?, ?, ?, ?)",
            (
                capt.id_logement,
                capt.ref_piece,
                capt.type_device,
                capt.type_capt_act,
                capt.ref_commercial,
                capt.port_communication,
            ),
        )
        conn.commit()
        conn.close()
        return {"message": "Capteur/Actionneur ajouté avec succès"}
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400, detail="Violation d'intégrité. Vérifiez les IDs."
        )
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Erreur SQLite : {e}")
    





#Question 2   

# Connexion à la base de données SQLite
def get_factures():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT type_facture, montant FROM facture")
        factures = c.fetchall()
        conn.close()
        # Retourner les données sous forme de liste de dictionnaires
        return [{"type_facture": row[0], "montant": row[1]} for row in factures]
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Erreur SQLite : {e}")

# Route GET pour afficher la page HTML avec le graphique
@app.get("/factures", response_class=HTMLResponse)
def factures():
    # Récupérer les données des factures
    factures = get_factures()

    # Générer la variable data_convertie pour Google Charts
    data_convertie = [["Type de Facture", "Montant"]]  # En-têtes pour Google Charts
    data_convertie += [[facture["type_facture"], facture["montant"]] for facture in factures]

    # Convertir les données en JSON pour les utiliser dans le script JavaScript

    data_json = json.dumps(data_convertie)

    # Générer le contenu HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Graphique des Factures</title>
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
        <script type="text/javascript">
            google.charts.load('current', {{'packages':['corechart']}});
            google.charts.setOnLoadCallback(drawChart);

            function drawChart() {{
                var data = google.visualization.arrayToDataTable({data_json});

                var options = {{
                    title: 'Répartition des Factures',
                    is3D: true,
                }};

                var chart = new google.visualization.PieChart(document.getElementById('piechart_3d'));
                chart.draw(data, options);
            }}
        </script>
    </head>
    <body>
        <h1>Graphique des Factures</h1>
        <div id="piechart_3d" style="width: 900px; height: 500px;"></div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)



# Question 3

# Clé API pour openweathermap
# Votre clé API OpenWeatherMap
API_KEY = "ae14abf52617dbae29b3e0efcce691fa"

# Route pour afficher les prévisions météo
@app.get("/weather", response_class=HTMLResponse)
def get_weather(city: str = "Paris"):
    """
    Route pour obtenir les prévisions météo sur 5 jours et les afficher en HTML.
    """
    try:
        # URL pour l'API de prévisions sur 5 jours
        forecast_url = (
            f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=fr"
        )
        
        # Envoyer la requête à OpenWeatherMap
        response = requests.get(forecast_url)
        response.raise_for_status()  # Vérifie les erreurs HTTP

        # Analyse de la réponse JSON
        data = response.json()

        # Vérification des erreurs spécifiques d'OpenWeatherMap
        if "list" not in data:
            error_message = data.get("message", "Erreur inconnue.")
            raise HTTPException(status_code=400, detail=f"Erreur API OpenWeatherMap : {error_message}")

        # Extraction des prévisions toutes les 3 heures pour 5 jours
        forecasts = []
        for forecast in data["list"]:
            date_time = forecast["dt_txt"]
            temperature = forecast["main"]["temp"]
            description = forecast["weather"][0]["description"]
            forecasts.append(f"{date_time} - Température : {temperature}°C - {description}")


        # Génération du contenu HTML
        html_content = f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Prévisions météo pour {city}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                }}
                .forecast {{
                    margin-bottom: 15px;
                    padding: 10px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    background-color: #f9f9f9;
                }}
            </style>
        </head>
        <body>
            <h1>Prévisions météo pour {city} (5 jours)</h1>
        """
        for forecast in forecasts:
            html_content += f"<div class='forecast'>{forecast}</div>"

        html_content += """
        </body>
        </html>
        """
        return HTMLResponse(content=html_content, status_code=200)

    except requests.exceptions.RequestException as e:
        return HTMLResponse(content=f"<h1>Erreur API : {e}</h1>", status_code=500)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Erreur interne : {e}</h1>", status_code=500)

#pour la question 4 voir dossier "capt_temp" qui contient le code arduino


#Source : chatgpt / https://fastapi.tiangolo.com/deployment/manually/#run-the-server-program