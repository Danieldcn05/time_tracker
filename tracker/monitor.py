import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import psutil
from datetime import datetime
import time
from tracker.database import get_session, create_log, close_log, get_app_id, fetch_tracked_ps

def track_applications(apps_to_track):
    tracked_processes = {}
    session = get_session()

    try:
        while True:
            for process in psutil.process_iter(['pid', 'name']):
                ps_name = process.info['name']
                id = get_app_id(session, ps_name)
                if ps_name in apps_to_track and ps_name not in tracked_processes:
                    start_time = datetime.now()
                    tracked_processes[ps_name] = (process, start_time)

                    create_log(session, id)

            for ps_name in list(tracked_processes.keys()):
                process, start_time = tracked_processes[ps_name]
                if not psutil.pid_exists(process.pid):
                    id = get_app_id(session, ps_name)  
                    del tracked_processes[ps_name]

                    close_log(session, id)

            time.sleep(1) 
            print("Running " + str(datetime.now()))
    except KeyboardInterrupt:
        print("\nDetection finished.")
    finally:
        session.close()

if __name__ == "__main__":
    apps_to_track = fetch_tracked_ps(get_session()) 
    print("Starting application tracking...")
    print("Tracked processes: ", apps_to_track)
    track_applications(apps_to_track)
