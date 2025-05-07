import requests
import sqlite3
import os
import json
from BD_driver import conectar_bd, desconectar_bd
from process_utils import get_user_apps
from datetime import date
from registrar_apps import registrar_app
import difflib

def categorizar_app():
    apps = get_user_apps()
    conn = conectar_bd()
    cursor = conn.cursor()
    apps_categorizadas = []

    ruta_json = os.path.join(os.path.dirname(__file__), '../../assets/json/pre_apps.JSON')
    with open(ruta_json, 'r', encoding='utf-8') as f:
        pre_apps = json.load(f)
    
    pre_apps_dict = {app["nombre"].lower(): app["categoria"] for app in pre_apps}


    url_steam = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
    response = requests.get(url_steam)
    apps_steam = response.json()["applist"]["apps"] if response.status_code == 200 else []
    steam_nombres = set(a["name"].lower() for a in apps_steam)

    for app in apps:
        nombre_app = app["name"]

        # Buscar en base de datos local
        cursor.execute("SELECT * FROM apps WHERE nombre = ?", (nombre_app,))
        resultado = cursor.fetchone()

        if resultado:
            categoria = resultado[2]
        elif nombre_app.lower() in pre_apps_dict:
            # Buscar en JSON local
            categoria = pre_apps_dict[nombre_app.lower()]
            registrar_app(nombre_app, categoria)
        else:
            steam_match = difflib.get_close_matches(nombre_app.lower(), steam_nombres, n=1, cutoff=0.8)
            if steam_match:
                categoria = "Ocio"
                registrar_app(nombre_app, categoria)
            else:
                # Si no se encuentra en la base de datos ni en el JSON, asignar "Indefinida"
                categoria = "Indefinida"
                registrar_app(nombre_app, categoria)
        apps_categorizadas.append({
            "nombre": nombre_app,
            "categoria": categoria
        })
    desconectar_bd(conn)
    return apps_categorizadas