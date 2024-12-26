import psutil
from datetime import datetime
import time
from tracker.database import get_session, create_app, create_log, close_log, get_app_id

def track_applications(apps_to_track):
    tracked_processes = {}
    session = get_session()

    try:
        while True:
            for process in psutil.process_iter(['pid', 'name']):
                app_name = process.info['name']
                if app_name in apps_to_track and app_name not in tracked_processes:
                    start_time = datetime.now()
                    tracked_processes[app_name] = (process, start_time)

                    app = create_app(session, app_name)
                    create_log(session, app.id)

            for app_name in list(tracked_processes.keys()):
                process, start_time = tracked_processes[app_name]
                if not psutil.pid_exists(process.pid):
                    del tracked_processes[app_name]

                    id = get_app_id(session, app_name)
                    close_log(session, id)

            time.sleep(1)
    except KeyboardInterrupt:
        print("\nDetección finalizada.")
    finally:
        session.close()

if __name__ == "__main__":
    apps_to_track = ["spotify","firefox-bin","chrome"]
    print("Iniciando rastreo de aplicaciones...")
    track_applications(apps_to_track)