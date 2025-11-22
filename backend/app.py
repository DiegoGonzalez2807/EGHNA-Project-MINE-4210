from flask import Flask, request, jsonify
import traceback
import io
from PIL import Image
from model_inference import predict_fibrosis_stage

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "EGHNA-prediction-backend"
    }), 200


@app.route("/predict", methods=["POST"])
def predict():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image file found (field 'image' missing)"}), 400

        file = request.files["image"]

        if file.filename == "":
            return jsonify({"error": "Empty filename"}), 400

        img_bytes = file.read()
        image = Image.open(io.BytesIO(img_bytes)).convert("RGB")

        fibrosis_stage = predict_fibrosis_stage(image)

        return jsonify({"fibrosis_stage": fibrosis_stage}), 200

    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "details": str(e),
            "trace": traceback.format_exc()
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)