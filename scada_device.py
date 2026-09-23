import socket
import json

HOST = "127.0.0.1"
PORT = 5020

class SCADADevice:
    def __init__(self):
        self.status = "ONLINE"
        self.firmware = "1.0.0"
        self.is_patched = False
        self.auth_token = "SCADA-KEY-9931"

    def handle(self, data):
        try:
            msg = json.loads(data.decode())
        except Exception:
            return {"status": "ERROR", "reason": "Malformed packet"}

        cmd = msg.get("command")
        token = msg.get("token")

        # VULNERABILITY in v1.0: accepts any command without authentication
        if not self.is_patched:
            return self.execute(cmd)

        # PATCHED v1.1: requires valid token
        if token != self.auth_token:
            return {"status": "DENIED", "reason": "Unauthorized command blocked"}
        return self.execute(cmd)

    def execute(self, cmd):
        if cmd == "STOP":
            self.status = "OFFLINE"
        elif cmd == "START":
            self.status = "ONLINE"
        elif cmd == "PATCH":
            self.firmware = "1.1.0-SECURED"
            self.is_patched = True
            return {"status": "OK", "firmware": self.firmware}
        elif cmd == "STATUS":
            pass  # continue to return status
        else:
            return {"status": "ERROR", "reason": "Unknown command"}
        return {"status": "OK", "device_status": self.status, "firmware": self.firmware}

def main():
    dev = SCADADevice()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"[PLC] Device online | Firmware {dev.firmware} | Port {PORT}")
        print("[PLC] Waiting for commands...")
        while True:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(4096)
                if data:
                    reply = dev.handle(data)
                    print(f"[PLC] {data.decode()} -> {reply}")
                    conn.sendall(json.dumps(reply).encode())

if __name__ == "__main__":
    main()