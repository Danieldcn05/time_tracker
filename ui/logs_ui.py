import tkinter as tk
from tkinter import ttk
from tracker.database import fetch_logs

class LogsUI(tk.Frame):
    def __init__(self, parent, controller, session,bg=None):
        tk.Frame.__init__(self, parent, bg=bg)
        self.controller = controller
        self.session = session
        
        label = tk.Label(self, text="Logs")
        label.pack(side="top", fill="x", pady=10)

        # Table to display the logs
        self.tree = ttk.Treeview(self, columns=("App", "Start", "End", "Duration"), show="headings")
        self.tree.heading("App", text="Application")
        self.tree.heading("Start", text="Start")
        self.tree.heading("End", text="End")
        self.tree.heading("Duration", text="Duration")
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        button = tk.Button(self, text="Go to Home",
                           command=lambda: controller.show_frame("Home"))
        button.pack()

        
    def load_data(self):
            
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            logs = fetch_logs(self.session)
            for log in logs:
                self.tree.insert("", "end", values=log)
                
            
    def tkraise(self, aboveThis=None):
        self.load_data()
        super().tkraise(aboveThis)