import tkinter as tk
from tkinter import ttk
from ui.logs_ui import LogsUI
from ui.home_ui import Home
from ui.apps_ui import AppsUI
from ui.add_app_ui import AddAppUI

class MainWindow:
    def __init__(self, root, session):
        self.root = root
        self.session = session
        self.root.title("Time Tracker")
        self.root.resizable(False, False)
        self.root.geometry("1200x700")

        # Contenedor principal
        self.container = tk.Frame(root)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (LogsUI, Home, AppsUI, AddAppUI):  # AÑADIR NUEVAS VISTAS AQUÍ
            page_name = F.__name__
            frame = F(parent=self.container, controller=self, session=session)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Home")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

        # Configurar el contenedor para que se expanda y llene todo el espacio disponible
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)