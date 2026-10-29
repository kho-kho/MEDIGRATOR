"""
MEDIGRATOR: AI-Driven Medical Waste Detection & Intelligent Segregation
Flask server providing REST API for real-time YOLO11 waste detection,
segregation advisory generation, and interactive dashboard UI.
"""

import os
import sys
import base64
import io
import time
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from flask import Flask, request, jsonify, render_template, send_from_directory
    from werkzeug.utils import secure_filename
except ImportError:
    print("\n" + "=" * 70)
    print("CRITICAL ERROR: Flask or Werkzeug is not installed!")
    print("Please install the required dependencies first by running:")
    print("    pip install -r requirements.txt")
    print("=" * 70 + "\n")
    sys.exit(1)

from src.inference import (
    run_inference_on_image,
    run_inference_on_video,
    check_runtime_environment,
    get_system_transparency_info
)
from src.segregation_rules import (
    SEGREGATION_RULES,
    BIN_CATEGORIES_METADATA,
    CLASSES
)

app = Flask(
    __name__,
    template_folder=str(PROJECT_ROOT / "templates"),
    static_folder=str(PROJECT_ROOT / "static")
)

# App Configuration & Immediate Template Hot-Reloading
app.config["MAX_CONTENT_LENGTH"] = 64 * 1024 * 1024  # 64MB max upload limit (supports short videos)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.jinja_env.auto_reload = True

ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "bmp"}
ALLOWED_VIDEO_EXTENSIONS = {"mp4", "webm", "avi", "mov", "mkv"}

# Ensure upload and sample directories exist
UPLOADS_DIR = PROJECT_ROOT / "static" / "uploads"
SAMPLES_DIR = PROJECT_ROOT / "static" / "samples"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
SAMPLES_DIR.mkdir(parents=True, exist_ok=True)


@app.after_request
def add_no_cache_headers(response):
    """Ensures browsers always fetch fresh UI templates and assets without caching old versions."""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


def allowed_image(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


def allowed_video(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS


@app.route("/")
def index():
    """Renders the main MEDIGRATOR dashboard."""
    env_status = check_runtime_environment()
    transparency = get_system_transparency_info()
    return render_template(
        "index.html",
        env_status=env_status,
        transparency=transparency,
        classes=CLASSES,
        bin_meta=BIN_CATEGORIES_METADATA
    )


@app.route("/api/status", methods=["GET"])
def api_status():
    """Returns system hardware, PyTorch/Ultralytics status, and model info."""
    status = check_runtime_environment()
    transparency = get_system_transparency_info()
    return jsonify({
        "success": True,
        "environment": status,
        "transparency": transparency,
        "classes": CLASSES,
        "total_classes": len(CLASSES)
    })


@app.route("/api/model-info", methods=["GET"])
def api_model_info():
    """
    Returns authentic system transparency information:
      - Model name, architecture, weights path and size
      - Compute device (CPU / GPU with real hardware identification)
      - Dataset specifications (Roboflow Universe v3)
      - Supported clinical classes and model readiness status
    """
    return jsonify(get_system_transparency_info())


@app.route("/api/classes", methods=["GET"])
def api_classes():
    """Returns full segregation metadata for all 14 classes."""
    return jsonify({
        "success": True,
        "classes": CLASSES,
        "rules": SEGREGATION_RULES,
        "bins": BIN_CATEGORIES_METADATA
    })


@app.route("/api/samples", methods=["GET"])
def api_samples():
    """Returns list of preloaded sample images for instant demo testing."""
    sample_files = []
    if SAMPLES_DIR.exists():
        for f in sorted(SAMPLES_DIR.iterdir()):
            if f.is_file() and f.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]:
                sample_files.append({
                    "filename": f.name,
                    "url": f"/static/samples/{f.name}",
                    "title": f.stem.replace("_", " ").title()
                })
    return jsonify({
        "success": True,
        "samples": sample_files
    })


@app.route("/api/predict", methods=["POST"])
def api_predict():
    """
    Runs real YOLO11 inference on an uploaded image, base64 snapshot, or sample image.
    Parameters:
        - 'conf': Confidence threshold (float, default 0.25)
        - 'iou': IoU threshold (float, default 0.45)
        - 'verification_threshold': High-confidence threshold for automated bin assignment (default 0.50)
    """
    conf = float(request.form.get("conf", request.json.get("conf", 0.25) if request.is_json else 0.25))
    iou = float(request.form.get("iou", request.json.get("iou", 0.45) if request.is_json else 0.45))
    verif_thresh = float(request.form.get("verification_threshold", request.json.get("verification_threshold", 0.50) if request.is_json else 0.50))

    # Clamp thresholds
    conf = max(0.05, min(0.95, conf))
    iou = max(0.10, min(0.90, iou))
    verif_thresh = max(0.30, min(0.95, verif_thresh))

    image_source = None
    original_b64 = None

    # Option 1: Direct Multipart File Upload
    if "file" in request.files:
        file = request.files["file"]
        if not file or file.filename == "":
            return jsonify({"success": False, "error": "No file was selected for upload."}), 400
        
        if not allowed_image(file.filename):
            return jsonify({
                "success": False,
                "error": f"Unsupported file format '{file.filename}'. Allowed image formats: {', '.join(sorted(ALLOWED_IMAGE_EXTENSIONS))}."
            }), 400

        try:
            file_bytes = file.read()
            if len(file_bytes) == 0:
                return jsonify({"success": False, "error": "Uploaded file is empty."}), 400
            image_source = file_bytes
            original_b64 = "data:image/jpeg;base64," + base64.b64encode(file_bytes).decode("utf-8")
        except Exception as e:
            return jsonify({"success": False, "error": f"Error reading uploaded image: {str(e)}"}), 400

    # Option 2: JSON Payload (Base64 webcam or sample)
    elif request.is_json:
        data = request.get_json() or {}
        if "sample_filename" in data:
            filename = secure_filename(data["sample_filename"])
            sample_path = SAMPLES_DIR / filename
            if not sample_path.exists():
                return jsonify({"success": False, "error": f"Sample image '{filename}' not found on server."}), 404
            with open(sample_path, "rb") as sf:
                file_bytes = sf.read()
                image_source = file_bytes
                original_b64 = "data:image/jpeg;base64," + base64.b64encode(file_bytes).decode("utf-8")

        elif "image_base64" in data:
            raw_b64 = data["image_base64"]
            if "," in raw_b64:
                raw_b64 = raw_b64.split(",", 1)[1]
            try:
                file_bytes = base64.b64decode(raw_b64)
                if len(file_bytes) == 0:
                    return jsonify({"success": False, "error": "Decoded webcam snapshot is empty."}), 400
                image_source = file_bytes
                original_b64 = "data:image/jpeg;base64," + raw_b64
            except Exception as e:
                return jsonify({"success": False, "error": f"Invalid base64 image data: {str(e)}"}), 400

    # Option 3: Form data sample filename
    elif "sample_filename" in request.form:
        filename = secure_filename(request.form["sample_filename"])
        sample_path = SAMPLES_DIR / filename
        if not sample_path.exists():
            return jsonify({"success": False, "error": f"Sample image '{filename}' not found on server."}), 404
        with open(sample_path, "rb") as sf:
            file_bytes = sf.read()
            image_source = file_bytes
            original_b64 = "data:image/jpeg;base64," + base64.b64encode(file_bytes).decode("utf-8")

    if image_source is None:
        return jsonify({
            "success": False,
            "error": "No valid image provided. Upload a file, capture with the live webcam, or pick a sample image."
        }), 400

    # Execute actual YOLO prediction
    try:
        from PIL import Image
        pil_image = Image.open(io.BytesIO(image_source)).convert("RGB")
        
        result = run_inference_on_image(
            image_input=pil_image,
            conf_threshold=conf,
            iou_threshold=iou,
            verification_threshold=verif_thresh
        )

        if not result["success"]:
            return jsonify(result), 500

        result["original_image_b64"] = original_b64
        return jsonify(result)

    except ImportError as ie:
        return jsonify({
            "success": False,
            "error": f"Inference failed due to missing Python libraries: {str(ie)}. Please run 'pip install -r requirements.txt'."
        }), 500
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Prediction error: {str(e)}"
        }), 500


@app.route("/api/predict-video", methods=["POST"])
def api_predict_video():
    """
    Runs video inference with multi-object tracking:
      - Accepts video file (.mp4, .webm, .avi, .mov)
      - Samples frames and executes YOLO11 object detection
      - Tracks items across frames using persistent track IDs to avoid duplicate counting
      - Generates annotated keyframes and comprehensive segregation summary
    """
    conf = float(request.form.get("conf", 0.25))
    iou = float(request.form.get("iou", 0.45))
    verif_thresh = float(request.form.get("verification_threshold", 0.50))

    conf = max(0.05, min(0.95, conf))
    iou = max(0.10, min(0.90, iou))
    verif_thresh = max(0.30, min(0.95, verif_thresh))

    if "file" not in request.files:
        return jsonify({"success": False, "error": "No video file provided in upload request."}), 400

    file = request.files["file"]
    if not file or file.filename == "":
        return jsonify({"success": False, "error": "Empty video filename."}), 400

    if not allowed_video(file.filename):
        return jsonify({
            "success": False,
            "error": f"Unsupported video format '{file.filename}'. Supported formats: {', '.join(sorted(ALLOWED_VIDEO_EXTENSIONS))}."
        }), 400

    filename = secure_filename(f"vid_{int(time.time())}_{file.filename}")
    video_path = UPLOADS_DIR / filename

    try:
        file.save(str(video_path))

        result = run_inference_on_video(
            video_path=str(video_path),
            conf_threshold=conf,
            iou_threshold=iou,
            verification_threshold=verif_thresh,
            max_frames=30,
            sample_fps=2.0
        )

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Video processing error: {str(e)}"
        }), 500
    finally:
        # Clean up temporary uploaded video file
        try:
            if video_path.exists():
                video_path.unlink()
        except Exception:
            pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("=" * 70)
    print("MEDIGRATOR: AI-DRIVEN MEDICAL WASTE DETECTION & SEGREGATION")
    print(f"Dashboard server starting on http://127.0.0.1:{port}")
    print("Press Ctrl+C to terminate.")
    print("=" * 70)
    app.run(host="0.0.0.0", port=port, debug=False)
