from tracker.database import setup_database, get_session
from ui.main_window import MainWindow
import tkinter as tk

def main():
    
    setup_database()

    
    root = tk.Tk()
    session = get_session()  # Ensure session is created before passing to MainWindow
    app = MainWindow(root, session)
    root.mainloop()

if __name__ == "__main__":
    main()