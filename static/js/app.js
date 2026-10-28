/**
 * MEDIGRATOR: AI-Driven Medical Waste Detection & Intelligent Segregation
 * Frontend Application Engine & Clinical Dashboard Controller
 */

// Application State
const state = {
    selectedFile: null,
    selectedSample: null,
    webcamBase64: null,
    webcamStream: null,
    isProcessing: false,
    activeTab: 'studio',
    lastPredictionResult: null,
    theme: 'dark' // Starts in dark mode on every fresh page load
};

// DOM Elements
const el = {
    // Theme Toggle
    themeToggleBtn: document.getElementById('theme-toggle-btn'),
    themeLabel: document.getElementById('theme-label'),
    themeIcon: document.getElementById('theme-icon'),

    // Tabs
    tabStudio: document.getElementById('tab-studio'),
    tabGuidelines: document.getElementById('tab-guidelines'),
    tabSpecs: document.getElementById('tab-specs'),
    tabBtnStudio: document.getElementById('tab-btn-studio'),
    tabBtnGuidelines: document.getElementById('tab-btn-guidelines'),
    tabBtnSpecs: document.getElementById('tab-btn-specs'),

    // Environment Banner
    envBanner: document.getElementById('env-alert-banner'),
    envMessage: document.getElementById('env-alert-message'),
    systemStatusText: document.getElementById('system-status-text'),
    systemStatusBadge: document.getElementById('system-status-badge'),

    // Dropzone & Inputs
    dropZone: document.getElementById('drop-zone'),
    fileInput: document.getElementById('file-input'),
    dropzonePrompt: document.getElementById('dropzone-prompt'),
    dropzonePreview: document.getElementById('dropzone-preview'),
    previewImg: document.getElementById('preview-img'),
    previewFilename: document.getElementById('preview-filename'),
    clearImageBtn: document.getElementById('clear-image-btn'),
    samplesContainer: document.getElementById('samples-container'),

    // Sliders
    confSlider: document.getElementById('conf-slider'),
    confVal: document.getElementById('conf-val'),
    iouSlider: document.getElementById('iou-slider'),
    iouVal: document.getElementById('iou-val'),

    // Buttons
    analyzeBtn: document.getElementById('analyze-btn'),
    analyzeBtnText: document.getElementById('analyze-btn-text'),
    analyzeSpinner: document.getElementById('analyze-spinner'),
    resetAllBtn: document.getElementById('reset-all-btn'),

    // Webcam Modal
    openWebcamBtn: document.getElementById('open-webcam-btn'),
    closeWebcamBtn: document.getElementById('close-webcam-btn'),
    cancelWebcamBtn: document.getElementById('cancel-webcam-btn'),
    snapWebcamBtn: document.getElementById('snap-webcam-btn'),
    webcamModal: document.getElementById('webcam-modal'),
    webcamVideo: document.getElementById('webcam-video'),
    webcamCanvas: document.getElementById('webcam-canvas'),

    // Results Views
    resultsPlaceholder: document.getElementById('results-placeholder'),
    resultsContainer: document.getElementById('results-container'),
    toggleAnnotatedBtn: document.getElementById('toggle-annotated-btn'),
    toggleOriginalBtn: document.getElementById('toggle-original-btn'),
    resImageAnnotated: document.getElementById('res-image-annotated'),
    resImageOriginal: document.getElementById('res-image-original'),

    // KPI Stats
    statTotalItems: document.getElementById('stat-total-items'),
    statPrimaryStream: document.getElementById('stat-primary-stream'),
    statMaxConf: document.getElementById('stat-max-conf'),
    statLatency: document.getElementById('stat-latency'),
    statHazardBadge: document.getElementById('stat-hazard-badge'),

    // Lists & Advisory
    detectionsList: document.getElementById('detections-list'),
    requiredBinsCards: document.getElementById('required-bins-cards'),
    actionChecklist: document.getElementById('action-checklist'),
    classesTableBody: document.getElementById('classes-table-body')
};

// Initialize Application
document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initEventListeners();
    fetchSystemStatus();
    fetchSampleImages();
    fetchClassesDirectory();
});

// Theme Management Logic
function initThemeToggle() {
    // Requirements: Application starts in DARK MODE on every fresh page visit.
    setTheme('dark');

    if (el.themeToggleBtn) {
        el.themeToggleBtn.addEventListener('click', toggleTheme);
        el.themeToggleBtn.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                toggleTheme();
            }
        });
    }
}

function toggleTheme() {
    const isCurrentlyDark = document.documentElement.classList.contains('dark');
    // If dark, sliding switch changes to light; if light, sliding switch restores dark
    setTheme(isCurrentlyDark ? 'light' : 'dark');
}

function setTheme(theme) {
    state.theme = theme;
    const isDark = (theme === 'dark');

    if (isDark) {
        // Dark Mode: Knob on RIGHT, label "Dark Mode"
        document.documentElement.classList.add('dark');
        if (el.themeLabel) el.themeLabel.textContent = 'Dark Mode';
        if (el.themeToggleBtn) {
            el.themeToggleBtn.setAttribute('aria-checked', 'true');
        }
        if (el.themeIcon) {
            el.themeIcon.setAttribute('data-lucide', 'moon');
            el.themeIcon.className = 'w-2.5 h-2.5 text-slate-800';
        }
    } else {
        // Light Mode: Knob on LEFT, label "Light Mode"
        document.documentElement.classList.remove('dark');
        if (el.themeLabel) el.themeLabel.textContent = 'Light Mode';
        if (el.themeToggleBtn) {
            el.themeToggleBtn.setAttribute('aria-checked', 'false');
        }
        if (el.themeIcon) {
            el.themeIcon.setAttribute('data-lucide', 'sun');
            el.themeIcon.className = 'w-2.5 h-2.5 text-amber-500';
        }
    }

    if (window.lucide) {
        lucide.createIcons();
    }
}

// Tab Navigation
function switchTab(tabName) {
    state.activeTab = tabName;
    const tabs = [
        { name: 'studio', el: el.tabStudio, btn: el.tabBtnStudio },
        { name: 'guidelines', el: el.tabGuidelines, btn: el.tabBtnGuidelines },
        { name: 'specs', el: el.tabSpecs, btn: el.tabBtnSpecs }
    ];

    tabs.forEach(t => {
        if (t.name === tabName) {
            t.el.classList.remove('hidden');
            if (t.btn) t.btn.classList.add('active');
        } else {
            t.el.classList.add('hidden');
            if (t.btn) t.btn.classList.remove('active');
        }
    });

    if (window.lucide) {
        lucide.createIcons();
    }
}

// Fetch System Environment & Diagnostics
async function fetchSystemStatus() {
    try {
        const res = await fetch('/api/status');
        const data = await res.json();
        
        if (data.success && data.environment) {
            const env = data.environment;
            if (!env.ready) {
                let missingText = '';
                if (env.missing_packages && env.missing_packages.length > 0) {
                    missingText = `Missing packages: ${env.missing_packages.join(', ')}. Run: pip install -r requirements.txt`;
                } else if (!env.weights_found) {
                    missingText = `Trained weights missing at ${env.weights_path}.`;
                }
                el.envBanner.classList.remove('hidden');
                el.envMessage.textContent = missingText;
                
                el.systemStatusText.textContent = 'Setup Needed (Check Terminal)';
                el.systemStatusBadge.className = 'system-status-pill hidden xl:inline-flex text-amber-500 border-amber-500/30';
            } else {
                el.envBanner.classList.add('hidden');
                el.systemStatusText.textContent = `MEDIGRATOR Detection Ready (${env.device})`;
                el.systemStatusBadge.className = 'system-status-pill hidden xl:inline-flex text-secondary-label';
            }
        }
    } catch (err) {
        console.warn('Could not query system status:', err);
    }
}

// Fetch Preloaded Sample Images
async function fetchSampleImages() {
    try {
        const res = await fetch('/api/samples');
        const data = await res.json();
        
        if (data.success && data.samples && data.samples.length > 0) {
            el.samplesContainer.innerHTML = '';
            data.samples.forEach(sample => {
                const card = document.createElement('div');
                card.className = 'sample-thumb-card group relative aspect-[4/3] flex flex-col justify-end p-2';
                card.innerHTML = `
                    <img src="${sample.url}" alt="${sample.title}" class="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition duration-200">
                    <div class="absolute inset-0 bg-gradient-to-t from-black/85 via-black/25 to-transparent"></div>
                    <span class="relative z-10 text-[10px] font-semibold text-white truncate drop-shadow-sm">${sample.title}</span>
                `;
                card.onclick = () => selectSample(sample);
                el.samplesContainer.appendChild(card);
            });
        } else {
            el.samplesContainer.innerHTML = `<p class="col-span-3 text-xs text-muted-desc text-center py-2">No sample images found.</p>`;
        }
    } catch (err) {
        console.warn('Failed to load sample images:', err);
    }
}

// Select a sample image
function selectSample(sample) {
    state.selectedFile = null;
    state.webcamBase64 = null;
    state.selectedSample = sample.filename;

    el.previewImg.src = sample.url;
    el.previewFilename.textContent = sample.title;
    el.dropzonePrompt.classList.add('hidden');
    el.dropzonePreview.classList.remove('hidden');

    el.analyzeBtn.disabled = false;
    el.analyzeBtnText.textContent = `Analyze ${sample.title}`;
}

// Fetch Full Classes Directory for Tab 2
async function fetchClassesDirectory() {
    try {
        const res = await fetch('/api/classes');
        const data = await res.json();
        
        if (data.success && data.rules) {
            el.classesTableBody.innerHTML = '';
            const rules = data.rules;
            
            Object.keys(rules).forEach(cName => {
                const r = rules[cName];
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-500/5 transition border-b border-divider';

                let binBadge = '';
                if (r.bin_color === 'Yellow') {
                    binBadge = '<span class="text-[11px] px-2 py-0.5 rounded-full font-semibold bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/20">🟡 Yellow</span>';
                } else if (r.bin_color === 'Red') {
                    binBadge = '<span class="text-[11px] px-2 py-0.5 rounded-full font-semibold bg-red-500/10 text-red-600 dark:text-red-400 border border-red-500/20">🔴 Red</span>';
                } else if (r.bin_color === 'White') {
                    binBadge = '<span class="text-[11px] px-2 py-0.5 rounded-full font-semibold bg-slate-500/10 text-slate-700 dark:text-slate-300 border border-slate-500/20">⚪ White Box</span>';
                } else if (r.bin_color === 'Blue') {
                    binBadge = '<span class="text-[11px] px-2 py-0.5 rounded-full font-semibold bg-blue-500/10 text-blue-600 dark:text-blue-400 border border-blue-500/20">🔵 Blue</span>';
                } else {
                    binBadge = '<span class="text-[11px] px-2 py-0.5 rounded-full font-semibold bg-slate-500/10 text-slate-700 dark:text-slate-300 border border-slate-500/20">⚫ Black</span>';
                }

                let hazardBadge = '';
                if (r.hazard_level === 'Critical') {
                    hazardBadge = '<span class="text-[11px] px-2 py-0.5 rounded-full font-semibold bg-red-500/10 text-red-600 dark:text-red-400 border border-red-500/20">Critical (Sharps)</span>';
                } else if (r.hazard_level === 'High') {
                    hazardBadge = '<span class="text-[11px] px-2 py-0.5 rounded-full font-semibold bg-orange-500/10 text-orange-600 dark:text-orange-400 border border-orange-500/20">High (Biohazard)</span>';
                } else if (r.hazard_level === 'Moderate') {
                    hazardBadge = '<span class="text-[11px] px-2 py-0.5 rounded-full font-semibold bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/20">Moderate</span>';
                } else {
                    hazardBadge = '<span class="text-[11px] px-2 py-0.5 rounded-full font-semibold bg-teal-500/10 text-teal-600 dark:text-teal-400 border border-teal-500/20">Minimal</span>';
                }

                tr.innerHTML = `
                    <td class="py-2.5 px-3 font-mono font-semibold text-primary-heading text-xs">${r.class_name}</td>
                    <td class="py-2.5 px-3 text-secondary-label font-medium text-xs">${r.display_name}</td>
                    <td class="py-2.5 px-3">${binBadge}</td>
                    <td class="py-2.5 px-3">${hazardBadge}</td>
                    <td class="py-2.5 px-3 text-muted-desc max-w-xs text-xs">${r.treatment}</td>
                `;
                el.classesTableBody.appendChild(tr);
            });
        }
    } catch (err) {
        console.warn('Failed to load classes directory:', err);
    }
}

// Initialize UI Event Listeners
function initEventListeners() {
    // Slider values
    el.confSlider.addEventListener('input', (e) => {
        const val = e.target.value;
        el.confVal.textContent = `${val}% (${(val / 100).toFixed(2)})`;
    });

    el.iouSlider.addEventListener('input', (e) => {
        const val = e.target.value;
        el.iouVal.textContent = `${val}% (${(val / 100).toFixed(2)})`;
    });

    // File input changes
    el.fileInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files[0]) {
            handleSelectedFile(e.target.files[0]);
        }
    });

    // Drag and Drop
    ['dragenter', 'dragover'].forEach(name => {
        el.dropZone.addEventListener(name, (e) => {
            e.preventDefault();
            e.stopPropagation();
            el.dropZone.classList.add('drag-over');
        });
    });

    ['dragleave', 'drop'].forEach(name => {
        el.dropZone.addEventListener(name, (e) => {
            e.preventDefault();
            e.stopPropagation();
            el.dropZone.classList.remove('drag-over');
        });
    });

    el.dropZone.addEventListener('drop', (e) => {
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleSelectedFile(e.dataTransfer.files[0]);
        }
    });

    // Clear image
    el.clearImageBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        resetInput();
    });

    // Reset button
    el.resetAllBtn.addEventListener('click', () => {
        resetInput();
        el.resultsContainer.classList.add('hidden');
        el.resultsPlaceholder.classList.remove('hidden');
    });

    // Analyze button
    el.analyzeBtn.addEventListener('click', runAnalysis);

    // Toggle view buttons
    el.toggleAnnotatedBtn.addEventListener('click', () => {
        el.resImageAnnotated.classList.remove('hidden');
        el.resImageOriginal.classList.add('hidden');
        el.toggleAnnotatedBtn.style.backgroundColor = 'var(--accent-surface)';
        el.toggleAnnotatedBtn.style.color = 'var(--accent-text)';
        el.toggleAnnotatedBtn.className = 'px-2.5 py-1 rounded-md font-semibold text-[11px] transition';
        el.toggleOriginalBtn.style.backgroundColor = 'transparent';
        el.toggleOriginalBtn.style.color = 'var(--text-secondary)';
        el.toggleOriginalBtn.className = 'px-2.5 py-1 rounded-md font-medium text-[11px] text-secondary-label transition';
    });

    el.toggleOriginalBtn.addEventListener('click', () => {
        el.resImageAnnotated.classList.add('hidden');
        el.resImageOriginal.classList.remove('hidden');
        el.toggleOriginalBtn.style.backgroundColor = 'var(--accent-surface)';
        el.toggleOriginalBtn.style.color = 'var(--accent-text)';
        el.toggleOriginalBtn.className = 'px-2.5 py-1 rounded-md font-semibold text-[11px] transition';
        el.toggleAnnotatedBtn.style.backgroundColor = 'transparent';
        el.toggleAnnotatedBtn.style.color = 'var(--text-secondary)';
        el.toggleAnnotatedBtn.className = 'px-2.5 py-1 rounded-md font-medium text-[11px] text-secondary-label transition';
    });

    // Webcam Modal Handlers
    el.openWebcamBtn.addEventListener('click', startWebcam);
    el.closeWebcamBtn.addEventListener('click', stopWebcam);
    el.cancelWebcamBtn.addEventListener('click', stopWebcam);
    el.snapWebcamBtn.addEventListener('click', snapWebcam);
}

// Handle selected file from browse or drop
function handleSelectedFile(file) {
    if (!file.type.startsWith('image/')) {
        alert('Please select a valid image file (JPG, PNG, WEBP, BMP).');
        return;
    }

    state.selectedFile = file;
    state.selectedSample = null;
    state.webcamBase64 = null;

    const reader = new FileReader();
    reader.onload = (e) => {
        el.previewImg.src = e.target.result;
        el.previewFilename.textContent = file.name;
        el.dropzonePrompt.classList.add('hidden');
        el.dropzonePreview.classList.remove('hidden');

        el.analyzeBtn.disabled = false;
        el.analyzeBtnText.textContent = `Analyze ${file.name}`;
    };
    reader.readAsDataURL(file);
}

// Reset image input
function resetInput() {
    state.selectedFile = null;
    state.selectedSample = null;
    state.webcamBase64 = null;
    el.fileInput.value = '';
    el.previewImg.src = '';
    el.dropzonePreview.classList.add('hidden');
    el.dropzonePrompt.classList.remove('hidden');
    el.analyzeBtn.disabled = true;
    el.analyzeBtnText.textContent = 'Classify & Segregate Waste';
}

// Webcam Controls
async function startWebcam() {
    try {
        state.webcamStream = await navigator.mediaDevices.getUserMedia({
            video: { facingMode: 'environment', width: { ideal: 1280 }, height: { ideal: 720 } },
            audio: false
        });
        el.webcamVideo.srcObject = state.webcamStream;
        el.webcamModal.classList.remove('hidden');
    } catch (err) {
        alert('Unable to access webcam. Please check camera permissions in your browser: ' + err.message);
    }
}

function stopWebcam() {
    if (state.webcamStream) {
        state.webcamStream.getTracks().forEach(track => track.stop());
        state.webcamStream = null;
    }
    el.webcamModal.classList.add('hidden');
}

function snapWebcam() {
    const video = el.webcamVideo;
    const canvas = el.webcamCanvas;
    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    const b64 = canvas.toDataURL('image/jpeg', 0.9);
    state.webcamBase64 = b64;
    state.selectedFile = null;
    state.selectedSample = null;

    stopWebcam();

    // Show preview
    el.previewImg.src = b64;
    el.previewFilename.textContent = 'Live Webcam Capture';
    el.dropzonePrompt.classList.add('hidden');
    el.dropzonePreview.classList.remove('hidden');

    el.analyzeBtn.disabled = false;
    el.analyzeBtnText.textContent = 'Analyze Webcam Frame';
}

// Run Analysis: Calls /api/predict
async function runAnalysis() {
    if (state.isProcessing) return;

    const conf = parseFloat(el.confSlider.value) / 100;
    const iou = parseFloat(el.iouSlider.value) / 100;

    setLoadingState(true);

    try {
        let response;

        if (state.selectedFile) {
            const formData = new FormData();
            formData.append('file', state.selectedFile);
            formData.append('conf', conf.toString());
            formData.append('iou', iou.toString());

            response = await fetch('/api/predict', {
                method: 'POST',
                body: formData
            });
        } else if (state.selectedSample) {
            response = await fetch('/api/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    sample_filename: state.selectedSample,
                    conf: conf,
                    iou: iou
                })
            });
        } else if (state.webcamBase64) {
            response = await fetch('/api/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    image_base64: state.webcamBase64,
                    conf: conf,
                    iou: iou
                })
            });
        } else {
            alert('Please select or upload an image first.');
            setLoadingState(false);
            return;
        }

        const data = await response.json();

        if (!response.ok || !data.success) {
            const errorMsg = data.error || 'Prediction request failed.';
            showErrorAlert(errorMsg);
            setLoadingState(false);
            return;
        }

        // Render Results
        renderResults(data);

    } catch (err) {
        showErrorAlert('Network or server error: ' + err.message);
    } finally {
        setLoadingState(false);
    }
}

function setLoadingState(loading) {
    state.isProcessing = loading;
    el.analyzeBtn.disabled = loading;
    if (loading) {
        el.analyzeBtnText.textContent = 'Analyzing Waste with MEDIGRATOR...';
        el.analyzeSpinner.classList.remove('hidden');
    } else {
        el.analyzeBtnText.textContent = 'Classify & Segregate Waste';
        el.analyzeSpinner.classList.add('hidden');
    }
}

function showErrorAlert(message) {
    el.envBanner.classList.remove('hidden');
    el.envMessage.textContent = message;
    alert(`MEDIGRATOR Detection Alert:\n\n${message}`);
}

// Render Results on the Dashboard
function renderResults(data) {
    state.lastPredictionResult = data;

    // Reveal results panel
    el.resultsPlaceholder.classList.add('hidden');
    el.resultsContainer.classList.remove('hidden');

    // Display Annotated & Original Images
    if (data.annotated_image_b64) {
        el.resImageAnnotated.src = data.annotated_image_b64;
    }
    if (data.original_image_b64) {
        el.resImageOriginal.src = data.original_image_b64;
    }

    // Default to annotated view
    el.resImageAnnotated.classList.remove('hidden');
    el.resImageOriginal.classList.add('hidden');
    el.toggleAnnotatedBtn.style.backgroundColor = 'var(--accent-surface)';
    el.toggleAnnotatedBtn.style.color = 'var(--accent-text)';
    el.toggleOriginalBtn.style.backgroundColor = 'transparent';
    el.toggleOriginalBtn.style.color = 'var(--text-secondary)';

    // Summary KPIs
    const summary = data.summary || {};
    el.statTotalItems.textContent = summary.total_items || '0';
    el.statPrimaryStream.textContent = summary.primary_stream || 'No Objects';
    el.statLatency.textContent = `${data.latency_ms}ms`;

    // Max Confidence
    if (data.detections && data.detections.length > 0) {
        const topConf = Math.max(...data.detections.map(d => d.confidence_percent));
        el.statMaxConf.textContent = `${topConf}%`;
    } else {
        el.statMaxConf.textContent = '0%';
    }

    // Hazard Badge
    el.statHazardBadge.textContent = summary.highest_hazard || 'None';
    el.statHazardBadge.className = `text-[11px] px-2 py-0.5 rounded font-semibold border ${summary.highest_hazard_color || 'bg-slate-700 text-slate-300'}`;

    // Render Detections List
    renderDetectionsList(data.detections || []);

    // Render Segregation Action Bins
    renderRequiredBins(summary.bin_counts || {}, data.detections || []);

    // Render Checklist
    renderChecklist(summary.action_checklist || []);

    if (window.lucide) {
        lucide.createIcons();
    }
}

// Render Detected Items Cards
function renderDetectionsList(detections) {
    el.detectionsList.innerHTML = '';

    if (detections.length === 0) {
        el.detectionsList.innerHTML = `
            <div class="inner-box p-3.5 rounded-lg text-center text-xs text-muted-desc">
                No medical waste objects detected above the confidence threshold.
                Try adjusting the confidence slider to a lower percentage.
            </div>
        `;
        return;
    }

    detections.forEach(det => {
        const item = document.createElement('div');
        item.className = 'detection-item-row p-3 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2.5';

        let binPill = '';
        if (det.bin_color === 'Yellow') {
            binPill = '<span class="text-[11px] px-2 py-0.5 rounded-full font-semibold bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/20">🟡 Yellow</span>';
        } else if (det.bin_color === 'Red') {
            binPill = '<span class="text-[11px] px-2 py-0.5 rounded-full font-semibold bg-red-500/10 text-red-600 dark:text-red-400 border border-red-500/20">🔴 Red</span>';
        } else if (det.bin_color === 'White') {
            binPill = '<span class="text-[11px] px-2 py-0.5 rounded-full font-semibold bg-slate-500/10 text-slate-700 dark:text-slate-300 border border-slate-500/20">⚪ White Box</span>';
        } else if (det.bin_color === 'Blue') {
            binPill = '<span class="text-[11px] px-2 py-0.5 rounded-full font-semibold bg-blue-500/10 text-blue-600 dark:text-blue-400 border border-blue-500/20">🔵 Blue</span>';
        } else {
            binPill = '<span class="text-[11px] px-2 py-0.5 rounded-full font-semibold bg-slate-500/10 text-slate-700 dark:text-slate-300 border border-slate-500/20">⚫ Black</span>';
        }

        item.innerHTML = `
            <div class="flex items-center space-x-2.5">
                <span class="w-6 h-6 rounded-md inner-box text-muted-desc text-[11px] font-mono font-semibold flex items-center justify-center">#${det.id}</span>
                <div>
                    <div class="flex items-center space-x-1.5">
                        <span class="text-xs font-semibold text-primary-heading">${det.display_name}</span>
                        <span class="font-mono text-[10px] text-muted-desc">(${det.class_name})</span>
                    </div>
                    <p class="text-[11px] text-muted-desc mt-0.5">${det.treatment}</p>
                </div>
            </div>

            <div class="flex items-center space-x-3 sm:self-center">
                <div class="w-20 text-right">
                    <span class="text-xs font-mono font-semibold" style="color: var(--accent);">${det.confidence_percent}%</span>
                    <div class="w-full inner-box rounded-full h-1 mt-0.5 overflow-hidden">
                        <div class="h-1 rounded-full" style="width: ${det.confidence_percent}%; background-color: var(--accent);"></div>
                    </div>
                </div>
                ${binPill}
            </div>
        `;
        el.detectionsList.appendChild(item);
    });
}

// Render Required Bin Container Cards
function renderRequiredBins(binCounts, detections) {
    el.requiredBinsCards.innerHTML = '';
    const activeBins = Object.keys(binCounts);

    if (activeBins.length === 0) {
        el.requiredBinsCards.innerHTML = `
            <div class="col-span-2 text-center py-3 text-xs text-muted-desc">
                No active disposal streams triggered.
            </div>
        `;
        return;
    }

    const binDetails = {
        'Yellow': {
            title: 'Yellow Biohazard Bag',
            subtitle: 'Soiled & Infectious Waste',
            borderColor: '#f59e0b',
            pill: 'bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/20',
            desc: 'Autoclave or high-temperature incineration (>1050°C).'
        },
        'Red': {
            title: 'Red Non-Chlorinated Bag',
            subtitle: 'Contaminated Recyclable Plastics',
            borderColor: '#ef4444',
            pill: 'bg-red-500/10 text-red-600 dark:text-red-400 border border-red-500/20',
            desc: 'Autoclave / microwaving before shredding & authorized plastic recycling.'
        },
        'White': {
            title: 'White Translucent Container',
            subtitle: 'Waste Sharps & Needles',
            borderColor: '#94a3b8',
            pill: 'bg-slate-500/10 text-slate-700 dark:text-slate-300 border border-slate-500/20',
            desc: 'Puncture-proof container. Autoclave and sharp-pit encapsulation.'
        },
        'Blue': {
            title: 'Blue Rigid Cardboard Box',
            subtitle: 'Glassware & Medicine Vials',
            borderColor: '#3b82f6',
            pill: 'bg-blue-500/10 text-blue-600 dark:text-blue-400 border border-blue-500/20',
            desc: 'Disinfect with 1-2% Sodium Hypochlorite and glass recycling.'
        },
        'Black': {
            title: 'Black / Green Municipal Bin',
            subtitle: 'General Non-Hazardous Waste',
            borderColor: '#64748b',
            pill: 'bg-slate-500/10 text-slate-700 dark:text-slate-300 border border-slate-500/20',
            desc: 'General municipal solid waste collection.'
        }
    };

    activeBins.forEach(b => {
        const info = binDetails[b] || {
            title: `${b} Disposal Bin`,
            subtitle: 'Standard Healthcare Segregation',
            borderColor: '#64748b',
            pill: 'bg-slate-500/10 text-slate-400 border border-slate-500/20',
            desc: 'Authorized clinical disposal protocol.'
        };

        const count = binCounts[b] || 1;
        const card = document.createElement('div');
        card.className = `bin-rule-card p-3.5 space-y-1.5`;
        card.style.borderLeftColor = info.borderColor;
        card.innerHTML = `
            <div class="flex items-center justify-between">
                <span class="text-[11px] font-semibold px-2 py-0.5 rounded-full ${info.pill}">
                    ${info.title}
                </span>
                <span class="text-[11px] font-mono font-medium text-muted-desc">${count} item(s)</span>
            </div>
            <h4 class="text-xs font-semibold text-primary-heading">${info.subtitle}</h4>
            <p class="text-[11px] text-muted-desc leading-relaxed">${info.desc}</p>
        `;
        el.requiredBinsCards.appendChild(card);
    });
}

// Render Action Checklist
function renderChecklist(checklist) {
    el.actionChecklist.innerHTML = '';
    checklist.forEach(itemText => {
        const li = document.createElement('li');
        li.className = 'flex items-start space-x-2 text-secondary-label';
        li.innerHTML = `
            <i data-lucide="check" class="w-3.5 h-3.5 flex-shrink-0 mt-0.5" style="color: var(--accent);"></i>
            <span>${itemText}</span>
        `;
        el.actionChecklist.appendChild(li);
    });
}
