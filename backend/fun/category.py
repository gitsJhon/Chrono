import requests

def buscar_juego_en_steam(nombre_juego):
    url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        juegos = data['applist']['apps']

        # Filtra por nombre exacto (puedes ajustar con lower o similitud)
        for juego in juegos:
            if nombre_juego.lower() in juego['name'].lower():
                return juego
    else:
        print("Error al obtener datos de Steam.")
    return None

# Prueba
resultado = buscar_juego_en_steam("Fortnite")
if resultado:
    print(f"Juego encontrado: {resultado}")
else:
    print("Juego no encontrado.")
