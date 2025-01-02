import tkinter as tk
from tkinter import ttk
from ui.logs_ui import LogsUI
from ui.home_ui import Home
from ui.apps_ui import AppsUI

class MainWindow:
    def __init__(self, root, session):
        self.root = root
        self.session = session
        self.root.title("Time Tracker")

        # Contenedor principal
        self.container = tk.Frame(root)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (LogsUI, Home, AppsUI):  # AÑADIR NUEVAS VISTAS AQUÍ
            page_name = F.__name__
            frame = F(parent=self.container, controller=self, session=session)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Home")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()