import numpy as np

def generate_numpy_perlin(height: int, width: int, scale: float = 100.0, octaves: int = 4, persistence: float = 0.5) -> np.ndarray:
    """
    Generates smooth 2D noise using NumPy without external C dependencies.
    Simulates multi-octave fractal brownian motion (fBm).
    """
    grid = np.zeros((height, width))
    frequency = 1.0
    amplitude = 1.0
    max_value = 0.0

    # Fallback/alternative using smooth sine/cosine superposition or random value grid interpolation
    y_coords, x_coords = np.mgrid[0:height, 0:width]
    
    # Vectorized harmonic noise (sum of trigonometric waves with pseudo-random phases for rich planetary topology)
    np.random.seed(42)
    for i in range(octaves):
        freq = frequency / scale
        phase_y = np.random.uniform(0, 10)
        phase_x = np.random.uniform(0, 10)
        
        # Superimpose sinusoidal waves at different frequencies and orientations
        wave = np.sin(x_coords * freq * np.pi + phase_x) * np.cos(y_coords * freq * np.pi + phase_y)
        # Add secondary directional component
        wave += np.sin((x_coords - y_coords) * freq * 0.7 * np.pi) * 0.5
        
        grid += wave * amplitude
        max_value += amplitude
        amplitude *= persistence
        frequency *= 2.0

    # Normalize to [0, 1]
    grid = (grid - grid.min()) / (grid.max() - grid.min() + 1e-8)
    return grid
