import tkinter as tk
from tkinter import ttk
from tracker.database import fetch_logs

class LogsUI(tk.Frame):
    def __init__(self, parent, controller, session):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.session = session
        
        label = tk.Label(self, text="Logs")
        label.pack(side="top", fill="x", pady=10)

        # Tabla para mostrar el historial
        self.tree = ttk.Treeview(self, columns=("App", "Inicio", "Fin", "Duración"), show="headings")
        self.tree.heading("App", text="Aplicación")
        self.tree.heading("Inicio", text="Inicio")
        self.tree.heading("Fin", text="Fin")
        self.tree.heading("Duración", text="Duración")
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        button = tk.Button(self, text="Go to Home",
                           command=lambda: controller.show_frame("Home"))
        button.pack()

        self.load_data()

    def load_data(self):
        logs = fetch_logs(self.session)
        for log in logs:
            self.tree.insert("", "end", values=log)