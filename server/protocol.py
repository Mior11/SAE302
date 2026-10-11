"""Encodage et décodage des messages JSON terminés par un saut de ligne."""
from __future__ import annotations
import json
from typing import Any

MAX_MESSAGE_BYTES = 1_000_000


def encode_message(message: dict[str, Any]) -> bytes:
    """Encode un objet en JSON UTF-8 sur une ligne."""
    return (json.dumps(message, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")


def decode_message(line: bytes) -> dict[str, Any]:
    """Décode une ligne JSON et exige un objet à la racine."""
    if len(line) > MAX_MESSAGE_BYTES:
        raise ValueError("Message trop volumineux")
    data = json.loads(line.decode("utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Le message doit être un objet JSON")
    return data
