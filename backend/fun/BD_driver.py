import sqlite3
import os

# Ruta absoluta relativa al archivo actual
ruta_bd = os.path.join(os.path.dirname(__file__), 'database', 'BD.db')

# Conexion
def conectar_bd():
    try:
        conn = sqlite3.connect(ruta_bd)
        return conn
    except sqlite3.Error as e:
        return e

# Desconectar
def desconectar_bd(conn):
    if conn:
        conn.close()

# Solo para testear conexión
if __name__ == "__main__":
    print(conectar_bd())
