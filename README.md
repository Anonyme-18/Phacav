# 🪐 PHACAV: Exoplanetary Atmospheric & Surface Simulation Engine

[![CI Pipeline](https://github.com/Anonyme-18/Phacav/actions/workflows/ci.yml/badge.svg)](https://github.com/Anonyme-18/Phacav/actions/workflows/ci.yml)
[![Vercel Deployment](https://img.shields.io/badge/Deployed%20on-Vercel-black?style=flat&logo=vercel)](https://vercel.com)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **PHACAV** is an advanced scientific simulation engine and interactive web application designed to model exoplanetary surface topography and tidal-locked atmospheric circulation using real astrophysical data from the NASA Exoplanet Archive.

---

## 🔭 Scientific Overview

Exoplanets in the habitable zone of red dwarf stars (such as **TRAPPIST-1 e** or **Proxima Centauri b**) are frequently in **synchronous rotation** (tidal locking). This extreme astrophysical phenomenon results in:
* **Permanent Day-Side:** Intense stellar radiation and thermal input.
* **Permanent Night-Side:** Eternal darkness and extreme cold.
* **Global Wind Patterns:** Complex atmospheric thermal circulation driven by day-night pressure gradients and deflected by planetary topography.

PHACAV models these systems by combining:
1. **Real-Time NASA Data Retrieval:** Querying the NASA Exoplanet Archive TAP API (`pscomppars`) for physical parameters (radius, mass, orbital period, stellar temperature).
2. **Procedural Fractal Topography:** Fast vectorized NumPy-based fractal noise (fractional Brownian motion) to generate realistic rocky surfaces.
3. **Synchronous Atmospheric Dynamics:** Navier-Stokes simplified thermal flux modeling with elevation gradient coupling.
4. **Interactive Scientific Web Dashboard:** A responsive dark-mode UI built with Flask and Tailwind CSS for real-time visualization and rendering.

---

## 🏗 System Architecture

```text
Phacav/
├── app.py                 # Flask web application & Vercel serverless entrypoint
├── simulation.py          # Core simulation engine (NASA API + Topography + Winds + Renderer)
├── noise_generator.py     # Pure NumPy vectorized fractal noise generator (zero C compilation)
├── requirements.txt       # Production dependencies
├── vercel.json            # Vercel serverless deployment configuration
├── templates/
│   └── index.html         # Interactive scientific dashboard (Tailwind CSS)
├── tests/
│   └── test_simulation.py # Comprehensive Pytest suite
└── .github/
    └── workflows/ci.yml   # Continuous Integration pipeline
```

---

## 🚀 Getting Started

### Prerequisites
* Python 3.11 or higher
* Pip package manager

### 1. Clone the Repository
```bash
git clone https://github.com/Anonyme-18/Phacav.git
cd Phacav
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Unit Tests
```bash
python -m pytest
```

### 4. Start the Local Web Server
```bash
python app.py
```
Open your browser at `http://localhost:5000`.

---

## 🌍 Vercel Deployment

This project is fully configured for serverless deployment on [Vercel](https://vercel.com).

1. Push your repository to GitHub.
2. Import the project into Vercel.
3. Vercel will automatically detect `vercel.json` and build the Python serverless application.

---

## 📊 Sample Visualizations

Generated high-resolution maps include:
* **Topographic Elevation Heatmaps** (normalized relative surface heights).
* **Atmospheric Wind Quiver Overlays** (zonal and meridional velocity vectors).
* **Astrophysical Summary Data Cards** (NASA confirmed parameters).

---

## 📜 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

## 👨‍💻 Authors

* **AMOUZOU-ABLO Cédric Jean-Marc**
* **PEREIRA DASILVA Péniel**

*Developed for scientific exploration, professional demonstration, and advanced exoplanetary modeling.*
