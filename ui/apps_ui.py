import tkinter as tk
from tkinter import ttk
from tracker.database import fetch_apps

class AppsUI(tk.Frame):
    def __init__(self, parent, controller, session):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.session = session

        label = tk.Label(self, text="Apps")
        label.pack(side="top", fill="x", pady=10)
        
        
        # Tabla para mostrar las apps
        self.tree = ttk.Treeview(self, columns=("App", "Tiempo de uso"), show="headings")
        self.tree.heading("App", text="Aplicación")
        self.tree.heading("Tiempo de uso", text="Tiempo de uso")
        self.tree.pack(fill=tk.BOTH, expand=True)

        button = tk.Button(self, text="Go to Home",
                           command=lambda: controller.show_frame("Home"))
        button.pack()
        
        
        self.load_data()
        
    def load_data(self):
        logs = fetch_apps(self.session)
        for log in logs:
            self.tree.insert("", "end", values=log)