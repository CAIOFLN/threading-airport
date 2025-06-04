from flask import Flask, request, jsonify
from flask_cors import CORS
from airport_controller import airport, PlaneAction
import threading
import time

app = Flask(__name__)
CORS(app)  # Permitir requisições do frontend

@app.route('/api/status', methods=['GET'])
def get_status():
    """Retorna o status atual do aeroporto"""
    try:
        status = airport.get_airport_status()
        return jsonify({"success": True, "data": status})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/events', methods=['GET'])
def get_events():
    """Retorna eventos recentes"""
    try:
        limit = request.args.get('limit', 10, type=int)
        events = airport.get_recent_events(limit)
        return jsonify({"success": True, "data": events})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/plane/create', methods=['POST'])
def create_plane():
    """Cria um novo avião"""
    try:
        data = request.get_json()
        
        # Validar dados
        if not data or 'name' not in data or 'action' not in data or 'duration' not in data:
            return jsonify({"success": False, "error": "Dados incompletos"}), 400
        
        name = data['name']
        action_str = data['action'].lower()
        duration = float(data['duration'])
        
        if action_str not in ['decolar', 'pousar']:
            return jsonify({"success": False, "error": "Ação inválida"}), 400
        
        if duration <= 0 or duration > 60:
            return jsonify({"success": False, "error": "Duração deve ser entre 1 e 60 segundos"}), 400
        
        action = PlaneAction.TAKEOFF if action_str == 'decolar' else PlaneAction.LANDING
        plane_id = airport.create_plane(name, action, duration)
        
        return jsonify({
            "success": True, 
            "data": {
                "plane_id": plane_id,
                "message": f"Avião {name} criado com sucesso!"
            }
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/airport/reset', methods=['POST'])
def reset_airport():
    """Reinicia o aeroporto"""
    try:
        airport.reset_airport()
        return jsonify({"success": True, "message": "Aeroporto reiniciado!"})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/airport/config', methods=['POST'])
def configure_airport():
    """Configura número de pistas"""
    try:
        data = request.get_json()
        runways = int(data.get('runways', 2))
        
        if runways < 1 or runways > 5:
            return jsonify({"success": False, "error": "Número de pistas deve ser entre 1 e 5"}), 400
        
        airport.configure_runways(runways)
        
        return jsonify({
            "success": True, 
            "message": f"Aeroporto configurado com {runways} pistas!"
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    print("🏗️  Iniciando servidor do aeroporto...")
    print("📡 API disponível em: http://localhost:5001")
    print("✈️  Torre de controle operacional!")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5001, threaded=True)
    except KeyboardInterrupt:
        print("\n🔴 Encerrando servidor...")
        airport.shutdown()
