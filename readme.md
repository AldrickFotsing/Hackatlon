Markdown
# 📍 CareMap Cameroon 🏥
**Intelligence Géospatiale pour un Accès Rapide aux Soins de Santé.**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://hackatlon.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Location](https://img.shields.io/badge/Region-Yaoundé%2C%20Cameroon-red)](https://www.google.com/maps)

## 🌟 Vision du Projet
Dans les situations d'urgence ou de besoin de soins spécifiques, chaque seconde compte. **CareMap** est une solution interactive développée lors du **Hackathon Yango/Zindi (Avril 2026)** à Yaoundé. Elle permet de localiser instantanément les structures de santé (hôpitaux, pharmacies, centres spécialisés) les plus proches de l'utilisateur, en combinant la puissance du **Machine Learning** et de la **Visualisation Géospatiale**.

## 🚀 Fonctionnalités Clés
* **Recherche par Catégorie :** Filtrez parmi plus de 4 000 structures (Hôpitaux, Pharmacies, Centres de Santé, etc.).
* **Moteur KNN Ultra-Rapide :** Utilisation d'un algorithme `BallTree` avec la distance `Haversine` pour des recommandations en moins de **0,6 ms**.
* **Carte Interactive :** Visualisation dynamique via **Folium** avec regroupement de points (MarkerCluster).
* **Guidage GPS :** Génération automatique d'itinéraires vers Google Maps pour un guidage en temps réel.
* **Interface Responsive :** Déployé avec **Streamlit** pour une utilisation fluide sur PC et Smartphone.

## 🛠️ Stack Technique
* **Langage :** Python 3.x
* **Analyse de Données :** Pandas, NumPy
* **Machine Learning :** Scikit-learn (`BallTree` pour la recherche spatiale)
* **Cartographie :** Folium, Streamlit-Folium
* **Interface Web :** Streamlit

## 🏗️ Architecture du Projet
```text
├── app.py                # Application principale Streamlit
├── df_final_clean.csv    # Dataset nettoyé des structures de santé
├── requirements.txt      # Dépendances du projet
└── README.md             # Documentation
📊 Performance du Modèle
Le moteur de recommandation utilise une structure de données en arbre pour optimiser la recherche de proximité sur une sphère :

Algorithme : BallTree (métrique Haversine)

Temps de réponse : ~0.00057 secondes

Rayon de la Terre utilisé : 6371 km


Installer les dépendances :

Bash
pip install -r requirements.txt
Lancer l'application :

Bash
streamlit run app.py

Lien pour tester l'app: https://hackatlon.streamlit.app/

Projet réalisé dans le cadre du Hackathon  - Yaoundé 2026.
