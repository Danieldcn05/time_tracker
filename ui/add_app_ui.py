import tkinter as tk
from tkinter import ttk
from tracker.database import create_app, fetch_names, get_app_by_name
import json
import os

class AddAppUI(tk.Frame):
    def __init__(self, parent, controller, session):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.session = session

        # Obtener la ruta del archivo JSON
        json_path = os.path.join(os.path.dirname(__file__), 'apps.json')

        # Cargar el archivo JSON
        with open(json_path, 'r') as f:
            self.app_to_ps_name = json.load(f)

        label = tk.Label(self, text="Agregar App")
        label.pack(side="top", fill="x", pady=10)
        
        """
        # Entradas de texto para procesos personalizados
        
        app_name_label = tk.Label(self, text="Nombre de la App")
        app_name_label.pack()
        
        self.app_name = tk.Entry(self)
        self.app_name.pack()
        
        ps_name_label = tk.Label(self, text="Nombre del Proceso")
        ps_name_label.pack()
        
        self.ps_name = tk.Entry(self)
        self.ps_name.pack()
        """
        
        # Menú desplegable
        options_label = tk.Label(self, text="Opciones")
        options_label.pack()
        
        self.app_name = ttk.Combobox(self, values=list(self.app_to_ps_name.keys()), state='readonly')
        self.app_name.current(0) 
        self.app_name.pack()
        
        button = tk.Button(self, text="Agregar",
                           command=self.add_app)
        button.pack()
        
        self.console = tk.Label(self, text="Pulsa en 'Agregar' para añadir la app")
        self.console.pack()
        
        button = tk.Button(self, text="Go to Home",
                           command=lambda: controller.show_frame("Home"))
        button.pack()
    
    def add_app(self):
        trackered_apps = fetch_names(self.session)
        app_name = self.app_name.get()
        if app_name not in trackered_apps:
            ps_name = self.app_to_ps_name.get(app_name, "unknown")
            create_app(self.session, app_name, ps_name)
            self.console.config(text="App añadida correctamente", fg="green")
        else:
            app = get_app_by_name(self.session, app_name)
            if not app.tracking:
                app.tracking = True
                self.session.commit()
                self.console.config(text="App añadida correctamente", fg="green")
            else:
                self.console.config(text="La app ya ha sido añadida", fg="red")