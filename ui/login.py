# ui/login.py
import tkinter as tk
from tkinter import messagebox

def show_login(on_success):
    def attempt_login():
        username = entry_username.get()
        password = entry_password.get()
        if username and password:
            login_window.destroy()
            on_success()
        else:
            messagebox.showerror("Login Failed", "Please enter both username and password.")

    login_window = tk.Tk()
    login_window.title("EchoLock - Login")
    login_window.geometry("300x180")
    login_window.configure(bg="#1e1e1e")

    tk.Label(login_window, text="Username:", bg="#1e1e1e", fg="white").pack(pady=5)
    entry_username = tk.Entry(login_window)
    entry_username.pack(pady=5)

    tk.Label(login_window, text="Password:", bg="#1e1e1e", fg="white").pack(pady=5)
    entry_password = tk.Entry(login_window, show="*")
    entry_password.pack(pady=5)

    tk.Button(login_window, text="Login", command=attempt_login, bg="#0078d4", fg="white").pack(pady=10)

    login_window.mainloop()
