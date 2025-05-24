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
    login_window.geometry("400x240")  # 📏 Increased size
    login_window.configure(bg="#0f0f0f")  # 🖤 Darker background

    # Fonts & colors
    font = ("Consolas", 11)
    label_fg = "#39ff14"  # 💚 HackTheBox green
    button_bg = "#39ff14"
    button_fg = "#0f0f0f"

    tk.Label(login_window, text="Username:", bg="#0f0f0f", fg=label_fg, font=font).pack(pady=8)
    entry_username = tk.Entry(login_window, font=font, bg="#1e1e1e", fg="white", insertbackground="white")
    entry_username.pack(pady=5, ipadx=5, ipady=3)

    tk.Label(login_window, text="Password:", bg="#0f0f0f", fg=label_fg, font=font).pack(pady=8)
    entry_password = tk.Entry(login_window, show="*", font=font, bg="#1e1e1e", fg="white", insertbackground="white")
    entry_password.pack(pady=5, ipadx=5, ipady=3)

    tk.Button(login_window, text="Login", command=attempt_login,
              bg=button_bg, fg=button_fg, font=("Consolas", 11, "bold"),
              relief=tk.FLAT, padx=10, pady=4).pack(pady=15)

    login_window.mainloop()
