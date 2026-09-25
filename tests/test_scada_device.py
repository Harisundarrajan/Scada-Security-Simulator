import unittest
import json
from sys import path
from os.path import dirname as dir
import sys

# Add project root to path so we can import scada_device
sys.path.insert(0, dir(dir(__file__)))
from scada_device import SCADADevice

class TestSCADADevice(unittest.TestCase):
    def setUp(self):
        """Reset device to a clean state for each test."""
        self.device = SCADADevice()

    def test_unpatched_device_accepts_any_command(self):
        """Verify the VULNERABILITY: Before patching, no token is needed."""
        payload = {"command": "STOP"}
        response = self.device.handle(json.dumps(payload).encode())
        self.assertEqual(response["status"], "OK")
        self.assertEqual(self.device.status, "OFFLINE")

    def test_patched_device_denies_invalid_token(self):
        """Verify the FIX: After patching, invalid tokens are blocked."""
        patch_payload = {"command": "PATCH", "token": "SCADA-KEY-9931"}
        self.device.handle(json.dumps(patch_payload).encode())

        attack_payload = {"command": "STOP", "token": "HACKER-KEY"}
        response = self.device.handle(json.dumps(attack_payload).encode())
        self.assertEqual(response["status"], "DENIED")

    def test_patched_device_accepts_valid_token(self):
        """Verify: Patched device still works for authorized users."""
        self.device.handle(json.dumps({"command": "PATCH", "token": "SCADA-KEY-9931"}).encode())

        valid_payload = {"command": "START", "token": "SCADA-KEY-9931"}
        response = self.device.handle(json.dumps(valid_payload).encode())
        self.assertEqual(response["status"], "OK")
        self.assertEqual(self.device.status, "ONLINE")

    def test_malformed_packet_handling(self):
        """Verify security: System doesn't crash on bad data."""
        bad_data = b"this is not json!!!"
        response = self.device.handle(bad_data)
        self.assertEqual(response["status"], "ERROR")
        self.assertIn("Malformed", response["reason"])

if __name__ == '__main__':
    unittest.main()
