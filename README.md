# Welcome to the M1_dockerOnline wiki!

## Technologies utilisées

- Django, un framework web pour Python
- Module API Docker SDK pour Python
- Base de données SQLite
- Serveur Docker externe (Fedora 40 dans un Proxmox), localhost uniquement (à remplacer par un vrai serveur au moment de la mise en production de l'application)
- HTML/CSS avec templates Django pour l'interface utilisateur.

### Pourquoi Django ?
Django est une technologie moderne, sécurisée et complète, hautement scalable. Il possède des outils intégrés comme l'authentification et le panneau d'administration. De plus, j'ai choisi Django car je souhaitais découvrir ce framework et le projet s'y prête bien.

## Processus de développement

Plutôt agile, afin de pouvoir intégrer de nouvelles idées ou des changements d'architecture. Le développement sera local, avec une infrastructure locale (serveur pour Docker, serveur de test pour le déploiement de l'application). Pendant le développement, il y aura des commits réguliers. Une fois l'application utilisable, j'aimerais intégrer les outils CI/CD de GitHub pour la maintenance et la correction de bugs.
Tests unitaires et fonctionnels : Mise en place de tests automatisés pour s'assurer que les différentes fonctionnalités (lancement de conteneurs, gestion des utilisateurs, etc.) fonctionnent comme prévu.

## Fonctionnalités à implémenter

### Authentification & comptes

- Utilisation des outils intégrés à Django, stockage en base de données.
- Session liée à un utilisateur Linux unique (avec plus de ressources matérielles, il faudrait une VM complète liée à chaque utilisateur pour éviter les conflits de noms, de ports, etc., et passer Docker en mode Swarm pour éviter de surcharger un serveur).  Chaque utilisateur aurait alors un contrôle sur ses propres conteneurs et les administrateurs auraient une vue et un contrôle global.
- Création d'un utilisateur sur le serveur Fedora à chaque nouvel utilisateur.

### Gestion de Docker

- Lancer un conteneur avec plusieurs options (nom, nom de l'image [DockerHub], redirection de ports, commande, volumes, réseau, etc.).
- Lancer un conteneur à partir d'un Dockerfile, ou à partir d'un Docker Compose.
- Accéder au terminal du conteneur, fournir un lien web vers le conteneur (Apache ou Nginx, service web, etc.).
- Arrêter un conteneur, supprimer un conteneur, télécharger une image.

### Interface utilisateur

- Lister les conteneurs lancés ou stoppés, les volumes (uniquement ceux de l'utilisateur).
- Lancer les actions définies dans la partie gestion de Docker.
- afficher les ereurs docker en cas de problème de dockerfile/compose ou de mauvais parametres 

### Interface administrateur

- Lister les conteneurs lancés ou stoppés, les volumes (pour tous les utilisateurs).
- Lancer les actions définies dans la partie gestion de Docker.
- Lister les utilisateurs inscrits, en ajouter, en supprimer.

### Monitoring serveur

- Monitoring du serveur Docker via le déploiement d'un service Grafana sur le Proxmox.

### Manipulation des services réseaux

- Manipuler le DNS pour ajouter en temps réel les URL du type : "http://moncontainer34.ledomaine.ovh". Cela peut poser des problèmes de gestion de la propagation et du cache DNS, il faut donc trouver une autre solution.

### FrontEnd (UI/UX)
- HTML/CSS pour offrir une interface conviviale et ergonomique aux utilisateurs.
