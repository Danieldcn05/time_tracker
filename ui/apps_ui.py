import tkinter as tk
from tkinter import ttk
from tracker.database import fetch_apps, toggle_tracking

class AppsUI(tk.Frame):
    def __init__(self, parent, controller, session, bg=None):
        tk.Frame.__init__(self, parent ,bg=bg)
        self.controller = controller
        self.session = session

        label = tk.Label(self, text="Apps")
        label.pack(side="top", fill="x", pady=10)
        
        label = tk.Label(self, text="Click on a row to enable/disable app tracking")
        label.pack(side="top", fill="x", pady=10)
        
        # Table to display the apps
        self.tree = ttk.Treeview(self, columns=("App", "Process Name", "Tracking", "Usage Time"), show="headings")
        self.tree.heading("App", text="Application")
        self.tree.heading("Process Name", text="Process Name")
        self.tree.heading("Tracking", text="Tracking")
        self.tree.heading("Usage Time", text="Usage Time")
        
        self.tree.bind("<ButtonRelease-1>", self.on_row_click)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        button = tk.Button(self, text="Go to Home",
                           command=lambda: controller.show_frame("Home"))
        
        button2 = tk.Button(self, text="Add App",
                            command=lambda: controller.show_frame("AddAppUI"))
        
        button.pack()
        button2.pack()
        
    def on_row_click(self, event):
        item = self.tree.selection()[0]
        process_name = self.tree.item(item, "values")[1]
        toggle_tracking(self.session, process_name)
        self.load_data()    
    
    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        logs = fetch_apps(self.session)
        for log in logs:
            self.tree.insert("", "end", values=log)
    
    def tkraise(self, aboveThis=None):
        self.load_data()
        super().tkraise(aboveThis)
