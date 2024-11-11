# Réponses du test

## Utilisation de la solution (étape 1 à 3)_

### Setup virtual environment and install prerequisites

- Se placer sur la racine (project root - \technical-test-data-engineer) 
- Exécuter les commandes suivantes sur BASH dans le terminal:
1) (OPTIONAL) pip install virtualenv
2) python<version> -m venv venv
3) source venv/bin/activate
4) pip install -r requirements.txt

### 
- Une fois les python packages installés, rouler les commandes suivantes pour populer le json:
1) Se placer sur main.py
2) rouler avec les paramètres suivants pour la génération:
 
Pour la saisie quotidienne, utiliser cron dans linux avec les commandes suivantes:
 - crontab -e
 - 0 0 * * * /usr/bin/python3 (...)/technical-test-data-engineer/src/retrieve_daily_data.py

Pour la saisie instantannée, exécuter le programme retrieve_daily_data.py directement.

### Run unit tests
- Pour exécuter les test unitaires, rouler les commandes suivantes:
- 1) Se placer sur la racine

## Questions (étapes 4 à 7)

### Étape 4

Voici le lien vers le schéma de la base de données:
https://dbdiagram.io/d/MooVitamix-database-673164f5e9daa85acaf7a46e

Je recommande une base de données relationnelle PosgreSQL pour les raisons suivantes:
- Par exemple, supprimer un utilisateur permettrait de détruire l'historique associé et sa liste de genres musciaux préférés avec on delete CASCADE.
- Elle s'intègre bien avec SQL, ce qui facilite les opérations CRUD.
- Chaque table peut être modifiée sans avoir à gérer l'intégrité de la base de données.
- PosgreSQL est open source et est une option sécuritaire.

### Étape 5

- logging quotidien: détail de chaque connexion (avec le package logging)
- Afficher spédicifiquement les requêtes non-réussies 
- Métriques: temps d'exécution des requêtes, taux de succès, 
nombre d'entrées quotidienne pour chaque différente catégorie: Users, Tracks, History
- Alerte lorsque le nombre de connexions maximales a été atteint pour un usager 

### Étape 6
J'assume que l'équipe choisirait un top-k recommandation avec 10-15 chansons prédites selon l'historique écouté
- Pour automatiser le calcul, j'utiliserais un pickle des poids du modèle ML entrainé par les scientifiques de données.
- Lorsque l'utilisateur entre dans l'application, le programme predict_songs.py serait déclenchée, comportant une lecture SQL de l'historique de l'usager dans la base de données PosgreSQL.
Avec celui-ci, j'afficherais dans l'écran d'accueil la liste quotidienne des chansons recommandées.
- Lorsque l'utilisateur clique sélectionne une chanson, le programme predict_songs.py serait encore enclenché. 
Cette fois, l'utilisateur recevrait une suggestion de prochaines chansons à écouter en fonction de son écoute actuelle.
Les pickles quotidiens et la base de données seraient entreposés dans un S3 bucket AWS, lues par read_remote.py. 
- Leur mise à jour serait faite avec le cron quotidien et appelé par une fonction update_remote.py 

### Étape 7

- Lors de l'exécution de la saisie quotidienne du flux de données, je capturerais les statistiques utilisées pour l'entrainement du modèle.
- Ces dernières pourraient possiblement être le temps d'écoute des utilisateurs, le nombre de clics sur les recommandations, la similitude entre les chansons écoutées et recommandées selon le modèle
- Après la saisie quotidienne des données, je roulerais les programmes suivants avec cron:
1) calculate_statistics.py (pour calculer les statistiques, rentrer les données dans un json pour créer un payload flexible)
2) update_weights.py. J'entrainerais idéalement seulement la couche supérieure du softmax si l'on utilise du deep learning. 
Sinon, j'utiliserais cleanML pour faire la sélection des hyperparamètres de réentrainement, en fonction de la performance des derniers jours. 
3) select_model.py. Une fois les modèles assez stables, je ferais également la sélection de modèles sur les modèles ayant le plus performé.

