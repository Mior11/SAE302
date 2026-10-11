# Déploiement pédagogique sur VirtualBox

## Topologie proposée
- **VM 1 — application/serveur** : Linux, Python 3.10+, serveur TCP sur le port 5050.
- **VM 2 — base de données** : Linux, MariaDB, accessible uniquement depuis le réseau privé des VM.
- **Client graphique** : poste hôte ou VM avec environnement graphique et PySide6.

Configurez les deux VM sur un réseau privé hôte ou un réseau interne VirtualBox. Attribuez des adresses IP stables et vérifiez la connectivité avec `ping`. Ne publiez pas MariaDB sur Internet.

## Serveur
```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
mkdir -p ~/sae302 && cd ~/sae302
# Copier/cloner le dépôt, puis :
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python -m server.main --host 0.0.0.0 --port 5050
```

Autorisez le port TCP 5050 uniquement sur le réseau privé des VM dans le pare-feu. Le serveur actuel ne se connecte pas à MariaDB.

## MariaDB (VM 2)
```bash
sudo apt update
sudo apt install -y mariadb-server
sudo mariadb < database/schema.sql
```
Créez ensuite un utilisateur dédié avec des droits limités et autorisez l'accès réseau uniquement depuis la VM applicative. Ne placez jamais le mot de passe dans Git : utilisez des variables d'environnement ou un fichier de configuration non versionné.

## Limites
Ces instructions décrivent le déploiement de composants de démonstration, pas une architecture sûre pour la gestion réelle de la circulation. Mesurez et documentez les résultats effectivement observés dans le compte rendu.
