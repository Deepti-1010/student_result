import tkinter as tk
from ui import StudentApp

def main():
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
