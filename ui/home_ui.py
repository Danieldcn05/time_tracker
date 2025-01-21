import tkinter as tk
import os
import subprocess
import signal

# Path to the monitor script
MONITOR_SCRIPT = "tracker/monitor.py"

# PID file for the running process
pid_file = "monitor.pid"

class Home(tk.Frame):
    def __init__(self, parent, controller, session, bg=None):
        tk.Frame.__init__(self, parent, bg=bg)
        self.controller = controller
        self.session = session
        
        button_style = {
            "padx": 100,
            "pady": 20,
            "font": ("Arial", 12),
            "relief": tk.FLAT,
            "bg": "#055FFC",
            "fg": "#F9FEFD",
            "activebackground":"#003CBE",
            "activeforeground":"#F9FEFD"
        }        

        inner_frame = tk.Frame(self, bg=bg)
        inner_frame.pack(fill="both", expand=True)

        label = tk.Label(inner_frame, text="TIME TRACKER", font=("Helvetica", 24), bg=bg, fg="#1E1F23")

        button = tk.Button(inner_frame, text="Logs",
                           command=lambda: controller.show_frame("LogsUI"), **button_style)
        
        button2 = tk.Button(inner_frame, text="Apps",
                           command=lambda: controller.show_frame("AppsUI"), **button_style)
        
        button3 = tk.Button(inner_frame, text="Start Monitor",
                            command=self.start_monitor, **button_style)
        
        button4 = tk.Button(inner_frame, text="Stop Monitor",
                            command=self.stop_monitor, **button_style)
        
        self.tracking = tk.Label(inner_frame, text="Monitor is not running", fg="red", font=("Arial", 20), bg=bg)
        
        label.place(relx=0.5, y=50, anchor="center")
        button.place(relx=0.5, y=150, anchor="center")
        button2.place(relx=0.5, y=250, anchor="center")
        button3.place(relx=0.35, y=350, anchor="center")
        button4.place(relx=0.65, y=350, anchor="center")
        self.tracking.place(relx=0.5, y=450, anchor="center")
        
        if os.path.exists(pid_file):
            self.tracking.config(text="Monitor is running", fg="green")

    def start_monitor(self):
        if os.path.exists(pid_file):
            print("The monitor is already running.")
            self.tracking.config(text="Monitor is running", fg="green")
            return
    
        # Start the script as an independent process
        process = subprocess.Popen(["python", MONITOR_SCRIPT], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Save the PID to a file
        with open(pid_file, "w") as f:
            f.write(str(process.pid))
        
        print(f"Monitor started with PID {process.pid}")
        self.tracking.config(text="Monitor started", fg="green")
    
    def stop_monitor(self):
        # Check if the monitor is running
        if not os.path.exists(pid_file):
            print("The monitor is not running.")
            self.tracking.config(text="Monitor is not running", fg="red")
            return
        
        # Read the PID from the file
        with open(pid_file, "r") as f:
            pid = int(f.read().strip())
        
        # Terminate the process
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError:
            print("Failed to terminate the monitor process.")
            self.tracking.config(text="Failed to stop monitor", fg="red")
            return
        
        # Remove the PID file
        os.remove(pid_file)
        
        print("Monitor stopped.")
        self.tracking.config(text="Monitor stopped", fg="red")