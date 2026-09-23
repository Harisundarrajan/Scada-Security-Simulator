**SCADA Security Simulator**

A hands-on project that brings **Industrial Cybersecurity** to life!  
This simulator demonstrates how a critical SCADA device can be vulnerable — and how a simple security patch can stop an attack, while keeping the system running smoothly.

Built with **Python**, **Flask**, and **sockets**, this project models real-world OT security workflows: vulnerability discovery, patch development, validation, and audit logging.

---

**What It Does**

- Simulates a **SCADA PLC/RTU device** listening on TCP port 5020
- Shows a real **authentication bypass vulnerability** in firmware v1.0
- Implements a **token-based security patch** (v1.1) that blocks unauthorized commands
- Provides a **Flask web dashboard** to monitor device status, firmware, and security logs
- Runs **automated attack tests** before and after patching to prove the fix works

---

**Project Files**

| File | What It Does |
|------|--------------|
| scada_device.py | Simulates the SCADA field device (PLC/RTU) |
| app.py | Web dashboard (HMI + security console) |
| attacker.py | Test script that sends authorized and unauthorized commands |

---


