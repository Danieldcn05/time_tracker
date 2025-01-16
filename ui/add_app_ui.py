import tkinter as tk
from tkinter import ttk
from tracker.database import create_app

class AddAppUI(tk.Frame):
    def __init__(self, parent, controller, session):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.session = session

        label = tk.Label(self, text="Agregar App")
        label.pack(side="top", fill="x", pady=10)
        
        app_name_label = tk.Label(self, text="Nombre de la App")
        app_name_label.pack()
        

        self.app_name = tk.Entry(self)
        self.app_name.pack()
        
        ps_name_label = tk.Label(self, text="Nombre del Proceso")
        ps_name_label.pack()
        
        self.ps_name = tk.Entry(self)
        self.ps_name.pack()
        
        button = tk.Button(self, text="Agregar",
                           command=self.add_app)
        button.pack()
        
        button = tk.Button(self, text="Go to Home",
                           command=lambda: controller.show_frame("Home"))
        button.pack()
    
    def add_app(self):
        app_name = self.app_name.get()
        ps_name = self.ps_name.get()
        create_app(self.session, app_name, ps_name)
        self.app_name.delete(0, tk.END)
        self.ps_name.delete(0, tk.END)
        print("App agregada")