from process_utils import get_user_apps
import psutil
import GPUtil
import time

def apps_consumo():
    apps_visibles = get_user_apps()  # Apps a escanear
    resultados = {}
    procesos = {proc.pid: proc for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_info', 'pid'])}

    # Inicializamos CPU percent para todos los procesos
    for proc in procesos.values():
        try:
            proc.cpu_percent(None)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    time.sleep(0.1)  # Espera para que haya delta de CPU

    for app in apps_visibles:
        nombre_app = app["name"]
        pid = app["pid"]

        consumo_CPU = 0.0
        consumo_memoria = 0

        proc = procesos.get(pid)
        if proc:
            try:
                consumo_CPU = proc.cpu_percent(None)  # Ahora sí devuelve delta real
                consumo_memoria = proc.memory_info().rss / (1024 * 1024)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        resultados[nombre_app] = {
            'cpu_percent': round(consumo_CPU, 2),
            'memory_mb': round(consumo_memoria, 2),
            'gpu_percent': None,  # Se añade abajo
            'pid': pid
        }

    # GPU total del sistema
    gpus = GPUtil.getGPUs()
    consumo_gpu_total = sum([gpu.load for gpu in gpus]) * 100 if gpus else None

    for app in resultados:
        resultados[app]['gpu_percent'] = round(consumo_gpu_total, 2) if consumo_gpu_total is not None else None

    return resultados

# Test
print(apps_consumo())

