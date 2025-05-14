from process_utils import get_user_apps
import psutil
import GPUtil

def apps_consumo():
    apps_visibles = get_user_apps() #Apps a escanear
    #activas
    resultados = {}
    procesos = [proc for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_info', 'pid'])]

    for app in apps_visibles:
        nombre_app = app["name"]
        consumo_CPU = 0.0
        consumo_memoria = 0
        pids = []

        for proc in procesos:
            try:
                if proc.info['name'].lower() == nombre_app.lower():
                    consumo_CPU += proc.cpu_percent(interval=0.1)
                    consumo_memoria += proc.memory_info().rss / (1024 * 1024)
                    pids.append(proc.info['pid'])
            
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    
    #GPU
    gpus = GPUtil.getGPUs()
    consumo_gpu = sum([gpu.load for gpu in gpus]) * 100 if gpus else None

    resultados[nombre_app] = {
        'cpu_percent': round(consumo_CPU, 2),
        'memory_mb': round(consumo_memoria, 2),
        'gpu_percent': round(consumo_gpu, 2) if consumo_gpu is not None else None,
        'pids': pids
    }

    return resultados

if __name__ == "__main__":
    consumo = apps_consumo()
    for app, datos in consumo.items():
        print(f"{app}: {datos}")