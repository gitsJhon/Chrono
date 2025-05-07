import time
from process_utils import get_user_apps, get_visible_window_pids

apps_abiertas = {}
def get_apps_with_time():
    apps = get_user_apps()
    current_time = time.time()

    nombres_visibles = set(app['name'] for app in apps)
    for app in apps:
        name = app['name']
        #detecta nuevas apps
        if name not in apps_abiertas:
            apps_abiertas[name] = current_time
        #detecta apps cerradas
        cerradas = [name for name in apps_abiertas if name not in nombres_visibles]
        for name in cerradas:
            start_time = apps_abiertas.pop(name)
            tiempo = int(current_time - start_time)
            #Luego la añado a la base de datos, que pereza ahora
        apps_with_time = []
        for app in apps:
            name = app['name']
            if name in apps_abiertas:
                start_time = apps_abiertas[name]
                start_time = apps_abiertas[name]
                apps_with_time.append({
                    "name": name,
                    "start_time": start_time
                })
    return apps_with_time

def get_apps_with_time_and_category():
    from category import categorizar_app
    apps_time = get_apps_with_time()
    apps_categorizadas = categorizar_app()

    categorized_apps = []

    for app_time in apps_time:
        name = app_time['name']
        start_time = app_time['start_time']

        category = next((app['categoria'] for app in apps_categorizadas if app['nombre'] == name), "Indefinida")
        categorized_apps.append({
            "name": name,
            "start_time": start_time,
            "category": category
        })
    return categorized_apps
