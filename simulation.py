"""
Scientific simulation engine for exoplanetary atmospheres and surfaces (TRAPPIST-1 e model).
Integrates NASA Exoplanet Archive data retrieval, vectorized Perlin-like fractal topography,
synchronous tidal locking atmospheric circulation, and scientific visualization.
"""

import os
import re
import logging
import json
from typing import Dict, Tuple, Optional
import requests
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for headless/serverless execution
import matplotlib.pyplot as plt

from noise_generator import generate_numpy_perlin

LOGGER = logging.getLogger(__name__)
NASA_API_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"

FALLBACK_PLANETS = {
    "TRAPPIST-1 e": {
        "pl_name": "TRAPPIST-1 e",
        "sy_dist": 12.43,
        "st_teff": 2566.0,
        "pl_rade": 0.92,
        "pl_masse": 0.69,
        "pl_orbper": 6.10,
        "description": "Rocky exoplanet in the habitable zone with synchronous rotation."
    },
    "Proxima Centauri b": {
        "pl_name": "Proxima Centauri b",
        "sy_dist": 1.30,
        "st_teff": 3050.0,
        "pl_rade": 1.08,
        "pl_masse": 1.27,
        "pl_orbper": 11.18,
        "description": "Closest known exoplanet orbiting a red dwarf star."
    }
}

def sanitize_planet_name(planet_name: str) -> str:
    """Sanitizes planet name to prevent injection or invalid queries."""
    if not isinstance(planet_name, str):
        return "TRAPPIST-1 e"
    cleaned = re.sub(r"[^a-zA-Z0-9\s\-\.]", "", planet_name).strip()
    return cleaned if cleaned else "TRAPPIST-1 e"

def fetch_planet_data(planet_name: str) -> Dict:
    """
    Retrieves planetary parameters from the NASA Exoplanet Archive TAP service.
    Falls back to curated astrophysical data if network fails or planet is missing.
    """
    safe_name = sanitize_planet_name(planet_name)
    LOGGER.info(f"Fetching astrophysical data for {safe_name} from NASA Exoplanet Archive...")

    try:
        query = (f"SELECT pl_name, sy_dist, st_teff, pl_rade, pl_masse, pl_orbper "
                 f"FROM pscomppars WHERE pl_name = '{safe_name}'")
        response = requests.get(
            NASA_API_URL,
            params={"query": query, "format": "json"},
            timeout=8
        )
        response.raise_for_status()
        data = response.json()
        if data and isinstance(data, list) and len(data) > 0:
            record = data[0]
            # Ensure mandatory fields are present and not None
            if record.get('pl_rade') is not None:
                LOGGER.info(f"Successfully retrieved data from NASA API for {safe_name}")
                return record
    except Exception as e:
        LOGGER.warning(f"NASA API request failed ({e}). Using curated fallback astrophysical dataset.")

    # Fallback lookup
    if safe_name in FALLBACK_PLANETS:
        return FALLBACK_PLANETS[safe_name]
    
    # Default fallback
    return FALLBACK_PLANETS["TRAPPIST-1 e"]

def generate_topography(width: int = 1024, height: int = 512, scale: float = 120.0, octaves: int = 6) -> np.ndarray:
    """Generates 2D planetary topography using vectorized fractal noise."""
    LOGGER.info(f"Generating planetary topography ({width}x{height})...")
    topo = generate_numpy_perlin(height=height, width=width, scale=scale, octaves=octaves)
    return topo

def simulate_atmosphere(topo: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Simulates synchronous tidal-locking atmospheric circulation.
    Computes zonal and meridional wind vectors influenced by surface elevation gradients.
    """
    LOGGER.info("Simulating synchronous tidal-locking atmospheric circulation...")
    height, width = topo.shape

    # Correct gradient computation: along axis 0 (y/vertical -> meridional v), axis 1 (x/horizontal -> zonal u)
    grad_y, grad_x = np.gradient(topo)

    # Base synchronous wind: East-to-West thermal flow from day-side to night-side
    u_base = np.full((height, width), -2.0)
    v_base = np.zeros((height, width))

    # Incorporate topographical deflection
    wind_u = u_base - (grad_x * 4.0)
    wind_v = v_base - (grad_y * 4.0)

    return wind_u, wind_v

def render_simulation(topo: np.ndarray, u: np.ndarray, v: np.ndarray, planet_data: Dict, output_path: str) -> str:
    """
    Renders high-resolution scientific visualization combining topography heatmap and wind vector quivers.
    Saves figure securely and closes handles to prevent memory leaks.
    """
    LOGGER.info(f"Rendering scientific visualization to {output_path}...")
    fig, ax = plt.subplots(figsize=(14, 7), dpi=200)

    # Plot topography terrain heatmap
    im = ax.imshow(topo, cmap="terrain", origin="upper", extent=[0, 360, -90, 90])
    
    # Plot wind velocity vectors (quiver) with subsampling for clarity
    height, width = topo.shape
    step = max(1, width // 36)
    y_idxs, x_idxs = np.mgrid[0:height:step, 0:width:step]
    
    # Map grid indices to planetary coordinates (Longitude 0-360, Latitude -90 to 90)
    lon = np.linspace(0, 360, width)
    lat = np.linspace(-90, 90, height)
    xx, yy = np.meshgrid(lon[::step], lat[::step])
    
    sub_u = u[::step, ::step]
    sub_v = v[::step, ::step]

    ax.quiver(xx, yy, sub_u, sub_v, color="white", alpha=0.6, scale=60, width=0.003, headwidth=4)

    planet_name = planet_data.get('pl_name', 'Exoplanet')
    radius = planet_data.get('pl_rade', 'N/A')
    orbit = planet_data.get('pl_orbper', 'N/A')
    teff = planet_data.get('st_teff', 'N/A')

    ax.set_title(
        f"Exoplanetary Atmospheric & Surface Simulation: {planet_name}\n"
        f"Radius: {radius} R⊕ | Orbital Period: {orbit} days | Stellar Temp: {teff} K (Tidal Locking Model)",
        fontsize=12, fontweight='bold', pad=15, color='white'
    )
    ax.set_xlabel("Planet Longitude (Degrees)", fontsize=10, color='white')
    ax.set_ylabel("Planet Latitude (Degrees)", fontsize=10, color='white')
    
    # Styling dark theme for professional scientific aesthetic
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#0f172a')
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')

    cbar = fig.colorbar(im, ax=ax, orientation='horizontal', pad=0.1, shrink=0.8)
    cbar.set_label('Relative Surface Elevation (Normalized)', color='white')
    cbar.ax.tick_params(colors='white')

    os.path.dirname(output_path) and os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close(fig)  # Prevent memory leaks
    LOGGER.info(f"Render successfully saved to {output_path}")
    return output_path
