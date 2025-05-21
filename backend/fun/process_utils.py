import psutil
import ctypes
from ctypes import wintypes
import os

user32 = ctypes.windll.user32
EnumWindows = user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
GetWindowThreadProcessId = user32.GetWindowThreadProcessId
IsWindowVisible = user32.IsWindowVisible
GetWindowTextW = user32.GetWindowTextW

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
            name = os.path.splitext(proc.info['name'])[0]
            user_apps.append({
                "pid": proc.info['pid'],
                "name": name,
                "path": exe_path
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return user_apps
