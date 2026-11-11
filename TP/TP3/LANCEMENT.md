# Lancer le TP3 sous Windows PowerShell

L'environnement `.venv`, les données et le modèle ont été préparés localement.
Les commandes utilisent directement Python de cet environnement : aucune activation n'est nécessaire.

## Terminal 1 : API

```powershell
cd C:\Users\Salah\Desktop\TP3\maintai-starter-tp3
.\.venv\Scripts\python.exe -m uvicorn maintai.api.main:app --reload --env-file .env
```

Documentation API : http://localhost:8000/docs.

## Terminal 2 : interface

```powershell
cd C:\Users\Salah\Desktop\TP3\maintai-starter-tp3
.\.venv\Scripts\python.exe -m streamlit run ui/app.py
```

Ouvrir http://localhost:8501. Si Streamlit demande un e-mail, appuyer sur Entrée.
Dans la barre latérale, conserver `http://localhost:8000` et saisir la clé de `.env`
(valeur initiale copiée de l'exemple : `changez-moi`). Pour personnaliser cette clé,
modifier `.env`, redémarrer l'API et utiliser la nouvelle valeur dans Streamlit.
Dans « Prédiction », cliquer sur « Prédire » : les valeurs par défaut donnent 95 % et ALERTE.
Une mauvaise clé affiche une erreur 401 ; arrêter l'API puis prédire affiche « API injoignable ».
Ctrl+C arrête chaque serveur dans son terminal.

## Recréer l'environnement et les artefacts si nécessaire

```powershell
cd C:\Users\Salah\Desktop\TP3\maintai-starter-tp3
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
.\.venv\Scripts\python.exe -m maintai.dataset
.\.venv\Scripts\python.exe -m maintai.train
.\.venv\Scripts\python.exe -m pytest -q
```

Les 23 tests fournis sont conservés, avec trois vérifications supplémentaires des messages de l'interface.
Le PDF contient aussi un TP4 sur la création d'un package ; ce dossier correspond au TP3.
