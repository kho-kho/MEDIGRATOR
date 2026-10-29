"""
MEDIGRATOR: AI-Driven Medical Waste Detection & Intelligent Segregation
Detection System & Real-Time Inference Engine
Directly wraps Ultralytics YOLO11 model weights (models/best.pt).
Executes real computer vision inference on input images and video streams.
Maps detections to biomedical waste segregation protocols adhering to CPCB & WHO norms.

Strict Rule: No dummy or fake predictions. If dependencies or weights are missing,
it raises clear diagnostic errors detailing what is required.
"""

import os
import sys
import time
import base64
import io
import platform
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

# Import local segregation rules
from src.segregation_rules import (
    get_waste_guideline,
    evaluate_detection,
    summarize_detections,
    CLASSES,
    BIN_CATEGORIES_METADATA
)

# Global singleton cache for YOLO model
_CACHED_MODEL = None
_CACHED_WEIGHTS_PATH = None


def compute_iou(boxA: List[float], boxB: List[float]) -> float:
    """Computes Intersection-over-Union (IoU) between two bounding boxes [x1, y1, x2, y2]."""
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    interArea = max(0.0, xB - xA) * max(0.0, yB - yA)
    boxAArea = max(0.0, boxA[2] - boxA[0]) * max(0.0, boxA[3] - boxA[1])
    boxBArea = max(0.0, boxB[2] - boxB[0]) * max(0.0, boxB[3] - boxB[1])

    iou = interArea / float(boxAArea + boxBArea - interArea + 1e-6)
    return float(iou)


class SimpleIoUTracker:
    """
    Lightweight, deterministic IoU-based multi-object tracker for video streams.
    Tracks bounding boxes across consecutive frames using class matching and IoU spatial overlap.
    Assigns persistent integer track IDs, preventing duplicate counting of the same physical item.
    """
    def __init__(self, iou_threshold: float = 0.30, max_lost_frames: int = 5):
        self.iou_threshold = iou_threshold
        self.max_lost_frames = max_lost_frames
        self.next_id = 1
        self.active_tracks: Dict[int, Dict[str, Any]] = {}
        self.all_unique_objects: Dict[int, Dict[str, Any]] = {}

    def update(self, detections: List[Dict[str, Any]], frame_idx: int) -> List[Dict[str, Any]]:
        """
        Associates current frame detections with existing tracks or registers new unique objects.
        Returns detections augmented with assigned track_id.
        """
        matched_detections = []
        unmatched_dets = list(range(len(detections)))
        matched_tracks = set()

        # Step 1: Match with active tracks
        for track_id, track in list(self.active_tracks.items()):
            best_iou = 0.0
            best_det_idx = -1

            for det_idx in unmatched_dets:
                det = detections[det_idx]
                if det["class_name"] == track["class_name"]:
                    iou = compute_iou(det["bbox"], track["bbox"])
                    if iou >= self.iou_threshold and iou > best_iou:
                        best_iou = iou
                        best_det_idx = det_idx

            if best_det_idx >= 0:
                # Update existing track
                det = detections[best_det_idx]
                track["bbox"] = det["bbox"]
                track["last_frame"] = frame_idx
                track["lost_count"] = 0
                track["frame_count"] += 1
                if det["confidence"] > track["max_confidence"]:
                    track["max_confidence"] = det["confidence"]

                det_copy = dict(det)
                det_copy["track_id"] = track_id
                matched_detections.append(det_copy)
                matched_tracks.add(track_id)
                unmatched_dets.remove(best_det_idx)

                # Update registry of all unique items
                self.all_unique_objects[track_id]["max_confidence"] = track["max_confidence"]
                self.all_unique_objects[track_id]["last_frame"] = frame_idx
                self.all_unique_objects[track_id]["frame_count"] = track["frame_count"]
                self.all_unique_objects[track_id]["last_bbox"] = det["bbox"]

        # Step 2: Increment lost count for unmatched active tracks
        for track_id, track in list(self.active_tracks.items()):
            if track_id not in matched_tracks:
                track["lost_count"] += 1
                if track["lost_count"] > self.max_lost_frames:
                    del self.active_tracks[track_id]

        # Step 3: Register new tracks for unmatched detections
        for det_idx in unmatched_dets:
            det = detections[det_idx]
            new_id = self.next_id
            self.next_id += 1

            track_record = {
                "track_id": new_id,
                "class_name": det["class_name"],
                "bbox": det["bbox"],
                "max_confidence": det["confidence"],
                "first_frame": frame_idx,
                "last_frame": frame_idx,
                "frame_count": 1,
                "lost_count": 0
            }
            self.active_tracks[new_id] = track_record

            self.all_unique_objects[new_id] = {
                "track_id": new_id,
                "class_name": det["class_name"],
                "max_confidence": det["confidence"],
                "first_frame": frame_idx,
                "last_frame": frame_idx,
                "frame_count": 1,
                "last_bbox": det["bbox"]
            }

            det_copy = dict(det)
            det_copy["track_id"] = new_id
            matched_detections.append(det_copy)

        return matched_detections


def check_runtime_environment() -> Dict[str, Any]:
    """
    Inspects whether PyTorch, Ultralytics, and OpenCV are installed, detects real hardware,
    and checks model weights presence on disk.
    """
    status = {
        "ready": True,
        "missing_packages": [],
        "weights_found": False,
        "weights_path": "models/best.pt",
        "weights_size_mb": 0.0,
        "device": "CPU",
        "cuda_available": False,
        "gpu_name": None,
        "torch_version": None,
        "ultralytics_version": None,
        "platform": platform.platform(),
        "processor": platform.processor() or "x86_64"
    }

    # Check PyTorch
    try:
        import torch
        status["torch_version"] = torch.__version__
        status["cuda_available"] = torch.cuda.is_available()
        if torch.cuda.is_available():
            status["gpu_name"] = torch.cuda.get_device_name(0)
            status["device"] = f"CUDA (GPU: {status['gpu_name']})"
        else:
            status["device"] = f"CPU ({status['processor']})"
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
    if weights_path.exists():
        status["weights_found"] = True
        status["weights_path"] = str(weights_path)
        status["weights_size_mb"] = round(weights_path.stat().st_size / (1024 * 1024), 2)
    else:
        # Fallback check in runs folder
        fallback = Path("runs/detect/biomedical_waste_baseline/weights/best.pt")
        if fallback.exists():
            status["weights_found"] = True
            status["weights_path"] = str(fallback)
            status["weights_size_mb"] = round(fallback.stat().st_size / (1024 * 1024), 2)
        else:
            status["weights_found"] = False

    if status["missing_packages"] or not status["weights_found"]:
        status["ready"] = False

    return status


def get_system_transparency_info() -> Dict[str, Any]:
    """
    Returns authentic system transparency information for project evaluation:
      - Actual model name, architecture, and version
      - Real inference compute device (CPU or GPU)
      - Authentic dataset name, split, and Roboflow metadata
      - Supported model classes count
      - Current model loading or inference status
    No hardcoded GPU claims or fabricated test metrics.
    """
    env = check_runtime_environment()
    global _CACHED_MODEL

    model_status = "Not Loaded (Weights Present)"
    if _CACHED_MODEL is not None:
        model_status = "Model Loaded & Operational (Cached in RAM)"
    elif env["weights_found"]:
        model_status = "Weights Available on Disk"
    else:
        model_status = "Weights Checkpoint Missing"

    return {
        "success": True,
        "model": {
            "name": "YOLO11n-Biomedical-Waste",
            "architecture": "Ultralytics YOLO11 (Nano)",
            "version": f"YOLOv11 (Ultralytics v{env.get('ultralytics_version', '8.4.x')})",
            "weights_file": env["weights_path"],
            "weights_found": env["weights_found"],
            "weights_size_mb": env["weights_size_mb"],
            "input_resolution": "640x640 (RGB)",
            "status": model_status
        },
        "hardware": {
            "device": env["device"],
            "cuda_available": env["cuda_available"],
            "gpu_name": env["gpu_name"],
            "torch_version": env["torch_version"],
            "platform": env["platform"],
            "processor": env["processor"]
        },
        "dataset": {
            "name": "Biomedical Waste Detection",
            "version": "v3 (2026)",
            "format": "YOLOv11 PyTorch",
            "source": "Roboflow Universe (biowastemanagement/biomedical-waste-detection-nv7fq-bpeeu)",
            "total_classes": len(CLASSES),
            "classes": CLASSES
        }
    }


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
    verification_threshold: float = 0.50,
    imgsz: int = 640,
    device: Optional[str] = None
) -> Dict[str, Any]:
    """
    Runs genuine YOLO11 inference on an input image.
    Applies regulatory evaluation, flags low-confidence (<0.50) detections for human verification,
    and returns annotated visualization with comprehensive segregation metrics.
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

    if device is None:
        device = "0" if env_status["cuda_available"] else "cpu"

    model = get_yolo_model(env_status["weights_path"])

    start_time = time.perf_counter()

    # Execute YOLO inference
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
            "device": env_status["device"],
            "annotated_image_b64": "",
            "detections": [],
            "summary": summarize_detections([]),
            "model_classes": CLASSES,
            "transparency": get_system_transparency_info()
        }

    result = results[0]

    # Render bounding boxes onto image
    annotated_bgr = result.plot()
    
    # Encode annotated image to Base64 JPEG
    success, buffer = cv2.imencode(".jpg", annotated_bgr)
    annotated_b64 = "data:image/jpeg;base64," + base64.b64encode(buffer).decode("utf-8") if success else ""

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
            confidence = float(confs[i])
            bbox = [round(float(c), 1) for c in xyxy[i]]

            # Evaluate with segregation rules & verification threshold
            evaluated = evaluate_detection(
                class_name=cls_name,
                confidence=confidence,
                bbox=bbox,
                detection_id=i + 1,
                conf_threshold=conf_threshold,
                verification_threshold=verification_threshold
            )
            evaluated["class_id"] = cls_id
            detections.append(evaluated)

    # Sort detections by confidence descending
    detections.sort(key=lambda d: d["confidence"], reverse=True)

    summary = summarize_detections(detections)

    return {
        "success": True,
        "latency_ms": latency_ms,
        "device": env_status["device"],
        "annotated_image_b64": annotated_b64,
        "detections": detections,
        "summary": summary,
        "model_classes": list(result.names.values()) if result.names else CLASSES,
        "transparency": get_system_transparency_info()
    }


def run_inference_on_video(
    video_path: str,
    conf_threshold: float = 0.25,
    iou_threshold: float = 0.45,
    verification_threshold: float = 0.50,
    max_frames: int = 30,
    sample_fps: float = 2.0,
    device: Optional[str] = None
) -> Dict[str, Any]:
    """
    Processes video input with object tracking:
      - Samples video frames evenly (avoiding timeouts while capturing motion)
      - Tracks objects across frames with SimpleIoUTracker
      - Assigns persistent tracking IDs to avoid repeatedly counting the same physical item
      - Extracts representative keyframes with bounding box visualizations
      - Computes genuine deduplicated clinical segregation metrics
    """
    import cv2
    import numpy as np

    env_status = check_runtime_environment()
    if not env_status["ready"]:
        return {
            "success": False,
            "error": "Model or dependencies not ready for video inference.",
            "environment": env_status
        }

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        return {
            "success": False,
            "error": f"Could not open video file at '{video_path}'. Ensure the video is a valid MP4/WEBM/AVI file."
        }

    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    duration_sec = round(total_frames / fps, 2) if total_frames > 0 else 0.0

    # Determine frame step interval to sample at ~sample_fps
    frame_step = max(1, int(fps / sample_fps))
    
    # Cap total sampled frames to max_frames for responsive real-time inference
    if total_frames > 0 and (total_frames // frame_step) > max_frames:
        frame_step = max(1, total_frames // max_frames)

    model = get_yolo_model(env_status["weights_path"])
    tracker = SimpleIoUTracker(iou_threshold=0.30, max_lost_frames=6)

    processed_frames = []
    keyframes = []
    sampled_frame_count = 0
    frame_idx = 0

    start_time = time.perf_counter()

    while cap.isOpened():
        ret, frame_bgr = cap.read()
        if not ret:
            break

        if frame_idx % frame_step == 0:
            sampled_frame_count += 1

            # Run inference on frame
            results = model.predict(
                source=frame_bgr,
                conf=conf_threshold,
                iou=iou_threshold,
                imgsz=640,
                device="0" if env_status["cuda_available"] else "cpu",
                save=False,
                verbose=False
            )

            frame_dets = []
            if results and len(results) > 0:
                res = results[0]
                if res.boxes is not None and len(res.boxes) > 0:
                    xyxy = res.boxes.xyxy.cpu().numpy()
                    confs = res.boxes.conf.cpu().numpy()
                    classes = res.boxes.cls.cpu().numpy().astype(int)
                    names_dict = res.names or {}

                    for j in range(len(classes)):
                        c_id = int(classes[j])
                        c_name = names_dict.get(c_id, f"class_{c_id}")
                        conf = float(confs[j])
                        bbox = [round(float(c), 1) for c in xyxy[j]]
                        frame_dets.append({
                            "class_name": c_name,
                            "confidence": conf,
                            "bbox": bbox
                        })

            # Update tracker with detections from this frame
            tracked_dets = tracker.update(frame_dets, sampled_frame_count)

            # Draw bounding boxes with track IDs on this frame
            annotated_frame = frame_bgr.copy()
            for td in tracked_dets:
                b = [int(v) for v in td["bbox"]]
                t_id = td.get("track_id", 0)
                c_name = td["class_name"]
                c_conf = round(td["confidence"] * 100, 1)
                label = f"ID #{t_id}: {c_name} {c_conf}%"

                # Color coding based on whether confidence is high
                box_color = (0, 200, 100) if td["confidence"] >= verification_threshold else (0, 165, 255)
                cv2.rectangle(annotated_frame, (b[0], b[1]), (b[2], b[3]), box_color, 2)
                cv2.putText(
                    annotated_frame,
                    label,
                    (b[0], max(15, b[1] - 6)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    box_color,
                    2
                )

            # Save representative keyframes (first, last, and frames with detections)
            if len(keyframes) < 6 and (len(tracked_dets) > 0 or sampled_frame_count == 1):
                ok, buf = cv2.imencode(".jpg", annotated_frame)
                if ok:
                    b64 = "data:image/jpeg;base64," + base64.b64encode(buf).decode("utf-8")
                    timestamp_sec = round(frame_idx / fps, 2)
                    keyframes.append({
                        "frame_number": sampled_frame_count,
                        "timestamp_sec": timestamp_sec,
                        "detections_count": len(tracked_dets),
                        "annotated_b64": b64
                    })

            if sampled_frame_count >= max_frames:
                break

        frame_idx += 1

    cap.release()
    total_time_ms = round((time.perf_counter() - start_time) * 1000, 1)

    # Process all unique tracked objects (deduplicated across entire video)
    unique_objects = []
    for track_id, item in tracker.all_unique_objects.items():
        evaluated = evaluate_detection(
            class_name=item["class_name"],
            confidence=item["max_confidence"],
            bbox=item["last_bbox"],
            detection_id=track_id,
            conf_threshold=conf_threshold,
            verification_threshold=verification_threshold,
            track_id=track_id
        )
        evaluated["frames_observed"] = item["frame_count"]
        evaluated["first_frame"] = item["first_frame"]
        evaluated["last_frame"] = item["last_frame"]
        unique_objects.append(evaluated)

    # Sort unique objects by confidence descending
    unique_objects.sort(key=lambda d: d["confidence"], reverse=True)
    summary = summarize_detections(unique_objects)

    return {
        "success": True,
        "is_video": True,
        "latency_ms": total_time_ms,
        "device": env_status["device"],
        "video_metadata": {
            "fps": round(fps, 1),
            "total_frames": total_frames,
            "duration_sec": duration_sec,
            "sampled_frames_processed": sampled_frame_count
        },
        "total_unique_objects": len(unique_objects),
        "detections": unique_objects,
        "summary": summary,
        "keyframes": keyframes,
        "transparency": get_system_transparency_info()
    }
