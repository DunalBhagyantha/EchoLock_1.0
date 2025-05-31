# core/network/client.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


import socket
import threading
from core.encryption import encrypt_message, decrypt_message

class EchoLockClient:
    def __init__(self, host='127.0.0.1', port=9999, password="EchoLockSecret123!"):
        self.server = (host, port)
        self.password = password
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.client.connect(self.server)
            print("[+] Connected to server!")
            threading.Thread(target=self.receive_messages, daemon=True).start()
            self.send_loop()
        except Exception as e:
            print(f"[!] Connection failed: {e}")

    def send_message(self, message):
        encrypted = encrypt_message(message, self.password)
        self.client.send(encrypted.encode())

    def receive_messages(self):
        while True:
            try:
                encrypted = self.client.recv(4096).decode()
                decrypted = decrypt_message(encrypted, self.password)
                print(f"\n[Server]: {decrypted}")
            except:
                print("[!] Connection closed.")
                break

    def send_loop(self):
        while True:
            try:
                message = input("You: ")
                if message.lower() == "exit":
                    break
                self.send_message(message)
            except KeyboardInterrupt:
                break
        self.client.close()

#Run if executed directly

if __name__ == "__main__":
    EchoLockClient().connect()
