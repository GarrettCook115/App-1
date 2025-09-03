from flask import Flask, render_template ,request
import subprocess
import sys
import webbrowser



###Operating Pyhon Application

app = Flask(__name__)
app.config['Explain_Template_Loading'] = True

# Command Execution
if sys.platform =="win32":
    command_map={
        "ipconfig": "ipconfig /all ",
        "arp": "arp -a",
        "nslookup": "nslookup google.com",
        "netstat": "netstat"
        
    }
else:
    command_map = {
        "ipconfig": "ip a",
        "arp": "arp -a",
        "nslookup": "dig google.com",
        "netstat": "netstat"

        
    }

def execute_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

@app.route("/")
def index():
    return render_template("ARP.html", commands=list(command_map.keys()))

@app.route("/run_command", methods=["POST"])
def run_command():
    command = request.form.get("command","").lower()
    cmd = command_map.get(command)

    if not cmd:
        return "Invalid command selected!", 400
    
    try:
        output = execute_command(cmd)
        return f"<pre>{output}</pre>"
    
    except Exception as e:
        return f"<pre>Command Execution failed: {str(e)}</pre>", 500

from waitress import serve

if __name__=="__main__":
    # Uncomment below for Windows-specific behavior
    # if sys.platform =="win32":
    #     webbrowser.open("http://127.0.0.1:5000")
    #     app.run(debug=True)
    # else:

    serve(app, host="0.0.0.0", port=8080)