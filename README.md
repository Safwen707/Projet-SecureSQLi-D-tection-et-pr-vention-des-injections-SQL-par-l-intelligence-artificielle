# SecureSQLi

SecureSQLi est une application web de simulation d'injections SQL, accompagnée d'une intelligence artificielle (XGBoost) capable de détecter automatiquement les requêtes malveillantes.

## 🎯 Objectif

Ce projet a pour but :
- de sensibiliser aux risques des injections SQL (SQLi),
- de montrer comment une IA peut être utilisée pour identifier automatiquement les requêtes dangereuses.

## 🛠️ Technologies utilisées

- **Frontend** : HTML, CSS, JavaScript (Node.js, Express)
- **Backend** : Flask (Python)
- **Base de données** : MySQL
- **Machine Learning** : XGBoost, Scikit-learn, Pandas, Joblib, Matplotlib

---

## 📁 Structure du projet

| Fichier/Dossier            | Description |
|----------------------------|-------------|
| `node_modules/`            | Contient les dépendances Node.js. |
| `views/`                   | Contient les fichiers HTML pour l’interface utilisateur (pages vulnérables à SQLi). |
| `api.js`                   | Script Node.js gérant les routes API de l'application web. |
| `app.py`                   | Script principal Flask pour lancer le backend Python. |
| `demo.mp4`                 | Vidéo démonstrative du projet SecureSQLi. |
| `index.js`                 | Point d’entrée de l’application web côté serveur avec Express.js. |
| `package.json`             | Fichier de configuration listant les dépendances Node.js du projet. |
| `package-lock.json`        | Fichier de verrouillage des versions de dépendances Node.js. |
| `sqlInjection.txt`         | Fichier texte contenant des exemples de requêtes SQLi annotées (légitimes/malveillantes). |
| `tfidf_vectorizer.pkl`     | Modèle TF-IDF enregistré pour transformer les requêtes SQL en vecteurs. |
| `xgboost_best_model.pkl`   | Modèle entraîné XGBoost optimisé pour la détection des SQLi. |
| `XGBoostmodele.py`         | Script Python de classification : entraînement, sauvegarde et prédiction avec XGBoost. |

---

## 📊 Fonctionnalités principales

- **Interface vulnérable** : permet de simuler des attaques SQL dans un environnement contrôlé.
- **Détection automatique** : l'IA analyse les requêtes entrées pour les classifier.
- **Visualisation des performances** : affichage de la précision, F1-score, matrice de confusion.

---
