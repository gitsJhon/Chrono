import requests

url_steam = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
response = requests.get(url_steam)
apps_steam = response.json()["applist"]["apps"] if response.status_code == 200 else []
steam_nombres = set(a["name"].lower() for a in apps_steam)

app = "Hollow Knight"
if app.lower() in steam_nombres:
    print("Steam")
