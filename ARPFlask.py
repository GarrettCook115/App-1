from flask import Flask, render_template, request
import subprocess
import sys

    
# Ensure Windows execution
if sys.platform != "win32":
    print("This application only functions on a Windows System")
    

app = Flask(__name__)

# Command Execution
def execute_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

@app.route("/")
def index():
    return render_template("ARP.html")

@app.route("/run_command", methods=["POST"])
def run_command():
    command = request.form["command"]
    
    command_map = {
        "ipconfig": "ipconfig /all",
        "arp": "arp -a",
        "nslookup": "nslookup google.com"
        
    }

    cmd = command_map.get(command, None)
    if not cmd:
        return "Invalid command selected!"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    print(f"Executing command: {cmd}")  # Debugging
    print(f"Command Output:\n{result.stdout}")  # Debugging
    
    return f"<pre>{output}</pre>"

if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
