# Projet Serveur Mémoire
Nom : Khazal
Prenom : Chadi 
Projet : Serveur mémoire en Python (Système 2)
--------
# Étape 1 : Backend mémoire
État : parfaitement réussie
Le backend gère correctement :
- GET
- POST
- les erreurs d’indices
- la vérification des valeurs byte (0-255)
Tests effectués avec plusieurs lectures et écritures.
--------
# Étape 2 : Log périodique
État : parfaitement réussie
Le serveur affiche correctement le contenu de la mémoire périodiquement avec SIGALRM et les logs sont redirigés dans un fichier.
--------
# Étape 3 : Frontend segmentation
État : parfaitement réussie
Le frontend gère :
- PUT
- DELETE
- traduction GET/POST
- table des segments
- allocation FIRST FIT
- affichage debug
Les adresses virtuelles sont correctement traduites en adresses physiques.
--------
# Étape 4 : Communication frontend/backend
État : parfaitement réussie
Le frontend et le backend communiquent correctement avec des pipes.
Les commandes traduites sont transmises au backend et les réponses sont récupérées correctement.
--------
# Étape 5 : Serveur TCP
État : parfaitement réussie
Le serveur TCP fonctionne correctement avec telnet :
- connexion client
- envoi des commandes
- réception des réponses
Les tests du sujet fonctionnent correctement.
J’ai cependant rencontré quelques problèmes de synchronisation/buffering qui ont été corrigés avec flush=True.
--------
# Étape 6 : Clients automatiques
État : partiellement réussie

Les librairies RemoteMemory et ControledMemory fonctionnent correctement.
Le client.py interagit correctement avec le serveur.

Les tests avec plusieurs clients sur des segments différents fonctionnent correctement.

Pour les segments partagés, j’ai testé le lancement de plusieurs clients sur un même segment. 
J’ai observé que le deuxième client échoue lors de la requête PUT car le segment existe déjà. 

Pour la partie 6.3:
J’ai testé le serveur avec un premier client :

python3 client.py localhost 12343 seg0 10 --num_accesses 20 --debug

Le segment est bien créé et les requêtes fonctionnent.

Ensuite, j’ai testé un deuxième client avec :

python3 client.py localhost 12343 seg0 10 --num_accesses 20 --debug --no-alloc

Mais le client se bloque après :

[debug] Sending request: 'GET seg0 2'

Donc la requête semble être envoyée correctement, mais aucune réponse n’est renvoyée au client.
--------
# Difficultés rencontrées
Les principales difficultés du projet étaient :
- la communication entre processus
- les problèmes de buffering avec les pipes
- la synchronisation entre plusieurs clients
--------
# Estimation de note
Je pense que le projet est globalement fonctionnel jusqu’à l’étape 6 avec quelques limitations mineures.
Estimation personnelle : 15-17 / 20