import subprocess
import signal
import time
import os
import sys

# Ejecutar npm start
electron_process = subprocess.Popen(["npm", "start"], shell=True)

# Esperar un poco para que Electron inicie antes de levantar el servidor
time.sleep(2)

# Ejecutar servidor WebSocket
server_process = subprocess.Popen(["python", "backend/fun/server.py"], shell=True)

try:
    while True:
        # Si Electron se cierra, terminar todo
        if electron_process.poll() is not None:
            print("Electron cerrado. Terminando servidor...")
            server_process.terminate()
            break

        time.sleep(1)

except KeyboardInterrupt:
    print("Interrupción manual. Cerrando todo...")
    electron_process.terminate()
    server_process.terminate()

# Esperar que los procesos terminen bien
electron_process.wait()
server_process.wait()

print("Todo cerrado.")
