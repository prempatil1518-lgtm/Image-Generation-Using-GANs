import os
from pathlib import Path

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

from services.generator_service import GeneratorService

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "generator.pth"
GENERATED_DIR = BASE_DIR / "generated"

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}})

service = None
startup_error = None

if not MODEL_PATH.exists():
    startup_error = f"Generator model not found at {MODEL_PATH}"
else:
    try:
        service = GeneratorService(MODEL_PATH, GENERATED_DIR)
        print(f"Generator loaded on {service.device} from {MODEL_PATH}")
    except Exception as exc:
        startup_error = str(exc)
        print(f"Failed to load generator: {exc}")


@app.get("/")
def home():
    return jsonify({"message": "GAN Face Generator API is running"})


@app.get("/api/health")
def health():
    if startup_error:
        return jsonify({"success": False, "error": startup_error}), 500
    return jsonify({"success": True, "device": str(service.device)})


@app.post("/api/generate")
def generate():
    if service is None:
        return jsonify({"success": False, "error": "Generator model is not available."}), 500

    try:
        filename = service.generate()
        return jsonify({
            "success": True,
            "image_url": f"/generated/{filename}",
        })
    except Exception as exc:
        app.logger.exception("Image generation failed")
        return jsonify({"success": False, "error": "Unable to generate image."}), 500


@app.get("/generated/<path:filename>")
def generated_file(filename):
    return send_from_directory(GENERATED_DIR, filename)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5101")), debug=False)
    






    


