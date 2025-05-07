from backend.fun.BD_driver import conectar_bd, desconectar_bd

conn = conectar_bd()
cursor = conn.cursor()

cursor.execute("SELECT * FROM apps")
resultado = cursor.fetchall()
for fila in resultado:
    print(fila)
desconectar_bd(conn)

