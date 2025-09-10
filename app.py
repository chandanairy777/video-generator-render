from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Meditation Video Generator API (Flask)"

@app.route("/generate", methods=["GET"])
def generate_video():
    frequency = request.args.get("frequency", default=528, type=int)
    minutes = request.args.get("minutes", default=1, type=int)

    # Run video generator script
    subprocess.run(["python", "generate_video.py", str(frequency), str(minutes)])

    filename = f"output_{frequency}Hz.mp4"
    return jsonify({
        "status": "success",
        "file": filename,
        "frequency": frequency,
        "minutes": minutes
    })

# Required for some hosting platforms
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
