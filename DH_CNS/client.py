import socket
import threading
import tkinter as tk
from utils import *

HOST = "127.0.0.1"   # 🔁 change to server IP for LAN
PORT = 12345

client = socket.socket()
client.connect((HOST, PORT))

# 🔑 Diffie-Hellman
private_key = generate_private_key()
public_key = generate_public_key(private_key)

client.send(str(public_key).encode())

# Receive server public key (with delimiter)
buffer = ""
while "\n" not in buffer:
    buffer += client.recv(1024).decode()

server_public, buffer = buffer.split("\n", 1)
shared_key = generate_shared_key(int(server_public), private_key)

print("Shared Key:", shared_key)

# GUI
root = tk.Tk()
root.title("Secure Chat")

chat_box = tk.Text(root, height=20, width=50)
chat_box.pack()

entry = tk.Entry(root, width=40)
entry.pack(side=tk.LEFT)

# Validation
def validate_input(msg):
    if not msg.strip():
        return "error", "❌ Error: Empty message not allowed"
    if len(msg) > 20:
        return "warning", "⚠ Warning: Message too long"
    return "ok", None

def send_message():
    msg = entry.get()

    status, feedback = validate_input(msg)

    if status == "error":
        chat_box.insert(tk.END, feedback + "\n")
        entry.delete(0, tk.END)
        return

    if status == "warning":
        chat_box.insert(tk.END, feedback + "\n")

    enc = encrypt(msg, shared_key)

# send BOTH encrypted + original
    client.send((enc + "||" + msg + "\n").encode())

    chat_box.insert(tk.END, "You: " + msg + "\n")
    entry.delete(0, tk.END)

send_btn = tk.Button(root, text="Send", command=send_message)
send_btn.pack(side=tk.LEFT)

# Receive messages
recv_buffer = ""

def receive():
    global recv_buffer
    while True:
        try:
            data = client.recv(1024).decode()
            recv_buffer += data

            while "\n" in recv_buffer:
                msg, recv_buffer = recv_buffer.split("\n", 1)

                dec = decrypt(msg, shared_key)
                chat_box.insert(tk.END, "Other: " + dec + "\n")

        except:
            break

threading.Thread(target=receive, daemon=True).start()

root.mainloop()