import sys
import tkinter as tk
from tkinter import messagebox

from game.core.api_key import ensure_api_key


def main():
    if not ensure_api_key():
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("JEV Snake", "API key is required to start the game.")
        root.destroy()
        sys.exit(1)

    from game.app import App

    App().run()


if __name__ == "__main__":
    main()
