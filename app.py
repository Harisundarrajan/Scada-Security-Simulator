from flask import Flask, render_template_string, request, redirect
import socket, json, datetime

app = Flask(__name__)
HOST, PORT = "127.0.0.1", 5020
LOGS = []

def query_device(payload):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect((HOST, PORT))
            s.sendall(json.dumps(payload).encode())
            return json.loads(s.recv(4096).decode())
    except Exception as e:
        return {"status": "ERROR", "device_status": "OFFLINE", "firmware": "UNKNOWN", "reason": str(e)}

def log(event, level="INFO"):
    LOGS.insert(0, f"[{datetime.datetime.now().strftime('%H:%M:%S')}] [{level}] {event}")
    del LOGS[50:]

PAGE = """
<html>
<head>
<title>SCADA Security Console</title>
<style>
body { font-family: Segoe UI; background: #0d1117; color: #e6edf3; padding: 30px; }
.card { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 20px; margin: 10px 0; }
button { background: #238636; color: white; border: none; padding: 10px 16px; border-radius: 6px; cursor: pointer; margin-right: 8px; }
button.warn { background: #da3633; }
pre { background: #010409; padding: 12px; border-radius: 6px; max-height: 300px; overflow: auto; font-family: monospace; }
.online { color: #3fb950; }
.offline { color: #f85149; }
</style>
</head>
<body>
<h2>SCADA Security Console - HVDC Test Bench</h2>

<div class="card">
    <b>Device Status:</b>
    <span class="{{ 'online' if state.get('device_status') == 'ONLINE' else 'offline' }}">
        {{ state.get('device_status', 'UNKNOWN') }}
    </span><br>
    <b>Firmware:</b> {{ state.get('firmware', 'UNKNOWN') }}<br>
    <b>Security Patch:</b>
    {{ 'Applied' if 'SECURED' in state.get('firmware', '')|string else 'Not Applied' }}
</div>

<div class="card">
    <form method="post" action="/action" style="display:inline">
        <button name="cmd" value="PATCH">Apply Security Patch</button>
    </form>
    <form method="post" action="/action" style="display:inline">
        <button name="cmd" value="STOP" class="warn">Send STOP (authorized)</button>
    </form>
    <form method="post" action="/action" style="display:inline">
        <button name="cmd" value="START">Send START (authorized)</button>
    </form>
</div>

<div class="card">
    <b>Security Event Log</b>
    <pre>{{ log_text }}</pre>
</div>
</body>
</html>"""

@app.route("/")
def index():
    state = query_device({"command": "STATUS", "token": "SCADA-KEY-9931"})
    return render_template_string(PAGE, state=state, log_text="\n".join(LOGS))

@app.route("/action", methods=["POST"])
def action():
    cmd = request.form["cmd"]
    reply = query_device({"command": cmd, "token": "SCADA-KEY-9931"})
    log(f"Operator issued {cmd} -> {reply.get('status')}")
    if cmd == "PATCH":
        log("Firmware patched: authentication enforcement enabled", "SECURITY")
    return redirect("/")

if __name__ == "__main__":
    log("Security console started")
    app.run(port=5000, debug=False)