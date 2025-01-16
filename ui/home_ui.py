import tkinter as tk
from tkinter import ttk

class Home(tk.Frame):
    def __init__(self, parent, controller, session):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.session = session

        label = tk.Label(self, text="HOME")
        label.pack(side="top", fill="x", pady=10)

        button = tk.Button(self, text="See Logs",
                           command=lambda: controller.show_frame("LogsUI"))
        
        button2 = tk.Button(self, text="See Apps",
                           command=lambda: controller.show_frame("AppsUI"))
        
        button3 = tk.Button(self, text="Add App",
                            command=lambda: controller.show_frame("AddAppUI"))
        
        button.pack()
        button2.pack()
        button3.pack()