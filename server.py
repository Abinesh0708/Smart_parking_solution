import serial
import time
from flask import Flask, jsonify
from flask_socketio import SocketIO, emit

# Initialize Flask and Socket.IO
app = Flask(__name__)  # Flask app initialization
socketio = SocketIO(app)

# Parking slot status
parking_slot = {"slot_1": "available"}

# Configure Serial communication with Arduino
arduino = serial.Serial(port='COM5', baudrate=9600, timeout=1)  # Replace 'COM5' with your Arduino port

@app.route('/status', methods=['GET'])
def get_status():
    """Endpoint to get the current parking slot status."""
    return jsonify(parking_slot)

@socketio.on('connect')
def handle_connect():
    """When a client connects, send the current parking slot status."""
    emit('update', parking_slot)

def read_from_arduino():
    """Function to read data from Arduino over serial and update parking slot status."""
    while True:
        try:
            if arduino.in_waiting > 0:
                line = arduino.readline().decode('utf-8').strip()  # Read and decode the serial input
                print(f"Raw Arduino input: {line}")  # Debugging line to see the raw data
                if line in ["occupied", "available"]:
                    parking_slot["slot_1"] = line  # Update slot status
                    socketio.emit('update', parking_slot)  # Broadcast the updated status to all connected clients
                    print(f"Slot status updated: {line}")
            time.sleep(0.1)  # Sleep to avoid overloading the CPU, adjust if necessary
        except Exception as e:
            print(f"Error reading from Arduino: {e}")

# Run the serial reading function in the background
socketio.start_background_task(read_from_arduino)

if __name__ == "__main__":  # Ensure this is executed when running the script directly
    socketio.run(app, host="0.0.0.0", port=5000)
