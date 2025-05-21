import asyncio
import json
import websockets
from app_time_tracker import get_apps_with_time_and_category
from recursos import apps_consumo

async def apps_handler(websocket):
    while True:
        apps_tiempo = get_apps_with_time_and_category()  # lista de apps
        consumo_dict = apps_consumo()  # dict de consumo por app

        # convertir consumo_dict a lista como espera tu JS
        apps_consumo_list = []
        for name, valores in consumo_dict.items():
            apps_consumo_list.append({
                'name': name,
                'gpu': valores['gpu_percent'] if valores['gpu_percent'] is not None else 0,
                'cpu': valores['cpu_percent'],
                'ram': valores['memory_mb']
            })

        paquete = {
            "apps_tiempo": apps_tiempo,
            "apps_consumo": apps_consumo_list
        }

        await websocket.send(json.dumps(paquete))
        await asyncio.sleep(2)

async def main():
    async with websockets.serve(apps_handler, "localhost", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
