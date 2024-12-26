import psutil
from datetime import datetime
import time

def track_applications(apps_to_track):
    """
    Rastrea aplicaciones específicas y registra en consola
    cuándo se abren y cierran.
    """
    tracked_processes = {}  # Diccionario para guardar procesos activos

    try:
        while True:
            # Iterar sobre los procesos en ejecución
            for process in psutil.process_iter(['pid', 'name']):
                app_name = process.info['name']
                if app_name in apps_to_track and app_name not in tracked_processes:
                    # Registrar inicio de la aplicación
                    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"[START] {app_name} - {start_time}")
                    tracked_processes[app_name] = process

            # Verificar si alguna aplicación rastreada ha terminado
            for app_name in list(tracked_processes.keys()):
                if not psutil.pid_exists(tracked_processes[app_name].pid):
                    # Registrar cierre de la aplicación
                    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"[CLOSE] {app_name} - {end_time}")
                    del tracked_processes[app_name]

            time.sleep(1)  # Reducir la carga en la CPU
    except KeyboardInterrupt:
        print("\nDetección finalizada.")

if __name__ == "__main__":
    # Lista de aplicaciones que quieres rastrear (puedes personalizar)
    apps_to_track = ["spotify"]  # Ejemplo para Windows
    # En Linux/Mac, usa nombres como "firefox" o "gedit".
    print("Iniciando rastreo de aplicaciones...")
    track_applications(apps_to_track)
