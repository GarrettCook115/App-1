# app.py
from flask import Flask, request, jsonify
import subprocess
import platform

app = Flask(__name__)
os_name = platform.system()

commands = {
    "Windows": {
        "ARP Table": "arp /a",
        "IP Config": "ipconfig",
        "System Info": "SystemInfo",
        "Performance Monitor": "Perfmon.msc",
        "System Version": "Winver"
    },
    "Linux": {
        "ARP Table": "arp -a",
        "IP addr TCP/IP Info": "ifconfig",
        "System's Uptime": "uptime",
        "Memory usage and space": "free"
    },
    "Darwin": {
        "ARP Table": "arp -a",
        "IP addr TCP/IP Info": "ifconfig"
    }
}

@app.route("/commands", methods=["GET"])
def get_commands():
    return jsonify(list(commands[os_name].keys()))

@app.route("/execute", methods=["POST"])
def execute_command():
    data = request.json
    cmd = data.get("command")
    if cmd in commands[os_name]:
        result = subprocess.run(commands[os_name][cmd], shell=True, capture_output=True, text=True)
        return jsonify({"output": result.stdout})
    return jsonify({"error": "Invalid command"}), 400

if __name__ == "__main__":
    app.run(debug=True)