from tracker.database import setup_database, get_session
from ui.main_window import MainWindow
import tkinter as tk

def main():
    # Configurar base de datos
    setup_database()

    # Crear la ventana principal
    root = tk.Tk()
    session = get_session()  # Ensure session is created before passing to MainWindow
    app = MainWindow(root, session)
    root.mainloop()

if __name__ == "__main__":
    main()