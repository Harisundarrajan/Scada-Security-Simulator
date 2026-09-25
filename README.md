# SCADA/ICS Security Simulator

A simulation of an Industrial Control System (ICS) environment that demonstrates a real authentication weakness in industrial devices and validates the fix with automated tests. Built to understand how untrusted network traffic should be handled before it reaches control equipment.

**Stack:** Python · Flask · TCP Sockets · Token Authentication · Pytest · Git

---

## The Problem

Industrial control devices frequently accept commands over plain TCP without verifying who sent them. An attacker on the same network can issue stop/start commands to critical equipment. This project reproduces that weakness in a safe, isolated simulator and then proves a patch closes it.

## What It Does

- Simulates a PLC/RTU field device listening on TCP port 5020
- Provides a Flask-based HMI dashboard for viewing device state and firmware version
- Reproduces an authentication-bypass vulnerability in firmware v1.0
- Applies a token-based security patch (v1.1) that rejects unauthorized commands
- Records every access attempt to an audit log for monitoring
- Includes an attack client that simulates unauthorized command injection

## Architecture

Three components communicate over TCP:

1. **PLC/RTU Simulator** (`scada_device.py`) — holds device state, enforces authentication once patched
2. **HMI Dashboard** (`app.py`) — Flask web UI that queries the device and displays status plus a live security event log
3. **Attack Client** (`attacker.py`) — sends both unauthorized and authorized payloads to demonstrate the difference in behavior

Data flow before patching:

    Client -> PLC/RTU -> Command Accepted

Data flow after patching:

    Client -> Auth Middleware -> PLC/RTU -> Command Accepted

Failed authentication returns `DENIED` and is written to the audit log.

## Project Structure

    Scada-Security-Simulator/
    ├── scada_device.py           # Simulated PLC/RTU + authentication logic
    ├── app.py                    # Flask HMI dashboard and audit logging
    ├── attacker.py               # Attack simulation client
    ├── tests/
    │   └── test_scada_device.py  # Automated security regression tests
    ├── requirements.txt
    └── README.md

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

    git clone https://github.com/Harisundarrajan/Scada-Security-Simulator.git
    cd Scada-Security-Simulator
    python -m pip install -r requirements.txt

### Run the Environment

Start the simulated device first, then the dashboard.

    Terminal 1:  python scada_device.py
    Terminal 2:  python app.py

Open http://localhost:5000 to view the console.

### Reproduce the Vulnerability

With the device running at firmware v1.0:

    python attacker.py

The unauthorized STOP command succeeds, taking the device OFFLINE. Apply the security patch from the dashboard, then re-run the attack — the same command is now rejected.

## Testing

Security controls are verified automatically rather than manually.

    python -m pytest tests/ -v

All four tests pass:

| Test | What It Verifies |
|------|------------------|
| Unpatched device accepts any command | Documents the original vulnerability |
| Patched device denies invalid token | Confirms the fix blocks unauthorized access |
| Patched device accepts valid token | Ensures no regression for legitimate users |
| Malformed packet handling | Service remains stable on malformed input |

Test results observed locally: **4 passed**.

## Design Decisions

**Why raw sockets instead of HTTP?** Industrial protocols like Modbus operate at the transport layer. Modeling communication over TCP reflects real field-device behaviour more accurately than wrapping everything in REST.

**Why keep the vulnerable path?** Deleting the vulnerability would remove the point of the exercise. Both states are reachable so the before/after comparison is testable and repeatable.

**Why unit-test the device class directly?** Testing `SCADADevice.handle()` avoids needing a live socket during CI, keeping tests fast and deterministic.

## What I Would Build Next

- Rate limiting and lockout after repeated failed authentications
- Detection logic that flags anomalous command sequences
- Structured JSON logging suitable for ingestion into a SIEM or analytics pipeline
- Support for additional industrial protocol message shapes

## Relevance to Data Engineering

Modern data platforms ingest millions of events per day from distributed, untrusted sources. This project exercises the same fundamentals: ingesting data over raw network protocols, validating inputs before they reach processing logic, and emitting structured logs for observability. Those are the same concerns that govern secure, reliable ingestion pipelines at scale.

---

Built as part of B.Tech Information Technology coursework at Excel Engineering College.
