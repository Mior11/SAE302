# SAÉ 3.02 — Carrefour connecté

**Groupe : A113**  
**Étudiants :** BENCHEKCHOU Nail-Omar et LEMASSON Ewan

## Objectif
Prototype pédagogique d'un carrefour intelligent qui simule du trafic et accorde temporairement une priorité à un véhicule d'urgence. L'application graphique est écrite en Python avec PySide6. Un serveur TCP échange des messages JSON délimités par des retours à la ligne. Le schéma SQL MariaDB est fourni séparément.

> **État du projet :** base de travail à valider et enrichir. Le mode simulation graphique est local. Le client réseau et le serveur sont des composants séparés ; leur intégration complète et la connexion MariaDB restent à réaliser. Ce prototype ne doit jamais être utilisé pour contrôler un vrai carrefour ni pour prendre des décisions de circulation réelles.

## Prérequis
- Python 3.10 ou plus récent
- Linux, Windows ou macOS pour l'interface
- `pip` et un environnement virtuel
- MariaDB uniquement pour la partie base de données (optionnelle pour lancer la démo graphique)

## Installation
```bash
python -m venv .venv
# Linux/macOS : source .venv/bin/activate
# Windows : .venv\\Scripts\\activate
python -m pip install -r requirements.txt
```

## Lancer la simulation graphique
```bash
python -m client.main
```

## Lancer le serveur TCP
Dans un autre terminal :
```bash
python -m server.main --host 0.0.0.0 --port 5050
```
Le serveur reçoit une ligne JSON par message et renvoie une réponse JSON par ligne. Exemple : `{"type":"ping","payload":{}}`.

## Base de données
Le script `database/schema.sql` crée les tables de base. Suivre `docs/deployment_vms.md` pour le déploiement sur deux VM Linux. La connexion applicative à MariaDB n'est pas encore intégrée dans ce prototype.

## Tests
```bash
python -m unittest discover -s tests -v
```

## Architecture
- `client/` : interface PySide6 et moteur de simulation local
- `server/` : serveur TCP multiclient avec protocole JSON-lines
- `database/` : schéma SQL MariaDB
- `docs/` : protocole et notes de déploiement
- `tests/` : tests unitaires du protocole

## Livrables et bilan
`Bilan_Projet.pdf` et `IAGraphie.pdf` doivent être complétés avec les observations, comptes rendus et temps réellement mesurés par le groupe. Ne pas inventer les écarts entre planning prévisionnel et réel. Si les PDF ne sont pas encore présents dans le dépôt, les générer à partir des modèles validés par l'équipe.

## Licence
Projet pédagogique — préciser la licence retenue par le groupe avant diffusion finale.
