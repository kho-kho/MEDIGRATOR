"""
MEDIGRATOR: AI-Driven Medical Waste Detection & Intelligent Segregation
Detection System & Real-Time Inference Engine
Directly wraps Ultralytics YOLO11 model weights (models/best.pt).
Executes real computer vision inference on input images.
Maps detections to medical waste segregation protocols.

Strict Rule: No dummy or fake predictions. If dependencies or weights are missing,
it raises clear diagnostic errors detailing what is required.
"""

import os
import sys
import time
import base64
import io
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

# Import local segregation rules
from src.segregation_rules import get_waste_guideline, summarize_detections, CLASSES


# Global singleton cache for YOLO model
_CACHED_MODEL = None
_CACHED_WEIGHTS_PATH = None


def check_runtime_environment() -> Dict[str, Any]:
    """
    Inspects whether PyTorch, Ultralytics, and OpenCV are installed and whether
    the model weights file is present.
    """
    status = {
        "ready": True,
        "missing_packages": [],
        "weights_found": False,
        "weights_path": "models/best.pt",
        "device": "CPU",
        "cuda_available": False,
        "gpu_name": None,
        "torch_version": None,
        "ultralytics_version": None
    }

    # Check PyTorch
    try:
        import torch
        status["torch_version"] = torch.__version__
        status["cuda_available"] = torch.cuda.is_available()
        if torch.cuda.is_available():
            status["device"] = f"CUDA (GPU: {torch.cuda.get_device_name(0)})"
            status["gpu_name"] = torch.cuda.get_device_name(0)
    except ImportError:
        status["missing_packages"].append("torch")

    # Check Ultralytics
    try:
        import ultralytics
        status["ultralytics_version"] = ultralytics.__version__
    except ImportError:
        status["missing_packages"].append("ultralytics")

    # Check OpenCV
    try:
        import cv2
    except ImportError:
        status["missing_packages"].append("opencv-python")

    # Check Pillow
    try:
        from PIL import Image
    except ImportError:
        status["missing_packages"].append("pillow")

    # Check model weights file
    weights_path = Path("models/best.pt")
    if not weights_path.exists():
        # Fallback check
        fallback = Path("runs/detect/biomedical_waste_baseline/weights/best.pt")
        if fallback.exists():
            status["weights_found"] = True
            status["weights_path"] = str(fallback)
        else:
            status["weights_found"] = False
    else:
        status["weights_found"] = True
        status["weights_path"] = str(weights_path)

    if status["missing_packages"] or not status["weights_found"]:
        status["ready"] = False

    return status


def get_yolo_model(weights_path: str = "models/best.pt"):
    """
    Retrieves or loads the cached YOLO model instance.
    """
    global _CACHED_MODEL, _CACHED_WEIGHTS_PATH

    env_status = check_runtime_environment()
    if env_status["missing_packages"]:
        pkgs = ", ".join(env_status["missing_packages"])
        raise RuntimeError(
            f"Required computer vision packages are missing: [{pkgs}]. "
            f"Please run 'pip install -r requirements.txt' in your Python environment."
        )

    resolved_path = Path(weights_path)
    if not resolved_path.exists():
        fallback = Path("runs/detect/biomedical_waste_baseline/weights/best.pt")
        if fallback.exists():
            resolved_path = fallback
        else:
            raise FileNotFoundError(
                f"Trained model checkpoint not found at '{weights_path}'. "
                f"Ensure 'models/best.pt' exists before running inference."
            )

    if _CACHED_MODEL is not None and _CACHED_WEIGHTS_PATH == str(resolved_path):
        return _CACHED_MODEL

    from ultralytics import YOLO
    print(f"[MEDIGRATOR Engine] Loading YOLO11 detection weights from {resolved_path}...")
    _CACHED_MODEL = YOLO(str(resolved_path))
    _CACHED_WEIGHTS_PATH = str(resolved_path)
    return _CACHED_MODEL


def run_inference_on_image(
    image_input,
    conf_threshold: float = 0.25,
    iou_threshold: float = 0.45,
    imgsz: int = 640,
    device: Optional[str] = None
) -> Dict[str, Any]:
    """
    Runs actual YOLO inference on an input image (PIL Image, numpy array, or file path).

    Returns:
        dict: {
            "success": True,
            "latency_ms": float,
            "device": str,
            "annotated_image_b64": str (Base64 JPEG),
            "detections": list of dicts,
            "summary": dict,
            "model_classes": list of str
        }
    """
    env_status = check_runtime_environment()
    if not env_status["ready"]:
        error_msg = []
        if env_status["missing_packages"]:
            error_msg.append(f"Missing packages: {', '.join(env_status['missing_packages'])}")
        if not env_status["weights_found"]:
            error_msg.append(f"Model weights file not found at {env_status['weights_path']}")
        
        return {
            "success": False,
            "error": " | ".join(error_msg),
            "environment": env_status
        }

    import cv2
    import numpy as np
    from PIL import Image

    # Determine execution device
    if device is None:
        device = "0" if env_status["cuda_available"] else "cpu"

    model = get_yolo_model(env_status["weights_path"])

    start_time = time.perf_counter()

    # Run inference
    results = model.predict(
        source=image_input,
        conf=conf_threshold,
        iou=iou_threshold,
        imgsz=imgsz,
        device=device,
        save=False,
        verbose=False
    )

    latency_ms = round((time.perf_counter() - start_time) * 1000, 1)

    if not results or len(results) == 0:
        return {
            "success": True,
            "latency_ms": latency_ms,
            "device": device,
            "annotated_image_b64": "",
            "detections": [],
            "summary": summarize_detections([]),
            "model_classes": CLASSES
        }

    result = results[0]

    # Render bounding boxes onto the image using YOLO's native plot method
    annotated_bgr = result.plot()
    
    # Encode annotated image to Base64 JPEG
    success, buffer = cv2.imencode(".jpg", annotated_bgr)
    if success:
        annotated_b64 = "data:image/jpeg;base64," + base64.b64encode(buffer).decode("utf-8")
    else:
        annotated_b64 = ""

    # Extract detected bounding boxes and metadata
    detections: List[Dict[str, Any]] = []
    
    if result.boxes is not None and len(result.boxes) > 0:
        boxes = result.boxes
        xyxy = boxes.xyxy.cpu().numpy()
        confs = boxes.conf.cpu().numpy()
        classes = boxes.cls.cpu().numpy().astype(int)

        names_dict = result.names or {}

        for i in range(len(classes)):
            cls_id = int(classes[i])
            cls_name = names_dict.get(cls_id, f"class_{cls_id}")
            confidence = round(float(confs[i]), 4)
            bbox = [round(float(c), 1) for c in xyxy[i]]

            guideline = get_waste_guideline(cls_name)

            detections.append({
                "id": i + 1,
                "class_id": cls_id,
                "class_name": cls_name,
                "confidence": confidence,
                "confidence_percent": round(confidence * 100, 1),
                "bbox": bbox,
                "display_name": guideline.get("display_name", cls_name.title()),
                "bin_color": guideline.get("bin_color", "Yellow"),
                "bin_hex": guideline.get("bin_hex", "#EAB308"),
                "category_title": guideline.get("category_title", "Biohazard"),
                "hazard_level": guideline.get("hazard_level", "Moderate"),
                "treatment": guideline.get("treatment", "Sterilization / Incineration"),
                "handling_instructions": guideline.get("handling_instructions", []),
                "cpcb_schedule": guideline.get("cpcb_schedule", "Schedule I")
            })

    # Sort detections by confidence descending
    detections.sort(key=lambda d: d["confidence"], reverse=True)

    summary = summarize_detections(detections)

    return {
        "success": True,
        "latency_ms": latency_ms,
        "device": f"{'GPU' if device != 'cpu' else 'CPU'} ({env_status.get('gpu_name') or 'CPU'})",
        "annotated_image_b64": annotated_b64,
        "detections": detections,
        "summary": summary,
        "model_classes": list(result.names.values()) if result.names else CLASSES
    }

