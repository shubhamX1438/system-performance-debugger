import time
import psutil
import random
from flask import Flask, jsonify
from flask_cors import CORS  #
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Function to collect system metrics
def collect_system_metrics():
    # CPU usage
    cpu_usage = psutil.cpu_percent(interval=1)
    
    # Memory usage
    memory_usage = psutil.virtual_memory().percent
    
    # Swap memory usage
    swap_usage = psutil.swap_memory().percent
    
    # Disk usage
    disk_usage = psutil.disk_usage('/').percent
    
    # Disk I/O stats
    disk_io = psutil.disk_io_counters()
    
    # Network stats (bytes sent/received)
    net_io = psutil.net_io_counters()
    
    # Process information: top 5 processes by CPU usage
    top_processes = []
    for p in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            cpu_percent = p.info['cpu_percent']
            if cpu_percent is not None:
                top_processes.append((p.info['pid'], p.info['name'], cpu_percent))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Handle processes that are terminated or inaccessible
            pass
    
    # Sort processes by CPU usage (in descending order)
    top_processes.sort(key=lambda x: x[2], reverse=True)
    
    # Battery status (if available)
    battery = psutil.sensors_battery()
    battery_status = battery.percent if battery else "N/A"
    
    # Return the metrics as a dictionary
    return {
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "swap_usage": swap_usage,
        "disk_usage": disk_usage,
        "disk_io_read_count": disk_io.read_count,
        "disk_io_write_count": disk_io.write_count,
        "net_io_bytes_sent": net_io.bytes_sent,
        "net_io_bytes_recv": net_io.bytes_recv,
        "top_processes": top_processes[:5],  # Limit to top 5 processes
        "battery_status": battery_status,
    }


@app.route("/metrics", methods=["GET"])
def get_metrics():
    # Simulate GCP data by calling the collect_system_metrics function
    metrics = collect_system_metrics()
    return jsonify(metrics)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
