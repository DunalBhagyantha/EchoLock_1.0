# ui/chat_ui.py
import tkinter as tk
from core.encryption import encrypt_message, decrypt_message
import os
from datetime import datetime

CHAT_PASSWORD = "EchoLockSecret123!"
HISTORY_FILE = os.path.join("logs", "chat_logs.txt")
os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)

def start_chat_window():
    window = tk.Tk()
    window.title("EchoLock - Secure Chat")
    window.geometry("820x580") 
    window.configure(bg="#0d1117")

    # Title Label
    title_label = tk.Label(
        window,
        text="💬 EchoLock - Secure Chat",
        font=("Consolas", 16, "bold"),
        fg="#39ff14",
        bg="#0d1117",
        pady=10
    )
    title_label.pack()

    # Frame for chat display
    chat_frame = tk.Frame(window, bg="#0d1117")
    chat_frame.pack(pady=(0, 10), padx=20)

    scrollbar = tk.Scrollbar(chat_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    chat_display = tk.Text(
        chat_frame,
        height=25,
        width=95,
        bg="#161b22",
        fg="#39ff14",
        font=("Consolas", 11),
        yscrollcommand=scrollbar.set,
        wrap=tk.WORD,
        state=tk.NORMAL
    )
    chat_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=chat_display.yview)

    # Load history
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("["):
                    line = line[line.find("]") + 2:]
                chat_display.insert(tk.END, line)

    # Bottom Frame
    bottom_frame = tk.Frame(window, bg="#0d1117")
    bottom_frame.pack(pady=(0, 20), padx=20, fill=tk.X)

    message_entry = tk.Entry(
        bottom_frame,
        width=80,
        font=("Consolas", 11),
        bg="#21262d",
        fg="#ffffff",
        insertbackground="#ffffff"
    )
    message_entry.pack(side=tk.LEFT, padx=(0, 10), ipady=6)

    def send_message():
        message = message_entry.get()
        if message:
            encrypted = encrypt_message(message, CHAT_PASSWORD)
            decrypted = decrypt_message(encrypted, CHAT_PASSWORD)

            display_text = f"You (Encrypted): {encrypted}\nYou (Decrypted): {decrypted}\n\n"
            chat_display.insert(tk.END, display_text)
            chat_display.see(tk.END)

            timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
            file_text = (
                f"{timestamp} You (Encrypted): {encrypted}\n"
                f"{timestamp} You (Decrypted): {decrypted}\n\n"
            )
            with open(HISTORY_FILE, "a", encoding="utf-8") as f:
                f.write(file_text)

            message_entry.delete(0, tk.END)

    send_button = tk.Button(
        bottom_frame,
        text="Send",
        command=send_message,
        bg="#39ff14",
        fg="#000",
        font=("Consolas", 11, "bold"),
        width=10,
        relief=tk.FLAT,
        cursor="hand2"
    )
    send_button.pack(side=tk.LEFT)

    window.mainloop()
