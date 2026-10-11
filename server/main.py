"""Serveur TCP pédagogique pour les messages de la simulation."""
from __future__ import annotations
import argparse
import json
import logging
import select
import socket
from server.protocol import decode_message, encode_message, MAX_MESSAGE_BYTES

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
LOG = logging.getLogger("carrefour.server")


def handle_message(message: dict) -> dict:
    """Traite les commandes applicatives sans prétendre commander un vrai carrefour."""
    kind = message.get("type")
    if kind == "ping":
        return {"type": "pong", "payload": {"status": "ok"}}
    if kind == "status":
        return {"type": "status", "payload": {"service": "carrefour-connecte", "mode": "prototype"}}
    if kind == "priority_request":
        payload = message.get("payload", {})
        direction = payload.get("direction", "inconnue") if isinstance(payload, dict) else "inconnue"
        return {"type": "priority_ack", "payload": {"accepted": True, "direction": direction, "note": "Accusé de réception de démonstration uniquement"}}
    return {"type": "error", "payload": {"message": "Type de message inconnu"}}


def serve(host: str, port: int) -> None:
    """Boucle select() sur une socket d'écoute et les clients connectés."""
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((host, port)); listener.listen(); listener.setblocking(False)
    sockets = {listener}; buffers: dict[socket.socket, bytearray] = {}
    LOG.info("Serveur à l'écoute sur %s:%d", host, port)
    try:
        while True:
            readable, _, exceptional = select.select(list(sockets), [], list(sockets), 1.0)
            for sock in readable:
                if sock is listener:
                    client, address = listener.accept(); client.setblocking(False)
                    sockets.add(client); buffers[client] = bytearray()
                    LOG.info("Connexion de %s:%d", *address); continue
                try:
                    chunk = sock.recv(4096)
                    if not chunk:
                        sockets.discard(sock); buffers.pop(sock, None); sock.close(); continue
                    buf = buffers[sock]; buf.extend(chunk)
                    if len(buf) > MAX_MESSAGE_BYTES and b"\n" not in buf:
                        raise ValueError("Message trop volumineux")
                    while b"\n" in buf:
                        raw, _, rest = buf.partition(b"\n"); buffers[sock] = bytearray(rest); buf = buffers[sock]
                        response = handle_message(decode_message(raw))
                        sock.sendall(encode_message(response))
                except (OSError, ValueError, UnicodeDecodeError, json.JSONDecodeError) as exc:
                    LOG.warning("Client retiré après erreur de protocole : %s", exc)
                    sockets.discard(sock); buffers.pop(sock, None); sock.close()
            for sock in exceptional:
                if sock is not listener:
                    sockets.discard(sock); buffers.pop(sock, None); sock.close()
    finally:
        for sock in sockets: sock.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1", help="Adresse d'écoute (défaut : localhost)")
    parser.add_argument("--port", type=int, default=5050, help="Port TCP (défaut : 5050)")
    args = parser.parse_args(); serve(args.host, args.port)

if __name__ == "__main__":
    main()
