import tkinter as tk
from tkinter import ttk
from tracker.database import fetch_apps, toggle_tracking

class AppsUI(tk.Frame):
    def __init__(self, parent, controller, session):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.session = session

        label = tk.Label(self, text="Apps")
        label.pack(side="top", fill="x", pady=10)
        
        label = tk.Label(self, text="Click en una fila para activar/desactivar el tracking de la aplicación")
        label.pack(side="top", fill="x", pady=10)
        
        # Tabla para mostrar las apps
        self.tree = ttk.Treeview(self, columns=("App","Nombre del Proceso", "Tracking","Tiempo de uso" ), show="headings")
        self.tree.heading("App", text="Aplicación")
        self.tree.heading("Nombre del Proceso", text="Nombre del Proceso")
        self.tree.heading("Tracking", text="Tracking")
        self.tree.heading("Tiempo de uso", text="Tiempo de uso")
        
        self.tree.bind("<ButtonRelease-1>", self.on_row_click)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        

        button = tk.Button(self, text="Go to Home",
                           command=lambda: controller.show_frame("Home"))
        button.pack()
        
        self.load_data()
        
    def on_row_click(self, event):
        item = self.tree.selection()[0]
        process_name = self.tree.item(item, "values")[1]
        toggle_tracking(self.session, process_name)
        self.load_data()    
    
    def load_data(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Fetch and insert new data
        logs = fetch_apps(self.session)
        for log in logs:
            self.tree.insert("", "end", values=log)