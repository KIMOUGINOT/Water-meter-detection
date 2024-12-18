# Suez Challenge

## File structure

```raw
suez_challenge/
│
├── data/                     # Données brutes, intermédiaires et finales
│   ├── raw/                  # Données brutes (images téléchargées)
│   ├── detected/             # Images avec compteurs détectés et labels
│   ├── cropped/              # Images croppées
│   ├── models/               # Modèles entraînés et leurs métadonnées
│   └── output/               # Résultats finaux de la pipeline (par exemple, nombres détectés)
│
├── src/                      # Code source principal
│   ├── training/             # Scripts et modules pour la partie entraînement
│   │   ├── prepare_data.py   # Prétraitement des données pour l'entraînement
│   │   ├── train_model.py    # Script pour entraîner un modèle
│   │   └── evaluate_model.py # Évaluation des modèles
│   ├── detection/            # Modules pour la détection des compteurs
│   ├── cropping/             # Modules pour le recadrage des images
│   ├── number_detection/     # Modules pour détecter les nombres
│   └── pipeline.py           # Orchestration de la pipeline pour la production
│
├── configs/                  # Fichiers de configuration
│   ├── train_config.yaml     # Configuration pour l'entraînement
│   └── pipeline_config.yaml  # Configuration pour la production
│
├── tests/                    # Tests unitaires et d'intégration
│
├── venv/                     # Environnement virtuel Python (non versionné)
│
├── main.py                   # Point d'entrée principal pour orchestrer la pipeline
├── requirements.txt          # Dépendances Python
├── requirements-dev.txt      # Dépendances supplémentaires pour le développement
└── README.md                 # Documentation principale du projet
```
