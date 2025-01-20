import tkinter as tk
import subprocess

class Home(tk.Frame):
    def __init__(self, parent, controller, session):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.session = session
        self.monitor_running = False

        label = tk.Label(self, text="HOME")
        label.pack(side="top", fill="x", pady=10)

        button = tk.Button(self, text="See Logs",
                           command=lambda: controller.show_frame("LogsUI"))
        
        button2 = tk.Button(self, text="See Apps",
                           command=lambda: controller.show_frame("AppsUI"))
        
        button3 = tk.Button(self, text="Add App",
                            command=lambda: controller.show_frame("AddAppUI"))
        
        button4 = tk.Button(self, text="Toggle Monitor",
                            command=self.toggle_monitor)
        
        self.tracking = tk.Label(self, text="Monitor is not running", fg="red")
        
        
        
        button.pack()
        button2.pack()
        button3.pack()
        button4.pack()
        self.tracking.pack()

    def toggle_monitor(self):
        self.monitor_running = not self.monitor_running
        self.tracking.config(text="Monitor is running" if self.monitor_running else "Monitor is not running", fg="green" if self.monitor_running else "red")
    