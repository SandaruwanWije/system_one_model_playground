import os
import tkinter as tk
from tkinter import messagebox

from game.core.env import load_dotenv, save_env_value

KEY_NAME = "TYPESAFE_API_KEY"


def ensure_api_key():
    load_dotenv()
    if os.environ.get(KEY_NAME, "").strip():
        return True

    key = _ask_for_key()
    if not key:
        return False

    os.environ[KEY_NAME] = key
    save_env_value(KEY_NAME, key)
    return True


def _ask_for_key():
    root = tk.Tk()
    root.title("TypeSafe API Key")
    root.resizable(False, False)
    root.attributes("-topmost", True)

    frame = tk.Frame(root, padx=18, pady=16)
    frame.pack()

    tk.Label(frame, text="TYPESAFE_API_KEY is missing.", font=("Segoe UI", 11, "bold")).pack(anchor="w")
    tk.Label(
        frame,
        text="Paste your key to save it in .env and start the game.",
        font=("Segoe UI", 9),
        fg="#444",
    ).pack(anchor="w", pady=(4, 10))

    value = tk.StringVar()
    entry = tk.Entry(frame, textvariable=value, width=44, show="*", font=("Consolas", 10))
    entry.pack(fill="x")
    entry.focus_set()

    result = {"key": None}

    def submit(_event=None):
        text = value.get().strip()
        if not text:
            messagebox.showwarning("API Key", "Please enter a valid API key.", parent=root)
            return
        result["key"] = text
        root.destroy()

    def cancel():
        root.destroy()

    buttons = tk.Frame(frame)
    buttons.pack(fill="x", pady=(12, 0))
    tk.Button(buttons, text="Cancel", width=10, command=cancel).pack(side="right")
    tk.Button(buttons, text="Save & Start", width=12, command=submit).pack(side="right", padx=(0, 8))

    entry.bind("<Return>", submit)
    root.protocol("WM_DELETE_WINDOW", cancel)
    root.update_idletasks()
    w, h = root.winfo_width(), root.winfo_height()
    x = (root.winfo_screenwidth() - w) // 2
    y = (root.winfo_screenheight() - h) // 3
    root.geometry(f"+{x}+{y}")
    root.mainloop()
    return result["key"]
