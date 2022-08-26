# Résultats des Notebooks sous format HTML

Les résultats des notebooks en pages HTML :

<a href = https://deviluna29.github.io/oc_ingenieur-ia_p9/P09_00_notebook_analyse>Analyse du jeu de données</a>

<a href = https://deviluna29.github.io/oc_ingenieur-ia_p9/P09_01_notebook_modelisation>Modélisation et entraînement des différents modèles</a>

## Installation de l'environnement virtuel

Créer l'environnement à partir du fichier yaml
```bash
conda env create -f environment.yml
```

Activer l'environnement
```bash
conda activate projet_9
```

## Téléchargement du jeu de données

Récupérer le jeu de données <a href = https://www.kaggle.com/datasets/gspmoreira/news-portal-user-interactions-by-globocom/>à cette adresse</a>

Dezipper le fichiers dans le dossier : 

- "data/articles/"

Le dossier "articles" doit contenir ce qui suit :

- un dossier "/clicks"
- articles_embeddings.pickle
- articles_metadata.csv
- clicks_sample.csv

## Application Web

Url de l'application flask, hébergée sur Azure App : <a href = https://ocp9-recommandation.azurewebsites.net/>https://ocp9-recommandation.azurewebsites.net/</a>

(Après 20min d'inactivité, Azure App stop l'application. En cas de nouvelle requête il faut donc attendre quelques minutes pour que l'application redémarre)