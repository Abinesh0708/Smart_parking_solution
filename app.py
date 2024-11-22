from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS  # Enable CORS for cross-origin requests

# Initialize Flask app
app = Flask(__name__)

# Enable CORS (to allow connections from other origins)
CORS(app)

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")  # Accept requests from any origin for testing

# Sample parking slot status
parking_slot = {"slot_1": "available"} 

@app.route('/status')
def status():
    """Endpoint to get the current parking slot status."""
    return jsonify(parking_slot)

@socketio.on('connect')
def handle_connect():
    """Handle socket connection and emit the current parking slot status."""
    emit('update', parking_slot)  # Emit the parking slot status to the client

if __name__ == "__main__":
    # Run Flask with Socket.IO                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmn
    socketio.run(app, host="127.0.0.1", port=5000)
