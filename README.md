# MEDIGRATOR: AI-Driven Medical Waste Detection & Intelligent Segregation

An academic Computer Vision system engineered to identify, localize, and classify medical waste into standardized disposal categories using state-of-the-art object detection (Ultralytics YOLO11) and automated WHO/CPCB segregation protocols.

> **Project Scope:** This is a software and computer vision research project. Physical robotic sorting hardware is outside the current scope. All training and inference are designed for flexible, reproducible execution across local workstations and GPU compute machines.

---

## 1. Project Overview & Architecture

Proper segregation of biomedical waste is critical in hospital environments to prevent nosocomial infections, chemical contamination, and injuries from medical sharps. **MEDIGRATOR** combines deep learning object detection with regulatory waste management rules to automatically classify 14 distinct clinical waste items and advise staff on correct color-coded bin disposal.

### Project Directory Structure
```text
MEDIGRATOR/
├── dataset/
│   ├── data.yaml            # YOLO dataset configuration & class names
│   ├── README.dataset.txt   # Dataset source reference
│   └── README.roboflow.txt  # Dataset export specifications
├── models/
│   ├── best.pt              # Trained YOLO11n detection weights (5.48 MB)
│   └── README.md            # Guidelines for storing trained model weights
├── scripts/
│   └── verify_gpu.py        # CUDA & GPU hardware diagnostic script
├── src/
│   ├── train.py             # Configurable YOLO training pipeline
│   ├── predict.py           # Multi-source inference CLI (image/video/webcam)
│   ├── inference.py         # Real-time inference engine for web application
│   └── segregation_rules.py # CPCB & WHO biomedical waste segregation knowledge base
├── static/
│   ├── css/style.css        # Dashboard styling & glassmorphism accents
│   ├── js/app.js            # Frontend application logic & webcam handling
│   └── samples/             # Bundled demo images for one-click testing
├── templates/
│   └── index.html           # Modern, responsive MEDIGRATOR web dashboard
├── app.py                   # Flask web server and REST API
├── requirements.txt         # Core project dependencies
├── .gitignore               # Excludes large binaries, weights, venv, and datasets
└── README.md                # Project documentation
```

---

## 2. Dataset Information

The dataset is sourced from **Roboflow Universe**:
- **Dataset Title:** Biomedical Waste Detection (v3)
- **Source Link:** [Roboflow Universe - Biomedical Waste Detection](https://universe.roboflow.com/biowastemanagement/biomedical-waste-detection-nv7fq-bpeeu/dataset/3)
- **License:** CC BY 4.0
- **Total Images:** 5,319
  - **Train split:** 4,569 images
  - **Validation split:** 463 images
  - **Test split:** 287 images

### 14 Clinical Waste Target Classes
| Class ID | Class Name | Description / Clinical Waste Category | Assigned Disposal Bin |
|:---:|:---|:---|:---|
| `0` | `fluid bottle` | Saline, IV fluid containers, chemical bottles | 🔴 Red Bin (Recyclable Plastic) |
| `1` | `gauze` | Clean / general surgical cotton gauze | 🟡 Yellow Bin (Soiled / Infectious) |
| `2` | `glass` | Ampoules, glass vials, medicine bottles | 🔵 Blue Box (Glassware) |
| `3` | `glove` | Examination gloves (latex / nitrile) | 🔴 Red Bin (Contaminated Plastic) |
| `4` | `mask` | Surgical / N95 disposable masks | 🟡 Yellow Bin (Infectious PPE) |
| `5` | `needle` | Hypodermic injection needles (sharps) | ⚪ White Box (Puncture-Proof Sharps) |
| `6` | `needle cap` | Plastic protective caps for needles | 🔴 Red Bin (Recyclable Plastic) |
| `7` | `paper` | Medical wrappers, prescription pads, towel sheets | ⚫ Black/Green (General Municipal) |
| `8` | `plastic` | Generic non-bottle medical plastic containers | 🔴 Red Bin (Recyclable Plastic) |
| `9` | `scrub` | Medical scrubs, fabric caps, gowns | 🟡 Yellow Bin (Soiled Linen) |
| `10` | `test tube` | Blood collection tubes (Vacutainers, etc.) | 🔵 Blue Box (Glass) / 🟡 Yellow |
| `11` | `tube` | IV lines, catheter tubing, infusion tubes | 🔴 Red Bin (Contaminated Plastic) |
| `12` | `unused gauze` | Sealed / pristine gauze packs | ⚫ Black/Green (General Non-Hazardous) |
| `13` | `used syringe` | Syringe barrels with plunger assembly | ⚪ White Box (Sharps) / 🔴 Red Bin |

### Class Distribution & Known Imbalance
Object instance counts across the dataset:
- `glove`: 1,413
- `used syringe`: 1,136
- `paper`: 884
- `gauze`: 776
- `needle`: 742
- `mask`: 659
- `tube`: 558
- `test tube`: 468
- `fluid bottle`: 413
- `plastic`: 142
- `unused gauze`: 141
- `needle cap`: 113
- `scrub`: 34
- `glass`: 31

> ⚠️ **Class Imbalance & Validation Limitations:**
> The dataset is heavily imbalanced toward common PPE and disposables (`glove`, `used syringe`, `paper`), while classes like `scrub` (34 instances) and `glass` (31 instances) are rare.
> Crucially, the validation set contains **0 `scrub` instances** and only **2 `glass` instances**. Consequently, validation metrics (such as per-class mAP@50) for `scrub` and `glass` will have high variance or reflect sample sparsity. This limitation is acknowledged upfront in our project report.

---

## 3. Software Stack & Environment

- **OS:** Windows / Linux / macOS
- **Python:** 3.10+ / 3.11.x / 3.13.x
- **Deep Learning Framework:** PyTorch (>=2.0.0) with CUDA acceleration
- **Object Detection Architecture:** Ultralytics YOLO11 (YOLO11n lightweight baseline)
- **Web Application Framework:** Flask 3.x
- **Frontend Stack:** HTML5, Tailwind CSS, Lucide Icons, Vanilla JavaScript
- **Computer Vision Utilities:** OpenCV, Pillow, Matplotlib, PyYAML

---

## 4. Setup Guide for Local & GPU Execution

Follow these steps when setting up the project locally:

### Step 1: Navigate to Repository
```bash
cd BiomedicalwasteAI
```

### Step 2: Create and Activate Virtual Environment
**On Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
**On Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install CUDA-Enabled PyTorch & Dependencies
To ensure an NVIDIA GPU is utilized:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
pip install -r requirements.txt
```
*(If testing on CPU only, simply run `pip install -r requirements.txt`).*

### Step 4: Verify Hardware Diagnostics
Run the diagnostic script:
```bash
python scripts/verify_gpu.py
```
Expected output:
```text
============================================================
MEDIGRATOR - PyTorch & Hardware Diagnostic Verification
============================================================
Python Version       : 3.x.x
PyTorch Version      : 2.x.x
CUDA Available       : True (or False for CPU)
============================================================
```

---

## 5. Model Training Pipeline

We use **YOLO11n** (`yolo11n.pt`) as our baseline detection architecture. It offers fast inference speeds, low VRAM footprint, and high accuracy for embedded/edge deployment.

### Run Training with Sensible Defaults
```bash
python src/train.py
```
This automatically selects GPU `0` (or CPU fallback), runs 50 epochs, batch size 8, and input resolution 640x640.

### Configurable Training Options
You can customize hyperparameters via command-line arguments:
```bash
python src/train.py --epochs 100 --batch 16 --imgsz 640 --device 0 --workers 4
```

| Parameter | Default | Description |
|:---|:---:|:---|
| `--model` | `yolo11n.pt` | Pretrained YOLO checkpoint |
| `--data` | `dataset/data.yaml` | Path to dataset configuration |
| `--epochs` | `50` | Total training epochs (with early stopping patience 15) |
| `--batch` | `8` | Batch size (reduce to `4` if VRAM < 4GB; increase to `16` or `32` if VRAM >= 12GB) |
| `--imgsz` | `640` | Input image size |
| `--device` | `None` (auto) | `0` for GPU 0, `0,1` for multi-GPU, or `cpu` |
| `--workers` | `0` | DataLoader threads (`0` recommended on Windows) |
| `--project` | `runs/detect` | Base output directory |
| `--name` | `biomedical_waste_baseline` | Experiment run name |

---

## 6. Model Inference & Testing (CLI)

The CLI inference script `src/predict.py` loads the trained weights (`models/best.pt`) and detects waste items.

### Inference on a Single Image
```bash
python src/predict.py --weights models/best.pt --source path/to/sample.jpg
```

### Inference on Test Images (Batch)
```bash
python src/predict.py --weights models/best.pt --source dataset/test/images
```

### Inference on a Video File
```bash
python src/predict.py --weights models/best.pt --source path/to/waste_video.mp4
```

### Optional Live Webcam Inference
```bash
python src/predict.py --weights models/best.pt --source 0 --show
```

---

## 7. MEDIGRATOR Interactive Web UI & Segregation Dashboard

A modern, responsive web application for real-time medical waste inference and clinical segregation guidance.

### Dashboard Capabilities
- **Exact Project Presentation:** Official **MEDIGRATOR: AI-Driven Medical Waste Detection & Intelligent Segregation** interface featuring the **MEDIGRATOR Detection Studio**.
- **Clinical / SaaS Design System:** Refined dark navy palette (`#0B1120`, `#111B2E`) with restrained teal accents (`#14B8A6`) and crisp light mode (`#F5F7FB`, `#FFFFFF`). Engineered with subtle ~1px borders (`#263449` in dark, `#E2E8F0` in light), clean typography, and balanced spacing suitable for formal academic and clinical evaluations.
- **Compact Light/Dark Mode Switcher:** Accessible, sliding theme toggle located directly in the top navigation bar. Defaults to dark mode on fresh load with smooth transitions and high contrast across all elements.
- **Visual Detection Studio:** Real-time object detection with bounding box localization, confidence percentages, and detection latency metrics.
- **Detection Settings:** Configurable confidence thresholds and IoU overlap sliders in real time.
- **Detection Results:** Visual side-by-side view toggle (annotated vs. original photo) and summary KPIs.
- **Dynamic Segregation Advisory:** Direct mapping of predicted items to official WHO and CPCB color-coded disposal streams:
  - 🟡 **Yellow:** Soiled & infectious waste (incineration / autoclaving)
  - 🔴 **Red:** Contaminated recyclable plastics (autoclaving & shredding)
  - ⚪ **White:** Puncture-proof container for sharps and needles
  - 🔵 **Blue:** Glass ampoules and medicine vials (chemical disinfection & recycling)
  - ⚫ **Black/Green:** General non-hazardous municipal waste
- **Multiple Input Modes:** Drag-and-drop file upload, live browser webcam capture, and bundled one-click demo samples (`static/samples/`).
- **Technology & Dataset Reference:** Technical specifications, 14-class regulatory directory, and clinical handling checklists for academic evaluation.

### Running the Web Application Locally

```bash
# 1. Activate virtual environment
.\.venv\Scripts\Activate.ps1

# 2. Launch the MEDIGRATOR application
python app.py
```

Open your browser and navigate to:
```text
http://127.0.0.1:5000
```

---

## 8. Next Steps & Roadmap
1. **GPU Training:** Continue fine-tuning YOLO11 on expanded high-resolution clinical datasets.
2. **Evaluation:** Analyze confusion matrices and augment minority classes (`glass`, `scrub`).
3. **Hardware Deployment:** Interface the MEDIGRATOR API with conveyor sorting systems and smart IoT-enabled hospital waste bins.
