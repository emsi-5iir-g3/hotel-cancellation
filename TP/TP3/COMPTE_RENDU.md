# Compte rendu · TP3 : une interface Streamlit pour MaintAI

Groupe et membres : à renseigner. Date : 11 novembre 2026.

## 1. Mise en place

Environnement .venv créé, dépendances installées, données générées et modèle entraîné.
Résultat réel initial : `5 failed, 18 passed, 1 warning in 20.21s`.
Les trois tests de test_client.py échouaient avec NotImplementedError (predict vide).
Les deux tests de test_ui.py échouaient avec IndexError (indicateurs absents).

## 2. Lancer Streamlit

L'erreur décrite par le PDF pour `streamlit run ui/app.py` est :
`ModuleNotFoundError: No module named 'maintai'`.
Elle n'a pas été observée manuellement dans un navigateur pendant cette réalisation.
`python -m streamlit run ui/app.py`, depuis la racine, ajoute le répertoire courant à la recherche des modules. Les commandes de LANCEMENT.md sélectionnent explicitement Python de .venv. Le résultat de la première commande dépend aussi du PATH et des installations existantes.

## 3. Sprint 1 : Données

Code réalisé :

```python
    c1, c2, c3 = st.columns(3)
    c1.metric("Relevés", len(df))
    c2.metric("Taux de panne", f"{df.failure.mean():.1%}")
    c3.metric("Température moyenne", f"{df.temperature_c.mean():.1f} °C")

    variable = st.selectbox("Variable", FEATURES)
    tranches = pd.cut(df[variable], bins=10)
    taux = df.groupby(tranches, observed=True).failure.mean()
    taux.index = [round(intervalle.mid, 2) for intervalle in taux.index]
    taux.index.name = variable
    st.subheader("Taux de panne par tranche")
    st.bar_chart(taux.rename("Taux de panne (%)") * 100)

    st.subheader("Température et vibration selon la panne")
    nuage = df.assign(panne=df.failure.map({0: "Non", 1: "Oui"}))
    st.scatter_chart(nuage, x="temperature_c", y="vibration_mm_s", color="panne")
```

| Indicateur | Valeur sur les données générées |
|---|---|
| Relevés | 5000 |
| Taux de panne | 13,6 % |
| Température moyenne | 59,8 °C |

Pour vibration_mm_s, le taux de panne augmente : environ 2,0 % dans la première tranche, 32,3 % dans la troisième et 83,6 % dans la cinquième. Les tranches extrêmes ont moins d'observations. La vibration a un effet fort ; comparer formellement les variables demanderait une analyse standardisée, leurs unités étant différentes.

Un print("relance") en début de script s'affiche à chaque réexécution. Changer la liste Variable relance le script. Les curseurs étant dans st.form, les déplacer attend le bouton Prédire avant soumission. Ceci explique le comportement, sans prétendre à une observation manuelle du terminal.

@st.cache_data mémorise le résultat pour les mêmes arguments et évite de relire le CSV à chaque interaction. Un changement du contenu avec le même chemin peut nécessiter de vider le cache.

## 4. Sprint 2 : Prédiction

Méthode réalisée :

```python
    def predict(self, reading: dict) -> dict:
        """Envoie un relevé ; lève APIError si l'API refuse, httpx.HTTPError si elle est injoignable."""
        headers = {"X-API-Key": self.api_key} if self.api_key else {}
        response = self.http.post("/v1/predict", json=reading, headers=headers)
        if response.status_code != 200:
            try:
                detail = response.json().get("detail")
            except ValueError:
                detail = response.text
            raise APIError(response.status_code, detail)
        return response.json()

```

Tests fournis après les deux sprints : `23 passed, 1 warning in 5.17s`.
Avec trois tests supplémentaires des messages 401, connexion refusée et résultat normal : `26 passed, 1 warning in 5.15s`.
L'avertissement concerne la dépréciation du TestClient Starlette utilisant httpx ; aucun test n'échoue.

| Essai | Affichage |
|---|---|
| Valeurs par défaut, bonne clé | Probabilité 95 % et ALERTE |
| Fausse clé | Avertissement Erreur 401 et détail de l'API |
| API arrêtée | API injoignable et détail de connexion |

La probabilité réelle calculée sur le modèle local est 0,9475 pour 72 °C, 6 mm/s, 85 % et 15000 h. Le client est vérifié via TestClient ; les messages via AppTest avec réponses ou erreurs contrôlées. Les essais manuels avec deux serveurs sont reproductibles avec LANCEMENT.md, et restent à effectuer dans le navigateur.

CORS est une restriction appliquée par le navigateur. Ici, le serveur Python Streamlit appelle l'API via httpx. Le navigateur ne contacte pas directement le port 8000 ; autoriser le port 8501 n'est donc pas nécessaire pour ce trajet.

## 5. Questions de compréhension

1. En TP2, JavaScript dans le navigateur envoie la requête. En TP3, le serveur Python Streamlit l'envoie.
2. TestClient appelle directement l'application ASGI dans le processus de test, sans uvicorn ni connexion réseau. L'injection http=client permet de conserver le même code client.
3. Streamlit convient à une démonstration rapide avec formulaire et graphiques en Python. HTML/JavaScript offre plus de contrôle pour une application quotidienne de techniciens nécessitant une interface mobile précise et des parcours personnalisés, avec un coût de développement supérieur. Streamlit peut aussi convenir à un outil interne simple.

## 6. Rendu Git

Le dossier fourni n'est pas un dépôt Git. Message réel : `fatal: not a git repository (or any of the parent directories): .git`.

- Pull request : non créée, dépôt distant non fourni.
- Tag tp3 : non créé.
- git status avant commit : non applicable. Le .gitignore exclut .env, .venv/, data/*.csv et models/.

Le rendu Git reste à réaliser dans le dépôt du groupe après relecture. Aucun commit ou lien de PR n'est inventé.

## 7. Ce qui reste à renseigner

Identités du groupe, essais manuels dans le navigateur et rendu Git. Les deux sprints sont implémentés et vérifiés automatiquement. Le PDF comprend aussi le TP4, distinct de ce starter TP3.
