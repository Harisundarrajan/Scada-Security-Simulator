import socket
import json

HOST, PORT = "127.0.0.1", 5020

def send(payload):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(json.dumps(payload).encode())
        print("Response:", s.recv(4096).decode())

print("--- ATTACK 1: Unauthorized STOP command (no token) ---")
send({"command": "STOP"})

print("\n--- LEGITIMATE: Authorized START command (with token) ---")
send({"command": "START", "token": "SCADA-KEY-9931"})

print("\n--- QUERY: Check device status ---")
send({"command": "STATUS", "token": "SCADA-KEY-9931"})