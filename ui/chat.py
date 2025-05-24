import tkinter as tk
from core.encryption import encrypt_message, decrypt_message
import os
from datetime import datetime  # 🔥 Add this line for timestamps

CHAT_PASSWORD = "EchoLockSecret123!"
HISTORY_FILE = os.path.join("logs", "chat_logs.txt")
os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)

def start_chat_window():
    window = tk.Tk()
    window.title("EchoLock - Secure Chat")
    window.geometry("500x400")
    window.configure(bg="#1e1e1e")

    # Frame for scrollable text box
    chat_frame = tk.Frame(window)
    chat_frame.pack(pady=10)

    scrollbar = tk.Scrollbar(chat_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    chat_display = tk.Text(
        chat_frame,
        height=20,
        width=58,
        bg="#2e2e2e",
        fg="#39ff14",
        font=("Consolas", 10),
        yscrollcommand=scrollbar.set
    )
    chat_display.pack(side=tk.LEFT)
    scrollbar.config(command=chat_display.yview)

    # Load chat history (without timestamps)
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                # Ignore timestamp when displaying in UI
                if line.startswith("["):
                    line = line[line.find("]") + 2:]  # remove timestamp and space
                chat_display.insert(tk.END, line)

    message_entry = tk.Entry(window, width=45, font=("Consolas", 10), bg="#333", fg="#fff")
    message_entry.pack(side=tk.LEFT, padx=(10, 0), pady=10)

    def send_message():
        message = message_entry.get()
        if message:
            encrypted = encrypt_message(message, CHAT_PASSWORD)
            decrypted = decrypt_message(encrypted, CHAT_PASSWORD)

            # ➕ Insert without timestamp into UI
            display_text = f"You (Encrypted): {encrypted}\nYou (Decrypted): {decrypted}\n\n"
            chat_display.insert(tk.END, display_text)
            message_entry.delete(0, tk.END)

            # 🕒 Write to file with timestamp
            timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
            file_text = (
                f"{timestamp} You (Encrypted): {encrypted}\n"
                f"{timestamp} You (Decrypted): {decrypted}\n\n"
            )
            with open(HISTORY_FILE, "a", encoding="utf-8") as f:
                f.write(file_text)

            chat_display.see(tk.END)  # Auto-scroll to bottom

    send_button = tk.Button(window, text="Send", command=send_message, bg="#39ff14", fg="#000", font=("Consolas", 10))
    send_button.pack(side=tk.LEFT, padx=10, pady=10)

    window.mainloop()
