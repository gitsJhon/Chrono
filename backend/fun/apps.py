import psutil
import time
import ctypes
from ctypes import wintypes

# API Windows
user32 = ctypes.windll.user32
EnumWindows = user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
GetWindowThreadProcessId = user32.GetWindowThreadProcessId
IsWindowVisible = user32.IsWindowVisible
GetWindowTextW = user32.GetWindowTextW

# Tiempos acumulados
apps_time = {}

def get_visible_window_pids():
    visible_pids = set()
    def foreach_window(hwnd, lParam):
        if IsWindowVisible(hwnd):
            pid = wintypes.DWORD()
            GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            title = ctypes.create_unicode_buffer(512)
            GetWindowTextW(hwnd, title, 512)
            if title.value.strip():
                visible_pids.add(pid.value)
        return True
    EnumWindows(EnumWindowsProc(foreach_window), 0)
    return visible_pids

def get_user_apps():
    visible_pids = get_visible_window_pids()
    user_apps = []
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            if proc.info['pid'] not in visible_pids:
                continue
            exe_path = proc.info['exe']
            if not exe_path or "windows" in exe_path.lower():
                continue
            user_apps.append({
                "pid": proc.info['pid'],
                "name": proc.info['name'],
                "path": exe_path
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return user_apps

def get_apps_with_time():
    apps = get_user_apps()
    current_time = time.time()

    for app in apps:
        key = app['name']
        if key not in apps_time:
            apps_time[key] = {
                "start_time": current_time,
                "total_time": 0
            }
        else:
            elapsed = current_time - apps_time[key]["start_time"]
            apps_time[key]["total_time"] += elapsed
            apps_time[key]["start_time"] = current_time

    apps_with_time = []
    for app in apps:
        name = app['name']
        total_seconds = int(apps_time[name]['total_time'])
        apps_with_time.append({
            "name": name,
            "time": total_seconds
        })

    return apps_with_time