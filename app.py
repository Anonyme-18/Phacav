"""
Flask Web Application for Exoplanetary Atmospheric & Surface Simulation.
Designed for seamless deployment on Vercel and local execution.
"""

import os
import time
from flask import Flask, render_template, request, jsonify, send_from_directory
from simulation import fetch_planet_data, generate_topography, simulate_atmosphere, render_simulation

app = Flask(__name__, static_folder='static', template_folder='templates')

RESULTS_DIR = os.path.join(app.static_folder, 'results')
os.makedirs(RESULTS_DIR, exist_ok=True)

@app.route('/')
def index():
    """Renders the main scientific control dashboard."""
    return render_template('index.html')

@app.route('/api/simulate', methods=['POST', 'GET'])
def simulate():
    """API endpoint to run simulation for a given planet and return results."""
    try:
        planet_name = request.args.get('planet', 'TRAPPIST-1 e')
        if request.is_json and request.json:
            planet_name = request.json.get('planet', planet_name)

        # 1. Fetch NASA data
        planet_data = fetch_planet_data(planet_name)

        # 2. Generate Topography
        topo = generate_topography(width=1024, height=512)

        # 3. Simulate Atmosphere
        u, v = simulate_atmosphere(topo)

        # 4. Render visualization
        timestamp = int(time.time())
        filename = f"simulation_{timestamp}.png"
        output_path = os.path.join(RESULTS_DIR, filename)
        render_simulation(topo, u, v, planet_data, output_path)

        image_url = f"/static/results/{filename}"

        return jsonify({
            "status": "success",
            "planet_data": planet_data,
            "image_url": image_url,
            "message": f"Simulation successfully generated for {planet_data.get('pl_name', planet_name)}"
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "phacav-exoplanet-simulation"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
