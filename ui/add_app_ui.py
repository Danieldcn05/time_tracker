import tkinter as tk
from tkinter import ttk
from tracker.database import create_app, fetch_names, get_app_by_name
import json
import os

class AddAppUI(tk.Frame):
    def __init__(self, parent, controller, session, bg=None):
        tk.Frame.__init__(self, parent,bg=bg)
        self.controller = controller
        self.session = session

        # Get the path of the JSON file
        json_path = os.path.join(os.path.dirname(__file__), 'apps.json')

        # Load the JSON file
        with open(json_path, 'r') as f:
            self.app_to_ps_name = json.load(f)

        label = tk.Label(self, text="Add App")
        label.pack(side="top", fill="x", pady=10)
        
        """
        # Text entries for custom processes
        
        app_name_label = tk.Label(self, text="App Name")
        app_name_label.pack()
        
        self.app_name = tk.Entry(self)
        self.app_name.pack()
        
        ps_name_label = tk.Label(self, text="Process Name")
        ps_name_label.pack()
        
        self.ps_name = tk.Entry(self)
        self.ps_name.pack()
        """
        
        # Dropdown menu
        options_label = tk.Label(self, text="Options")
        options_label.pack()
        
        self.app_name = ttk.Combobox(self, values=list(self.app_to_ps_name.keys()), state='readonly')
        self.app_name.current(0) 
        self.app_name.pack()
        
        button = tk.Button(self, text="Add",
                           command=self.add_app)
        button.pack()
        
        self.console = tk.Label(self, text="Press 'Add' to add the app")
        self.console.pack()
        
        button = tk.Button(self, text="Back to Apps",
                           command=lambda: controller.show_frame("AppsUI"))
        button.pack()
    
    def add_app(self):
        tracked_apps = fetch_names(self.session)
        app_name = self.app_name.get()
        if app_name not in tracked_apps:
            ps_name = self.app_to_ps_name.get(app_name, "unknown")
            create_app(self.session, app_name, ps_name)
            self.console.config(text="App added successfully", fg="green")
        else:
            app = get_app_by_name(self.session, app_name)
            if not app.tracking:
                app.tracking = True
                self.session.commit()
                self.console.config(text="App added successfully", fg="green")
            else:
                self.console.config(text="The app has already been added", fg="red")