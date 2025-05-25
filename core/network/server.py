# core/network/server.py
import socket
import threading
from core.encryption import encrypt_message, decrypt_message

class EchoLockServer:
    def __init__(self, host='0.0.0.0', port=9999, password="EchoLockSecret123!"):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = []
        self.password = password
        print(f"[+] Server running on {host}:{port}")

    def broadcast(self, message, exclude_client=None):
        encrypted = encrypt_message(message, self.password)
        for client in self.clients:
            if client is not exclude_client:
                try:
                    client.send(encrypted.encode())
                except:
                    self.clients.remove(client)

    def handle_client(self, client_socket):
        addr = client_socket.getpeername()
        print(f"[+] New connection from {addr}")
        while True:
            try:
                data = client_socket.recv(4096)
                if not data:
                    break
                encrypted = data.decode()
                message = decrypt_message(encrypted, self.password)
                print(f"[Client {addr}]: {message}")
                self.broadcast(message, exclude_client=client_socket)
            except:
                break

        print(f"[!] Client {addr} disconnected")
        self.clients.remove(client_socket)
        client_socket.close()

    def run(self):
        try:
            while True:
                client_socket, _ = self.server.accept()
                self.clients.append(client_socket)
                thread = threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True)
                thread.start()
        except KeyboardInterrupt:
            print("\n[!] Server shutting down")
            self.server.close()

if __name__ == "__main__":
    # When you run `python -m core.network.server`, this will execute:
    server = EchoLockServer()
    server.run()
