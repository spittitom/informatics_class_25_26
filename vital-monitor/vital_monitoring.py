from flask import Flask, jsonify, request, render_template # render_template importieren
import os

app = Flask(__name__)

# Neue Route, die das HTML-Formular anzeigt
@app.route('/')
def home():
    return render_template('index.html') # Hier wird die HTML-Datei geladen

# Die alte API-Route bleibt unverändert
@app.route('/vital-check', methods=['POST'])
def check_vitals():
    data = request.json
    heart_rate = data.get("heart_rate")
    
    # Einfache medizinische Logik
    if heart_rate > 100:
        status = "Tachycardia Warning"
    elif heart_rate < 60:
        status = "Bradycardia Warning"
    else:
        status = "Normal"
        
    return jsonify({
        "patient_id": data.get("patient_id"),
        "assessment": status,
        "bpm": heart_rate
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)