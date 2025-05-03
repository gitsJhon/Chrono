from BD_driver import conectar_bd, desconectar_bd
import sqlite3
import time
from datetime import date

#registro de app
def registrar_app(app_name,category): #Falta agregar los try para amnejor de rrores
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