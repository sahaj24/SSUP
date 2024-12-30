from flask import Flask, render_template, jsonify
import time
import random
import threading

app = Flask(__name__)

# Store simulated ESP32 data
sensor_data = []

# Right now i dont have the gas and pressure sensor for esp32, So i give random data 
def simulate_esp32_data():
    while True:
        simulated_data = {
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
            "temperature": round(random.uniform(20.0, 40.0), 2),
            "humidity": round(random.uniform(30.0, 70.0), 2),
            "gasLevel": round(random.uniform(0.0, 500.0), 2),
            "pressure": round(random.uniform(90000.0, 110000.0), 2)
        }
        sensor_data.append(simulated_data)
        if len(sensor_data) > 20:
            sensor_data.pop(0)
        time.sleep(2)  

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    return jsonify(sensor_data)

if __name__ == '__main__':
    threading.Thread(target=simulate_esp32_data, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
