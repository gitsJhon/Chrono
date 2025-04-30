import requests
import sqlite3
import os
from BD_driver import conectar_bd, desconectar_bd
from apps import get_user_apps
from datetime import date



#registro de app
def registrar_app(app_name,category):
    ultima_apertura = date.today()
    conn = conectar_bd()
    if conn is None:
        return False
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO apps (nombre, categoria, ultima_apertura)
        VALUES (?, ?, ?)
    """, (app_name, category, ultima_apertura))
    conn.commit()
    desconectar_bd(conn)
    return True

def ver_apps():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM apps")
    apps = cursor.fetchall()
    for app in apps:
        print(app)
    desconectar_bd(conn)

# Probar
ver_apps()
