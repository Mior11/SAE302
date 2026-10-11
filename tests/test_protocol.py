"""Tests unitaires du protocole et du routage des commandes."""
import unittest
from server.protocol import encode_message, decode_message
from server.main import handle_message


class ProtocolTests(unittest.TestCase):
    def test_round_trip_unicode(self):
        message = {"type": "status", "payload": {"label": "véhicule d'urgence"}}
        self.assertEqual(decode_message(encode_message(message).rstrip(b"\n")), message)

    def test_reject_non_object(self):
        with self.assertRaises(ValueError):
            decode_message(b"[1,2,3]")

    def test_ping(self):
        self.assertEqual(handle_message({"type": "ping"})["type"], "pong")

    def test_unknown_type(self):
        self.assertEqual(handle_message({"type": "unknown"})["type"], "error")

if __name__ == "__main__":
    unittest.main()
