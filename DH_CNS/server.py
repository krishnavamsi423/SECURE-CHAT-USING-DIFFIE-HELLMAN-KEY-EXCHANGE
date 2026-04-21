import socket
import threading
from utils import *

HOST = '0.0.0.0'
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(2)

print("Server running... Waiting for clients...")

clients = []

# Accept 2 clients
while len(clients) < 2:
    conn, addr = server_socket.accept()
    print("Connected:", addr)
    clients.append(conn)

# 🔑 Key Exchange
public_keys = []

for conn in clients:
    public_keys.append(int(conn.recv(1024).decode()))

clients[0].send((str(public_keys[1]) + "\n").encode())
clients[1].send((str(public_keys[0]) + "\n").encode())

# Shared key (only for display)
server_private = generate_private_key()
shared_key = generate_shared_key(public_keys[0], server_private)

print("\n--- Diffie-Hellman ---")
print(f"p={p}, g={g}")
print(f"Public keys: {public_keys}")
print(f"Shared key (demo): {shared_key}")
print("----------------------\n")

# 🔁 HANDLE CLIENT
def handle_client(sender, receiver):
    buffer = ""
    while True:
        try:
            data = sender.recv(1024).decode()
            if not data:
                break

            buffer += data

            while "\n" in buffer:
                msg, buffer = buffer.split("\n", 1)

# split encrypted + original
                enc_msg, orig_msg = msg.split("||")

                # 🔓 Decryption display
                print("\n--- Message Relay ---")
                print(f"Encrypted: {enc_msg}")
                # print(f"ASCII: {[ord(c) for c in enc_msg]}")
                print(f"Decrypted : {orig_msg}")
                print("----------------------")

                # Forward message
                receiver.send((enc_msg + "\n").encode())

        except:
            break

# Threads
threading.Thread(target=handle_client, args=(clients[0], clients[1]), daemon=True).start()
threading.Thread(target=handle_client, args=(clients[1], clients[0]), daemon=True).start()

# Keep server alive
while True:
    pass