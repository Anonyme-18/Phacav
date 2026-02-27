import os
import logging
import json
import re
from typing import Dict, Tuple

import requests
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from noise import pnoise2

# --- CONFIGURATION ---
WIDTH, HEIGHT = 1024, 512
DATA_DIR = "trappist_e_results"
NASA_API_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
TARGET_PLANET = "TRAPPIST-1 e"

os.makedirs(DATA_DIR, exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(message)s")
LOGGER = logging.getLogger(__name__)

# --- ÉTAPE 1 : RÉCUPÉRATION DES DONNÉES NASA ---
def fetch_planet_data(planet_name: str) -> Dict:
    LOGGER.info(f"Étape 1 : Récupération des données pour {planet_name}...")
    safe_name = re.sub(r"[^a-zA-Z0-9\s\-\.]", "", planet_name).strip()
    query = (f"SELECT pl_name, sy_dist, st_teff, pl_rade, pl_masse, pl_orbper "
             f"FROM pscomppars WHERE pl_name = '{safe_name}'")

    response = requests.get(NASA_API_URL, params={"query": query, "format": "json"}, timeout=10)
    response.raise_for_status()
    data = response.json()
    if not data: raise ValueError("Données introuvables.")

    LOGGER.info(f"Données reçues : Rayon={data[0]['pl_rade']} R_Earth, Temp_Étoile={data[0]['st_teff']}K")
    return data[0]

# --- ÉTAPE 2 : GÉNÉRATION DE LA TOPOGRAPHIE ---
def generate_topography() -> np.ndarray:
    LOGGER.info("Étape 2 : Génération de la surface rocheuse...")
    scale = 120.0
    octaves = 8

    topo = np.zeros((HEIGHT, WIDTH))
    for y in range(HEIGHT):
        for x in range(WIDTH):
            topo[y][x] = pnoise2(y/scale, x/scale, octaves=octaves, persistence=0.5, lacunarity=2.0)

    # Normalisation 0-1
    topo = (topo - topo.min()) / (topo.max() - topo.min())

    plt.figure(figsize=(12, 6))
    plt.imshow(topo, cmap='magma')
    plt.title(f"Topographie brute de {TARGET_PLANET}")
    plt.colorbar(label="Altitude relative")
    plt.savefig(os.path.join(DATA_DIR, "step2_topo.png"))
    plt.show()
    return topo

# --- ÉTAPE 3 : SIMULATION DES VENTS (MODÈLE SYNCHRONE) ---
def simulate_atmosphere(topo: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    LOGGER.info("Étape 3 : Simulation de la circulation atmosphérique (Flux Jour-Nuit)...")

    # Gradient de la topo pour l'influence du relief
    grad_y, grad_x = np.gradient(topo)

    # Modèle synchrone : Vent dominant du point chaud (centre) vers le point froid (bords)
    # Pour simplifier : un flux zonal (Est vers Ouest) constant
    u_base = np.full((HEIGHT, WIDTH), -2.0)
    v_base = np.zeros((HEIGHT, WIDTH))

    # Influence du relief
    wind_u = u_base + (grad_y * 5.0)
    wind_v = v_base - (grad_x * 5.0)

    plt.figure(figsize=(12, 6))
    step = 30
    y, x = np.mgrid[0:HEIGHT:step, 0:WIDTH:step]
    plt.quiver(x, y, wind_u[::step, ::step], -wind_v[::step, ::step], color='blue')
    plt.title("Vecteurs de circulation atmosphérique")
    plt.savefig(os.path.join(DATA_DIR, "step3_winds.png"))
    plt.show()
    return wind_u, wind_v

# --- ÉTAPE 4 : RENDU FINAL ---
def final_render(topo: np.ndarray, u: np.ndarray, v: np.ndarray, data: Dict):
    LOGGER.info("Étape 4 : Rendu final combiné...")
    plt.figure(figsize=(16, 8))

    # Fond : Terrain
    sns.heatmap(topo, cmap="terrain", cbar=False, xticklabels=False, yticklabels=False)

    # Overlay : Vents
    step = 25
    y, x = np.mgrid[0:HEIGHT:step, 0:WIDTH:step]
    plt.quiver(x, y, u[::step, ::step], -v[::step, ::step],
               color="white", alpha=0.5, scale=50)

    info_text = f"Rayon: {data['pl_rade']} R⊕ | Orbite: {data['pl_orbper']} jours"
    plt.title(f"{TARGET_PLANET}\n{info_text}", fontsize=14)
    plt.savefig(os.path.join(DATA_DIR, "final_planet_e.png"), dpi=300)
    plt.show()

# --- MAIN ---
def main():
    try:
        # 1. Data
        planet_info = fetch_planet_data(TARGET_PLANET)

        # 2. Surface
        topo_map = generate_topography()

        # 3. Atmosphere
        u, v = simulate_atmosphere(topo_map)

        # 4. Visualization
        final_render(topo_map, u, v, planet_info)

        LOGGER.info(f"Simulation terminée. Résultats sauvegardés dans {DATA_DIR}")

    except Exception as e:
        LOGGER.error(f"Erreur : {e}")

if __name__ == "__main__":
    main()