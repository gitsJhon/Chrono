import requests
import sqlite3
import os
from BD_driver import conectar_bd, desconectar_bd
from apps import get_user_apps
from datetime import date
from registrar_apps import registrar_app
import json
def categorizar_app():
    apps = get_user_apps()
    conn = conectar_bd()
    cursor = conn.cursor()
    apps_categorizadas = []
    ruta_json = os.path.join(os.path.dirname(__file__), '../../assets/json/pre_apps.JSON')
    with open(ruta_json, 'r') as file:
        pre_apps = json.load(file)
    url_steam = f"https://api.steampowered.com/ISteamApps/GetAppList/v2/"
    response = requests.get(url_steam)
    if response.status_code == 200:
        data = response.json()
        apps_steam = data["applist"]["apps"]
    else:
        apps_steam = []
    steam_nombres = set(a["name"].lower() for a in apps_steam) #Tabla de steam mas rapida de buscar
    for app in apps:
        cursor.execute("SELECT * FROM apps WHERE nombre = ?", (app["name"],))
        resultado = cursor.fetchone()
        
        if resultado:
            categoria = resultado[3]  # De la consulta anterior 
            apps_categorizadas.append({
                "nombre": app["name"],
                "categoria": categoria
            })
        else:
            #en este punto es que no esta en la base de datos
            #Buscamos en la lista descargada de steam
            if  app["name"].lower() in steam_nombres: #En este caso la app esta en steam
                apps_categorizadas.append({
                    "nombre": app["name"],
                    "categoria": "Ocio"
                })
                registrar_app(app["name"], "Ocio")
            else: #En este caso la app no esta en steam
                apps_categorizadas.append({
                    "nombre": app["name"],
                    "categoria": "Indefinida"
                })
                registrar_app(app["name"], "Indefinida")
    desconectar_bd(conn)  #Desconectamos la base de datos
    return apps_categorizadas #Return de cada app


