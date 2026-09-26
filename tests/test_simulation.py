import pytest
import numpy as np
from simulation import sanitize_planet_name, fetch_planet_data, generate_topography, simulate_atmosphere

def test_sanitize_planet_name():
    assert sanitize_planet_name("TRAPPIST-1 e") == "TRAPPIST-1 e"
    assert sanitize_planet_name("  Proxima Centauri b  ") == "Proxima Centauri b"
    assert sanitize_planet_name("Planet; DROP TABLE;") == "Planet DROP TABLE"
    assert sanitize_planet_name(None) == "TRAPPIST-1 e"

def test_fetch_planet_data():
    data = fetch_planet_data("TRAPPIST-1 e")
    assert isinstance(data, dict)
    assert "pl_name" in data
    assert data["pl_name"] == "TRAPPIST-1 e"
    assert "pl_rade" in data

def test_generate_topography():
    topo = generate_topography(width=128, height=64)
    assert isinstance(topo, np.ndarray)
    assert topo.shape == (64, 128)
    assert topo.min() >= 0.0
    assert topo.max() <= 1.0

def test_simulate_atmosphere():
    topo = np.random.rand(64, 128)
    u, v = simulate_atmosphere(topo)
    assert isinstance(u, np.ndarray)
    assert isinstance(v, np.ndarray)
    assert u.shape == (64, 128)
    assert v.shape == (64, 128)
