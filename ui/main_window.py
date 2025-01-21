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
        
        # Set background color
        self.bg_color = "#F6F8FA"  # Change this to your desired color

        # Main container
        self.container = tk.Frame(root, bg=self.bg_color)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (LogsUI, Home, AppsUI, AddAppUI):  # ADD NEW VIEWS HERE
            page_name = F.__name__
            frame = F(parent=self.container, controller=self, session=session, bg=self.bg_color)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Home")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

        # Configure the container to expand and fill all available space
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)