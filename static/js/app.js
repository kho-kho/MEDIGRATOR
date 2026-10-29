/**
 * MEDIGRATOR: AI-Driven Medical Waste Detection & Intelligent Segregation
 * Frontend Application Engine & Clinical Dashboard Controller
 */

// Application State
const state = {
    inputMode: 'image', // 'image' or 'video'
    selectedFile: null,
    selectedVideoFile: null,
    selectedSample: null,
    webcamBase64: null,
    webcamStream: null,
    isProcessing: false,
    activeTab: 'studio',
    lastPredictionResult: null,
    transparencyData: null,
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

    // Environment Banner & Hardware Badge
    envBanner: document.getElementById('env-alert-banner'),
    envMessage: document.getElementById('env-alert-message'),
    systemStatusText: document.getElementById('system-status-text'),
    systemStatusDot: document.getElementById('system-status-dot'),
    systemStatusBadge: document.getElementById('system-status-badge'),
    footerDeviceLabel: document.getElementById('footer-device-label'),

    // Input Mode Tabs
    modeImageBtn: document.getElementById('mode-image-btn'),
    modeVideoBtn: document.getElementById('mode-video-btn'),
    inputLimitsLabel: document.getElementById('input-limits-label'),

    // Image Dropzone
    dropZone: document.getElementById('drop-zone'),
    fileInput: document.getElementById('file-input'),
    dropzonePrompt: document.getElementById('dropzone-prompt'),
    dropzonePreview: document.getElementById('dropzone-preview'),
    previewImg: document.getElementById('preview-img'),
    previewFilename: document.getElementById('preview-filename'),
    clearImageBtn: document.getElementById('clear-image-btn'),

    // Video Dropzone
    videoDropZone: document.getElementById('video-drop-zone'),
    videoFileInput: document.getElementById('video-file-input'),
    videoDropzonePrompt: document.getElementById('video-dropzone-prompt'),
    videoDropzonePreview: document.getElementById('video-dropzone-preview'),
    videoPreviewFilename: document.getElementById('video-preview-filename'),
    videoPreviewSize: document.getElementById('video-preview-size'),
    clearVideoBtn: document.getElementById('clear-video-btn'),

    // Samples
    samplesSection: document.getElementById('samples-section'),
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

    // Compact Transparency Card Elements
    transModelName: document.getElementById('trans-model-name'),
    transDeviceName: document.getElementById('trans-device-name'),
    transDatasetVer: document.getElementById('trans-dataset-ver'),
    transClassesCount: document.getElementById('trans-classes-count'),
    compactModelStatusPill: document.getElementById('compact-model-status-pill'),

    // Specs Tab Elements
    specWeightsFile: document.getElementById('spec-weights-file'),
    specWeightsSize: document.getElementById('spec-weights-size'),
    specDeviceInfo: document.getElementById('spec-device-info'),
    specFrameworkInfo: document.getElementById('spec-framework-info'),

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
    resultsLoading: document.getElementById('results-loading'),
    loadingStatusText: document.getElementById('loading-status-text'),
    resultsContainer: document.getElementById('results-container'),
    viewModeButtons: document.getElementById('view-mode-buttons'),
    toggleAnnotatedBtn: document.getElementById('toggle-annotated-btn'),
    toggleOriginalBtn: document.getElementById('toggle-original-btn'),
    resImageAnnotated: document.getElementById('res-image-annotated'),
    resImageOriginal: document.getElementById('res-image-original'),

    // Video Keyframes
    videoKeyframesSection: document.getElementById('video-keyframes-section'),
    videoKeyframesCarousel: document.getElementById('video-keyframes-carousel'),
    videoTrackingStats: document.getElementById('video-tracking-stats'),

    // KPI Stats
    statTotalItems: document.getElementById('stat-total-items'),
    statClassesCount: document.getElementById('stat-classes-count'),
    statVerifiedCount: document.getElementById('stat-verified-count'),
    statPendingCount: document.getElementById('stat-pending-count'),
    statLatency: document.getElementById('stat-latency'),
    statHazardBadge: document.getElementById('stat-hazard-badge'),

    // Verification Alert Box
    verificationAlertBox: document.getElementById('verification-alert-box'),
    verificationAlertDesc: document.getElementById('verification-alert-desc'),
    verificationItemsList: document.getElementById('verification-items-list'),

    // Segregation Guidance Table
    detectionsTableBody: document.getElementById('detections-table-body'),

    // Lists & Advisory
    requiredBinsCards: document.getElementById('required-bins-cards'),
    actionChecklist: document.getElementById('action-checklist'),
    classesTableBody: document.getElementById('classes-table-body')
};

// Initialize Application
document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initEventListeners();
    fetchSystemTransparency();
    fetchSampleImages();
    fetchClassesDirectory();
});

// Theme Management Logic
function initThemeToggle() {
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
    setTheme(isCurrentlyDark ? 'light' : 'dark');
}

function setTheme(theme) {
    state.theme = theme;
    const isDark = (theme === 'dark');

    if (isDark) {
        document.documentElement.classList.add('dark');
        if (el.themeLabel) el.themeLabel.textContent = 'Dark Mode';
        if (el.themeToggleBtn) el.themeToggleBtn.setAttribute('aria-checked', 'true');
        if (el.themeIcon) {
            el.themeIcon.setAttribute('data-lucide', 'moon');
            el.themeIcon.className = 'w-2.5 h-2.5 text-slate-800';
        }
    } else {
        document.documentElement.classList.remove('dark');
        if (el.themeLabel) el.themeLabel.textContent = 'Light Mode';
        if (el.themeToggleBtn) el.themeToggleBtn.setAttribute('aria-checked', 'false');
        if (el.themeIcon) {
            el.themeIcon.setAttribute('data-lucide', 'sun');
            el.themeIcon.className = 'w-2.5 h-2.5 text-amber-500';
        }
    }

    if (window.lucide) {
        lucide.createIcons();
    }
}

// Navigation Tabs
function switchTab(tabId) {
    state.activeTab = tabId;

    el.tabStudio.classList.add('hidden');
    el.tabGuidelines.classList.add('hidden');
    el.tabSpecs.classList.add('hidden');

    el.tabBtnStudio.classList.remove('active');
    el.tabBtnGuidelines.classList.remove('active');
    el.tabBtnSpecs.classList.remove('active');

    if (tabId === 'studio') {
        el.tabStudio.classList.remove('hidden');
        el.tabBtnStudio.classList.add('active');
    } else if (tabId === 'guidelines') {
        el.tabGuidelines.classList.remove('hidden');
        el.tabBtnGuidelines.classList.add('active');
    } else if (tabId === 'specs') {
        el.tabSpecs.classList.remove('hidden');
        el.tabBtnSpecs.classList.add('active');
    }

    if (window.lucide) {
        lucide.createIcons();
    }
}

// Fetch Authentic System Transparency Information
async function fetchSystemTransparency() {
    try {
        const res = await fetch('/api/model-info');
        if (!res.ok) throw new Error('Status code ' + res.status);
        const data = await res.json();
        state.transparencyData = data;

        const hw = data.hardware || {};
        const model = data.model || {};
        const dataset = data.dataset || {};

        // Update Navbar Status
        if (el.systemStatusText) {
            const devText = hw.cuda_available ? `GPU: ${hw.gpu_name || 'CUDA'}` : `CPU: ${hw.processor || 'x86_64'}`;
            el.systemStatusText.textContent = `MEDIGRATOR Active (${devText})`;
        }
        if (el.systemStatusDot) {
            el.systemStatusDot.className = hw.cuda_available ? 'w-2 h-2 rounded-full bg-emerald-400' : 'w-2 h-2 rounded-full bg-teal-400';
        }
        if (el.footerDeviceLabel) {
            el.footerDeviceLabel.textContent = `${model.name || 'YOLO11'} • ${hw.device || 'CPU'}`;
        }

        // Update Compact Transparency Card
        if (el.transModelName) el.transModelName.textContent = model.name || 'YOLO11n PyTorch';
        if (el.transDeviceName) el.transDeviceName.textContent = hw.cuda_available ? (hw.gpu_name || 'CUDA GPU') : 'CPU (Host Processor)';
        if (el.transDatasetVer) el.transDatasetVer.textContent = `${dataset.name || 'Biomedical'} ${dataset.version || 'v3'}`;
        if (el.transClassesCount) el.transClassesCount.textContent = `${dataset.total_classes || 14} Classes`;
        if (el.compactModelStatusPill) {
            el.compactModelStatusPill.textContent = model.weights_found ? 'Model Ready' : 'Weights Missing';
            el.compactModelStatusPill.style.color = model.weights_found ? 'var(--accent-text)' : '#ef4444';
        }

        // Update Specs Tab
        if (el.specWeightsFile) el.specWeightsFile.textContent = model.weights_file || 'models/best.pt';
        if (el.specWeightsSize) el.specWeightsSize.textContent = `${model.weights_size_mb || 5.22} MB`;
        if (el.specDeviceInfo) el.specDeviceInfo.textContent = hw.device || 'CPU';
        if (el.specFrameworkInfo) el.specFrameworkInfo.textContent = `PyTorch v${hw.torch_version || '2.x'} (${model.version || 'Ultralytics'})`;

    } catch (err) {
        console.warn('Could not retrieve system transparency info:', err);
        if (el.systemStatusText) el.systemStatusText.textContent = 'MEDIGRATOR System Ready';
    }
}

// Fetch Sample Images
async function fetchSampleImages() {
    try {
        const res = await fetch('/api/samples');
        const data = await res.json();

        if (data.success && data.samples.length > 0) {
            el.samplesContainer.innerHTML = '';
            data.samples.forEach(sample => {
                const card = document.createElement('div');
                card.className = 'sample-thumb-card p-1.5 flex flex-col items-center text-center space-y-1';
                card.dataset.filename = sample.filename;
                card.innerHTML = `
                    <div class="w-full h-14 rounded overflow-hidden bg-black/30 flex items-center justify-center">
                        <img src="${sample.url}" alt="${sample.title}" class="w-full h-full object-cover">
                    </div>
                    <span class="text-[10px] font-semibold text-secondary-label truncate w-full block">${sample.title}</span>
                `;
                card.addEventListener('click', () => selectSample(sample.filename, sample.url, sample.title, card));
                el.samplesContainer.appendChild(card);
            });
        } else {
            el.samplesContainer.innerHTML = '<div class="col-span-3 text-center py-2 text-xs text-muted-desc">No sample images found.</div>';
        }
    } catch (err) {
        console.warn('Sample fetch error:', err);
    }
}

// Select Quick Test Sample
function selectSample(filename, url, title, cardEl) {
    // Switch to image mode if not already
    setInputMode('image');

    state.selectedSample = filename;
    state.selectedFile = null;
    state.selectedVideoFile = null;
    state.webcamBase64 = null;

    // Highlight card
    document.querySelectorAll('.sample-thumb-card').forEach(c => c.classList.remove('active-sample'));
    if (cardEl) cardEl.classList.add('active-sample');

    el.previewImg.src = url;
    el.previewFilename.textContent = `Sample: ${title}`;
    el.dropzonePrompt.classList.add('hidden');
    el.dropzonePreview.classList.remove('hidden');

    el.analyzeBtn.disabled = false;
    el.analyzeBtnText.textContent = `Classify Sample: ${title}`;
}

// Fetch Full Classes Segregation Directory for Tab 2
async function fetchClassesDirectory() {
    try {
        const res = await fetch('/api/classes');
        const data = await res.json();
        if (!data.success) return;

        const rules = data.rules || {};
        el.classesTableBody.innerHTML = '';

        Object.keys(rules).forEach(cname => {
            const r = rules[cname];
            const row = document.createElement('tr');
            row.className = 'border-divider';

            let binBadge = '';
            if (r.bin_color === 'Yellow') {
                binBadge = '<span class="px-2 py-0.5 rounded-full font-semibold bg-amber-500/10 text-amber-500 border border-amber-500/20">🟡 Yellow Bin</span>';
            } else if (r.bin_color === 'Red') {
                binBadge = '<span class="px-2 py-0.5 rounded-full font-semibold bg-red-500/10 text-red-500 border border-red-500/20">🔴 Red Bin</span>';
            } else if (r.bin_color === 'White') {
                binBadge = '<span class="px-2 py-0.5 rounded-full font-semibold bg-slate-500/10 text-slate-300 border border-slate-500/20">⚪ White Sharps Box</span>';
            } else if (r.bin_color === 'Blue') {
                binBadge = '<span class="px-2 py-0.5 rounded-full font-semibold bg-blue-500/10 text-blue-400 border border-blue-500/20">🔵 Blue Box</span>';
            } else {
                binBadge = '<span class="px-2 py-0.5 rounded-full font-semibold bg-slate-500/10 text-slate-300 border border-slate-500/20">⚫ Black/Green Bin</span>';
            }

            row.innerHTML = `
                <td class="font-mono font-semibold text-primary-heading">${r.class_name}</td>
                <td class="font-medium text-secondary-label">${r.display_name}</td>
                <td class="text-xs text-muted-desc">${r.official_category || 'CPCB Schedule I'}</td>
                <td>${binBadge}</td>
                <td><span class="px-1.5 py-0.5 rounded text-[10px] font-semibold border ${r.hazard_color || ''}">${r.hazard_level}</span></td>
                <td class="text-xs text-secondary-label">${r.treatment}</td>
            `;
            el.classesTableBody.appendChild(row);
        });
    } catch (err) {
        console.warn('Classes fetch error:', err);
    }
}

// Set Input Mode (Image vs Video)
function setInputMode(mode) {
    state.inputMode = mode;
    resetInput();

    if (mode === 'image') {
        el.modeImageBtn.classList.add('active');
        el.modeVideoBtn.classList.remove('active');
        el.dropZone.classList.remove('hidden');
        el.videoDropZone.classList.add('hidden');
        el.samplesSection.classList.remove('hidden');
        el.inputLimitsLabel.textContent = 'Max 32MB';
        el.analyzeBtnText.textContent = 'Classify & Segregate Waste';
    } else {
        el.modeVideoBtn.classList.add('active');
        el.modeImageBtn.classList.remove('active');
        el.videoDropZone.classList.remove('hidden');
        el.dropZone.classList.add('hidden');
        el.samplesSection.classList.add('hidden');
        el.inputLimitsLabel.textContent = 'Max 64MB Video';
        el.analyzeBtnText.textContent = 'Analyze Video Stream (Object Tracking)';
    }

    if (window.lucide) {
        lucide.createIcons();
    }
}

// Initialize Event Listeners
function initEventListeners() {
    // Mode Switcher
    el.modeImageBtn.addEventListener('click', () => setInputMode('image'));
    el.modeVideoBtn.addEventListener('click', () => setInputMode('video'));

    // Image Input File Change
    el.fileInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files[0]) {
            handleSelectedImage(e.target.files[0]);
        }
    });

    // Video Input File Change
    el.videoFileInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files[0]) {
            handleSelectedVideo(e.target.files[0]);
        }
    });

    // Drag and Drop: Image
    el.dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        el.dropZone.classList.add('drag-over');
    });
    el.dropZone.addEventListener('dragleave', () => {
        el.dropZone.classList.remove('drag-over');
    });
    el.dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        el.dropZone.classList.remove('drag-over');
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleSelectedImage(e.dataTransfer.files[0]);
        }
    });

    // Drag and Drop: Video
    el.videoDropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        el.videoDropZone.classList.add('drag-over');
    });
    el.videoDropZone.addEventListener('dragleave', () => {
        el.videoDropZone.classList.remove('drag-over');
    });
    el.videoDropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        el.videoDropZone.classList.remove('drag-over');
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleSelectedVideo(e.dataTransfer.files[0]);
        }
    });

    // Sliders
    el.confSlider.addEventListener('input', (e) => {
        const val = e.target.value;
        const dec = (val / 100).toFixed(2);
        el.confVal.textContent = `${val}% (${dec})`;
    });

    el.iouSlider.addEventListener('input', (e) => {
        const val = e.target.value;
        const dec = (val / 100).toFixed(2);
        el.iouVal.textContent = `${val}% (${dec})`;
    });

    // Clear Buttons
    el.clearImageBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        resetInput();
    });
    el.clearVideoBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        resetInput();
    });

    // Reset All
    el.resetAllBtn.addEventListener('click', () => {
        resetInput();
        el.resultsContainer.classList.add('hidden');
        el.resultsLoading.classList.add('hidden');
        el.resultsPlaceholder.classList.remove('hidden');
    });

    // Analyze Button
    el.analyzeBtn.addEventListener('click', runAnalysis);

    // Toggle Visual Views
    el.toggleAnnotatedBtn.addEventListener('click', () => {
        el.resImageAnnotated.classList.remove('hidden');
        el.resImageOriginal.classList.add('hidden');
        el.toggleAnnotatedBtn.style.backgroundColor = 'var(--accent-surface)';
        el.toggleAnnotatedBtn.style.color = 'var(--accent-text)';
        el.toggleOriginalBtn.style.backgroundColor = 'transparent';
        el.toggleOriginalBtn.style.color = 'var(--text-secondary)';
    });

    el.toggleOriginalBtn.addEventListener('click', () => {
        el.resImageAnnotated.classList.add('hidden');
        el.resImageOriginal.classList.remove('hidden');
        el.toggleOriginalBtn.style.backgroundColor = 'var(--accent-surface)';
        el.toggleOriginalBtn.style.color = 'var(--accent-text)';
        el.toggleAnnotatedBtn.style.backgroundColor = 'transparent';
        el.toggleAnnotatedBtn.style.color = 'var(--text-secondary)';
    });

    // Webcam Modal Handlers
    el.openWebcamBtn.addEventListener('click', startWebcam);
    el.closeWebcamBtn.addEventListener('click', stopWebcam);
    el.cancelWebcamBtn.addEventListener('click', stopWebcam);
    el.snapWebcamBtn.addEventListener('click', snapWebcam);
}

// Handle Selected Image
function handleSelectedImage(file) {
    if (!file.type.startsWith('image/')) {
        showErrorAlert('Please select a valid image file (JPG, PNG, WEBP, BMP).');
        return;
    }

    state.selectedFile = file;
    state.selectedSample = null;
    state.selectedVideoFile = null;
    state.webcamBase64 = null;

    document.querySelectorAll('.sample-thumb-card').forEach(c => c.classList.remove('active-sample'));

    const reader = new FileReader();
    reader.onload = (e) => {
        el.previewImg.src = e.target.result;
        el.previewFilename.textContent = file.name;
        el.dropzonePrompt.classList.add('hidden');
        el.dropzonePreview.classList.remove('hidden');

        el.analyzeBtn.disabled = false;
        el.analyzeBtnText.textContent = `Classify ${file.name}`;
    };
    reader.readAsDataURL(file);
}

// Handle Selected Video
function handleSelectedVideo(file) {
    const validExtensions = ['mp4', 'webm', 'avi', 'mov', 'mkv'];
    const ext = file.name.split('.').pop().toLowerCase();

    if (!validExtensions.includes(ext) && !file.type.startsWith('video/')) {
        showErrorAlert(`Unsupported video format. Please upload an MP4, WEBM, AVI, or MOV file.`);
        return;
    }

    state.selectedVideoFile = file;
    state.selectedFile = null;
    state.selectedSample = null;
    state.webcamBase64 = null;

    const sizeMb = (file.size / (1024 * 1024)).toFixed(1);
    el.videoPreviewFilename.textContent = file.name;
    el.videoPreviewSize.textContent = `Size: ${sizeMb} MB • Ready for Multi-Object Tracking`;
    el.videoDropzonePrompt.classList.add('hidden');
    el.videoDropzonePreview.classList.remove('hidden');

    el.analyzeBtn.disabled = false;
    el.analyzeBtnText.textContent = `Analyze Video Stream (${file.name})`;
}

// Reset Input
function resetInput() {
    state.selectedFile = null;
    state.selectedVideoFile = null;
    state.selectedSample = null;
    state.webcamBase64 = null;

    el.fileInput.value = '';
    el.videoFileInput.value = '';
    el.previewImg.src = '';

    el.dropzonePreview.classList.add('hidden');
    el.dropzonePrompt.classList.remove('hidden');
    el.videoDropzonePreview.classList.add('hidden');
    el.videoDropzonePrompt.classList.remove('hidden');

    document.querySelectorAll('.sample-thumb-card').forEach(c => c.classList.remove('active-sample'));

    el.analyzeBtn.disabled = true;
    el.analyzeBtnText.textContent = state.inputMode === 'video' ? 'Analyze Video Stream' : 'Classify & Segregate Waste';
}

// Live Webcam Controls (With graceful failure handling)
async function startWebcam() {
    try {
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            throw new Error('Webcam media capture is not supported by your current browser.');
        }

        state.webcamStream = await navigator.mediaDevices.getUserMedia({
            video: { facingMode: 'environment', width: { ideal: 1280 }, height: { ideal: 720 } },
            audio: false
        });
        el.webcamVideo.srcObject = state.webcamStream;
        el.webcamModal.classList.remove('hidden');
    } catch (err) {
        showErrorAlert(
            `Webcam access failed: ${err.message}.\n\n` +
            `Ensure camera permissions are enabled in your browser settings. You can continue using image or video upload normally.`
        );
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
    state.selectedVideoFile = null;
    state.selectedSample = null;

    stopWebcam();
    setInputMode('image');

    // Show preview
    el.previewImg.src = b64;
    el.previewFilename.textContent = 'Live Webcam Frame';
    el.dropzonePrompt.classList.add('hidden');
    el.dropzonePreview.classList.remove('hidden');

    el.analyzeBtn.disabled = false;
    el.analyzeBtnText.textContent = 'Analyze Webcam Frame';
}

// Show Error Banner
function showErrorAlert(message) {
    el.envBanner.classList.remove('hidden');
    el.envMessage.textContent = message;
    alert(`MEDIGRATOR Alert:\n\n${message}`);
}

// Loading State Controller
function setLoadingState(loading, statusText = '') {
    state.isProcessing = loading;
    el.analyzeBtn.disabled = loading;

    if (loading) {
        el.resultsPlaceholder.classList.add('hidden');
        el.resultsContainer.classList.add('hidden');
        el.resultsLoading.classList.remove('hidden');
        el.loadingStatusText.textContent = statusText || 'Executing YOLO11 computer vision inference...';
        el.analyzeSpinner.classList.remove('hidden');
        el.analyzeBtnText.textContent = 'Processing Media...';
    } else {
        el.resultsLoading.classList.add('hidden');
        el.analyzeSpinner.classList.add('hidden');
        el.analyzeBtnText.textContent = state.inputMode === 'video' ? 'Analyze Video Stream' : 'Classify & Segregate Waste';
    }
}

// Run Analysis (Dispatches to Image or Video endpoint)
async function runAnalysis() {
    if (state.isProcessing) return;

    const conf = parseFloat(el.confSlider.value) / 100;
    const iou = parseFloat(el.iouSlider.value) / 100;

    // Video Mode Dispatch
    if (state.inputMode === 'video') {
        if (!state.selectedVideoFile) {
            showErrorAlert('Please select or drop a medical video file first.');
            return;
        }

        setLoadingState(true, 'Extracting video frames, executing YOLO11 inference & tracking objects across time...');

        try {
            const formData = new FormData();
            formData.append('file', state.selectedVideoFile);
            formData.append('conf', conf.toString());
            formData.append('iou', iou.toString());
            formData.append('verification_threshold', '0.50');

            const res = await fetch('/api/predict-video', {
                method: 'POST',
                body: formData
            });

            const data = await res.json();
            if (!res.ok || !data.success) {
                showErrorAlert(data.error || 'Video inference failed.');
                setLoadingState(false);
                el.resultsPlaceholder.classList.remove('hidden');
                return;
            }

            renderResults(data);

        } catch (err) {
            showErrorAlert('Video processing error: ' + err.message);
            el.resultsPlaceholder.classList.remove('hidden');
        } finally {
            setLoadingState(false);
        }
        return;
    }

    // Image / Sample / Webcam Dispatch
    setLoadingState(true, 'Running YOLO11 object detection & regulatory categorization...');

    try {
        let response;

        if (state.selectedFile) {
            const formData = new FormData();
            formData.append('file', state.selectedFile);
            formData.append('conf', conf.toString());
            formData.append('iou', iou.toString());
            formData.append('verification_threshold', '0.50');

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
                    iou: iou,
                    verification_threshold: 0.50
                })
            });
        } else if (state.webcamBase64) {
            response = await fetch('/api/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    image_base64: state.webcamBase64,
                    conf: conf,
                    iou: iou,
                    verification_threshold: 0.50
                })
            });
        } else {
            showErrorAlert('Please select or upload an image first.');
            setLoadingState(false);
            el.resultsPlaceholder.classList.remove('hidden');
            return;
        }

        const data = await response.json();

        if (!response.ok || !data.success) {
            showErrorAlert(data.error || 'Inference failed on server.');
            setLoadingState(false);
            el.resultsPlaceholder.classList.remove('hidden');
            return;
        }

        renderResults(data);

    } catch (err) {
        showErrorAlert('Network or server error: ' + err.message);
        el.resultsPlaceholder.classList.remove('hidden');
    } finally {
        setLoadingState(false);
    }
}

// Render Results on the Dashboard (Image or Video)
function renderResults(data) {
    state.lastPredictionResult = data;

    // Reveal results panel
    el.resultsPlaceholder.classList.add('hidden');
    el.resultsLoading.classList.add('hidden');
    el.resultsContainer.classList.remove('hidden');

    const isVideo = !!data.is_video;
    const summary = data.summary || {};
    const detections = data.detections || [];

    // Visual Viewport Handling
    if (isVideo) {
        // Video mode: Show first keyframe in main view and populate carousel
        el.viewModeButtons.classList.add('hidden');
        el.videoKeyframesSection.classList.remove('hidden');

        if (data.keyframes && data.keyframes.length > 0) {
            el.resImageAnnotated.src = data.keyframes[0].annotated_b64;
            el.resImageAnnotated.classList.remove('hidden');
            el.resImageOriginal.classList.add('hidden');
            renderVideoKeyframes(data.keyframes);
        }

        const vidMeta = data.video_metadata || {};
        el.videoTrackingStats.textContent = `${vidMeta.sampled_frames_processed || 0} frames sampled • ${data.total_unique_objects || 0} unique tracked items`;

    } else {
        // Image mode
        el.viewModeButtons.classList.remove('hidden');
        el.videoKeyframesSection.classList.add('hidden');

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
    }

    // KPI Summary Metrics
    el.statTotalItems.textContent = summary.total_items ?? '0';
    el.statClassesCount.textContent = summary.unique_classes_count ?? (summary.detected_classes ? summary.detected_classes.length : '0');
    el.statVerifiedCount.textContent = summary.verified_assignments_count ?? '0';
    el.statPendingCount.textContent = summary.pending_verification_count ?? '0';
    el.statLatency.textContent = `${data.latency_ms || 0}ms`;

    // Hazard Badge
    el.statHazardBadge.textContent = `Hazard: ${summary.highest_hazard || 'None'}`;
    el.statHazardBadge.className = `text-[11px] px-2.5 py-0.5 rounded font-semibold border ${summary.highest_hazard_color || 'bg-slate-800 text-slate-300'}`;

    // Human Verification Alert Box (Requirement 3)
    if (summary.pending_verification_count > 0) {
        el.verificationAlertBox.classList.remove('hidden');
        el.verificationAlertDesc.textContent =
            `${summary.pending_verification_count} item(s) flagged for human clinical verification due to low confidence (<50%) or unverified classification. These items have NOT been automatically assigned to a disposal stream to prevent contamination or safety hazards.`;

        el.verificationItemsList.innerHTML = '';
        (summary.verification_items || []).forEach(item => {
            const row = document.createElement('div');
            row.className = 'inner-box p-2 text-xs flex items-center justify-between text-secondary-label';
            row.innerHTML = `
                <div class="flex items-center space-x-2">
                    <span class="font-mono font-semibold text-amber-400">#${item.id}</span>
                    <span class="font-semibold text-primary-heading">${item.class_name}</span>
                    <span class="text-muted-desc">(${item.confidence_percent}%)</span>
                </div>
                <span class="text-[11px] text-amber-500 font-medium">${item.reason}</span>
            `;
            el.verificationItemsList.appendChild(row);
        });
    } else {
        el.verificationAlertBox.classList.add('hidden');
    }

    // Render Clinical Segregation Guidance Table (Requirement 4)
    renderSegregationTable(detections);

    // Render Target Containers
    renderRequiredBins(summary.bin_counts || {}, detections);

    // Render Operational Checklist
    renderChecklist(summary.action_checklist || []);

    if (window.lucide) {
        lucide.createIcons();
    }
}

// Render Video Keyframes Carousel
function renderVideoKeyframes(keyframes) {
    el.videoKeyframesCarousel.innerHTML = '';
    keyframes.forEach((kf, index) => {
        const card = document.createElement('div');
        card.className = `keyframe-card p-1 text-center ${index === 0 ? 'active-keyframe' : ''}`;
        card.innerHTML = `
            <div class="w-full h-12 rounded overflow-hidden bg-black flex items-center justify-center">
                <img src="${kf.annotated_b64}" alt="Frame ${kf.frame_number}" class="w-full h-full object-cover">
            </div>
            <div class="mt-1 flex items-center justify-between text-[10px] text-muted-desc px-0.5">
                <span>${kf.timestamp_sec}s</span>
                <span class="text-teal-400 font-semibold">${kf.detections_count} obj</span>
            </div>
        `;
        card.addEventListener('click', () => {
            document.querySelectorAll('.keyframe-card').forEach(c => c.classList.remove('active-keyframe'));
            card.classList.add('active-keyframe');
            el.resImageAnnotated.src = kf.annotated_b64;
        });
        el.videoKeyframesCarousel.appendChild(card);
    });
}

// Render Clinical Segregation Table (Requirement 4)
function renderSegregationTable(detections) {
    el.detectionsTableBody.innerHTML = '';

    if (detections.length === 0) {
        el.detectionsTableBody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center py-6 text-xs text-muted-desc">
                    No medical waste objects detected above the selected confidence threshold (${el.confSlider.value}%).
                    <br>Try lowering the slider threshold to detect fainter objects or test a different sample image.
                </td>
            </tr>
        `;
        return;
    }

    detections.forEach(det => {
        const row = document.createElement('tr');
        row.className = 'border-divider';

        // Track or Detection ID
        const idLabel = det.track_id ? `Track #${det.track_id}` : `#${det.id}`;

        // Model Confidence Badge
        let confBadge = '';
        if (det.confidence_level === 'High Confidence') {
            confBadge = `<span class="inline-flex items-center space-x-1 px-2 py-0.5 rounded-full text-[10px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                <span>${det.confidence_percent}%</span>
                <span>• High</span>
            </span>`;
        } else {
            confBadge = `<span class="inline-flex items-center space-x-1 px-2 py-0.5 rounded-full text-[10px] font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/20" title="${det.verification_reason}">
                <span>${det.confidence_percent}%</span>
                <span>• ⚠️ Review</span>
            </span>`;
        }

        // Assigned Bin Pill
        let binBadge = '';
        if (det.requires_human_verification) {
            binBadge = `<span class="px-2 py-0.5 rounded-full text-[11px] font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/20">
                ⚠️ Pending Review
            </span>`;
        } else if (det.assigned_bin === 'Yellow') {
            binBadge = '<span class="px-2 py-0.5 rounded-full text-[11px] font-semibold bg-amber-500/10 text-amber-500 border border-amber-500/20">🟡 Yellow Bin</span>';
        } else if (det.assigned_bin === 'Red') {
            binBadge = '<span class="px-2 py-0.5 rounded-full text-[11px] font-semibold bg-red-500/10 text-red-500 border border-red-500/20">🔴 Red Bin</span>';
        } else if (det.assigned_bin === 'White') {
            binBadge = '<span class="px-2 py-0.5 rounded-full text-[11px] font-semibold bg-slate-500/10 text-slate-300 border border-slate-500/20">⚪ White Box</span>';
        } else if (det.assigned_bin === 'Blue') {
            binBadge = '<span class="px-2 py-0.5 rounded-full text-[11px] font-semibold bg-blue-500/10 text-blue-400 border border-blue-500/20">🔵 Blue Box</span>';
        } else {
            binBadge = '<span class="px-2 py-0.5 rounded-full text-[11px] font-semibold bg-slate-500/10 text-slate-300 border border-slate-500/20">⚫ Black Bin</span>';
        }

        // Category Text
        let categoryDisplay = '';
        if (det.mapping_status !== 'VERIFIED') {
            categoryDisplay = `<span class="text-rose-400 font-semibold flex items-center space-x-1">
                <span>Mapping requires verification</span>
            </span>`;
        } else if (det.requires_human_verification) {
            categoryDisplay = `<span class="text-amber-400 font-semibold">Unassigned (Pending Human Verification)</span>`;
        } else {
            categoryDisplay = `<span class="text-primary-heading font-medium">${det.official_category || det.assigned_category}</span>`;
        }

        row.innerHTML = `
            <td class="font-mono text-muted-desc text-[11px]">${idLabel}</td>
            <td>
                <div class="font-semibold text-primary-heading">${det.display_name}</div>
                <div class="font-mono text-[10px] text-muted-desc">Model Class: ${det.class_name}</div>
            </td>
            <td>${confBadge}</td>
            <td class="text-xs">${categoryDisplay}</td>
            <td>${binBadge}</td>
            <td class="text-xs text-secondary-label max-w-xs leading-relaxed">
                <div>${det.treatment}</div>
                <div class="text-[10px] text-muted-desc mt-0.5">${det.cpcb_schedule}</div>
            </td>
        `;

        el.detectionsTableBody.appendChild(row);
    });
}

// Render Target Bin Containers
function renderRequiredBins(binCounts, detections) {
    el.requiredBinsCards.innerHTML = '';
    const activeBins = Object.keys(binCounts);

    if (activeBins.length === 0) {
        el.requiredBinsCards.innerHTML = `
            <div class="col-span-2 text-center py-4 text-xs text-muted-desc inner-box rounded-lg">
                No automated disposal bins triggered. All candidate items require human verification or no objects detected.
            </div>
        `;
        return;
    }

    const binDetails = {
        'Yellow': {
            title: 'Yellow Biohazard Bag',
            subtitle: 'Soiled & Infectious Waste',
            borderColor: '#f59e0b',
            pill: 'bg-amber-500/10 text-amber-500 border border-amber-500/20',
            desc: 'Autoclave or high-temperature incineration (>1050°C).'
        },
        'Red': {
            title: 'Red Non-Chlorinated Bag',
            subtitle: 'Contaminated Recyclable Plastics',
            borderColor: '#ef4444',
            pill: 'bg-red-500/10 text-red-500 border border-red-500/20',
            desc: 'Autoclave / microwaving before shredding & authorized plastic recycling.'
        },
        'White': {
            title: 'White Translucent Container',
            subtitle: 'Waste Sharps & Needles',
            borderColor: '#94a3b8',
            pill: 'bg-slate-500/10 text-slate-300 border border-slate-500/20',
            desc: 'Puncture-proof container. Autoclave and sharp-pit encapsulation.'
        },
        'Blue': {
            title: 'Blue Rigid Cardboard Box',
            subtitle: 'Glassware & Medicine Vials',
            borderColor: '#3b82f6',
            pill: 'bg-blue-500/10 text-blue-400 border border-blue-500/20',
            desc: 'Disinfect with 1-2% Sodium Hypochlorite and glass recycling.'
        },
        'Black': {
            title: 'Black / Green Municipal Bin',
            subtitle: 'General Non-Hazardous Waste',
            borderColor: '#64748b',
            pill: 'bg-slate-500/10 text-slate-300 border border-slate-500/20',
            desc: 'General municipal solid waste collection.'
        }
    };

    activeBins.forEach(b => {
        const info = binDetails[b] || {
            title: `${b} Disposal Bin`,
            subtitle: 'Standard Clinical Segregation',
            borderColor: '#64748b',
            pill: 'bg-slate-500/10 text-slate-400 border border-slate-500/20',
            desc: 'Authorized clinical disposal protocol.'
        };

        const count = binCounts[b] || 1;
        const card = document.createElement('div');
        card.className = 'bin-rule-card p-3.5 space-y-1.5';
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

// Render Action Protocols Checklist
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
