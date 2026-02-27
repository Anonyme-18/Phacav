🌍 TRAPPIST-1 e – Simulation Planétaire Simplifiée

Simulation scientifique et visuelle de la surface et de la circulation atmosphérique de la planète TRAPPIST-1 e à partir des données publiques de la NASA Exoplanet Archive.

Ce projet combine :

🔭 Données astrophysiques réelles

🏔 Génération procédurale de topographie (Perlin Noise)

🌬 Simulation atmosphérique simplifiée (modèle synchrone jour-nuit)

📊 Visualisation scientifique avec Matplotlib & Seaborn

📌 Objectif

Créer une représentation scientifique stylisée de TRAPPIST-1 e incluant :

📡 Récupération des données physiques depuis l’archive NASA

🗺 Génération d’une surface rocheuse procédurale

🌪 Simulation de vents globaux (planète en rotation synchrone)

🖼 Rendu final combinant relief + circulation atmosphérique

🧠 Contexte Scientifique

TRAPPIST-1 e est une exoplanète rocheuse située dans la zone habitable du système TRAPPIST-1.
Elle est probablement en rotation synchrone, ce qui signifie :

Une face toujours éclairée (jour permanent)

Une face toujours sombre (nuit permanente)

Une circulation atmosphérique influencée par ce contraste thermique extrême

Ce script modélise une version simplifiée de ce phénomène.

🛠 Technologies Utilisées

Python 3

requests → requêtes API NASA

numpy → calcul scientifique

noise → génération Perlin Noise

matplotlib → visualisation

seaborn → rendu thermique

logging → suivi des étapes

📂 Structure du Projet
.
├── main.py

⚙️ Installation
1️⃣ Cloner le projet
git clone <repo_url>
cd <repo>
2️⃣ Installer les dépendances
pip install requests numpy matplotlib seaborn noise
🚀 Exécution
python main.py
🔬 Fonctionnement Détaillé
1️⃣ Récupération des données NASA
fetch_planet_data(planet_name)

Interroge l’API Exoplanet Archive

Récupère :

Rayon planétaire

Température de l’étoile

Période orbitale

Masse

Distance au système

2️⃣ Génération de la Topographie
generate_topography()

Génération via Perlin Noise 2D

8 octaves

Normalisation entre 0 et 1

Export : step2_topo.png

3️⃣ Simulation Atmosphérique
simulate_atmosphere(topo)

Modèle simplifié :

Vent zonal constant Est → Ouest

Influence du relief via gradient

Affichage vectoriel avec quiver

Export : step3_winds.png

4️⃣ Rendu Final
final_render(topo, u, v, data)

Heatmap terrain

Superposition vecteurs atmosphériques

Informations planétaires intégrées

Export HD : final_planet_e.png

🖼 Résultats Générés
Fichier	Description
step2_topo.png	Carte d'altitude relative
step3_winds.png	Vecteurs atmosphériques
final_planet_e.png	Rendu scientifique final
📊 Paramètres Modifiables

Dans le script :

WIDTH, HEIGHT = 1024, 512
TARGET_PLANET = "TRAPPIST-1 e"

Tu peux :

Augmenter la résolution

Changer la planète (si présente dans l’archive NASA)

Ajuster la force des vents

Modifier la palette de couleurs

⚠️ Limitations

Modèle atmosphérique simplifié

Pas de dynamique thermique réelle

Pas de modélisation 3D sphérique

Hypothèse de vent constant

Ce projet est une visualisation scientifique pédagogique, pas un modèle climatologique complet.

💡 Améliorations Possibles

Intégrer une carte thermique jour/nuit

Modéliser l’évaporation/condensation

Ajouter un rendu sphérique 3D

Simuler différentes compositions atmosphériques

Export animation vidéo

📜 Licence

Projet éducatif et expérimental.

👨‍🚀 Auteur
AMOUZOU-ABLO Cédric Jean-Marc & PEREIRA DASILVA Péniel

Simulation développée pour exploration scientifique et démonstration de modélisation procédurale appliquée à l’astrophysique.
