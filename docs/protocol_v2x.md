# Protocole réseau — prototype

Le serveur écoute en TCP. Chaque message est un objet JSON encodé en UTF-8, terminé par `\n` (JSON-lines). Les clients peuvent envoyer plusieurs messages sur une connexion. Le serveur répond par un objet JSON par ligne.

## Exemples

```json
{"type":"ping","payload":{}}
{"type":"priority_request","payload":{"direction":"nord","vehicle_id":"ambulance-1"}}
```

Réponse `priority_ack` :

```json
{"type":"priority_ack","payload":{"accepted":true,"direction":"nord","note":"Accusé de réception de démonstration uniquement"}}
```

Le prototype limite un message à 1 Mo. Les types connus sont `ping`, `status` et `priority_request`. La commande de priorité ne commande aucun équipement physique ; elle sert uniquement à démontrer un échange réseau. Une future version devra ajouter authentification, validation de schéma, délais d'expiration, journalisation et tests de charge.
