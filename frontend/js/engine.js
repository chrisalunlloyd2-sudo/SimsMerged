// TIMESTAMP: 2026-05-30T01:05:00.452Z
// PROJECT_ID: SimsMerged-v1.3-Metropolis
// AGENT_ID: Gemini-CLI-Architect

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const tooltip = document.getElementById('hover-tooltip');

function resize() {
    const parent = canvas.parentElement;
    canvas.width = parent.clientWidth || window.innerWidth - 320;
    canvas.height = parent.clientHeight || window.innerHeight;
}
window.addEventListener('resize', resize);
resize();

const TILE_WIDTH = 64, TILE_HEIGHT = 32, MAP_SIZE = 40;
let selectedTile = { x: 0, y: 0 };
window.agents = window.agents || [];
let currentBuildType = 'CPU';
window.setBuildType = (type) => { currentBuildType = type; };

let camX = 0, camY = 0, zoom = 1.0;
let isDragging = false, lastMouseX = 0, lastMouseY = 0;

// Mouse Interaction & Viewport Control
canvas.oncontextmenu = (e) => e.preventDefault(); 

canvas.onmousedown = (e) => {
    if (e.button === 0) { // Left Click
        const tile = fromIso(e.clientX, e.clientY);
        const existing = districts.find(d => d.x === tile.x && d.y === tile.y);
        if (existing) {
            addRenderLog(`SELECT: ${existing.type} at [${tile.x}, ${tile.y}]`);
        } else {
            // Direct click-to-build painting!
            if (currentBuildType && BUILD_TYPES[currentBuildType]) {
                districts.push({ x: tile.x, y: tile.y, type: currentBuildType, label: `${currentBuildType}_Node` });
                addRenderLog(`GENESIS: Deployed ${currentBuildType} at [${tile.x}, ${tile.y}]`);
            } else {
                addRenderLog(`INTERACT: Empty Tile [${tile.x}, ${tile.y}]`);
            }
        }
    } else if (e.button === 2) { // Right Click
        isDragging = true;
        lastMouseX = e.clientX;
        lastMouseY = e.clientY;
    }
};

window.onmouseup = () => { isDragging = false; };

canvas.onmousemove = (e) => {
    lastMouseX = e.clientX; 
    lastMouseY = e.clientY;
    if (isDragging) {
        camX += (e.clientX - lastMouseX);
        camY += (e.clientY - lastMouseY);
    }
    const rect = canvas.getBoundingClientRect();
    selectedTile = fromIso(e.clientX, e.clientY);
};

canvas.onwheel = (e) => {
    e.preventDefault();
    const zoomSpeed = 0.1;
    if (e.deltaY < 0) zoom = Math.min(zoom + zoomSpeed, 2.0);
    else zoom = Math.max(zoom - zoomSpeed, 0.4);
};

function toIso(x, y) {
    return { 
        isoX: (x - y) * (TILE_WIDTH / 2) * zoom + canvas.width / 2 + camX, 
        isoY: (x + y) * (TILE_HEIGHT / 2) * zoom + canvas.height / 2 + camY 
    };
}

function fromIso(screenX, screenY) {
    const rect = canvas.getBoundingClientRect();
    const x = (screenX - rect.left - canvas.width / 2 - camX) / zoom;
    const y = (screenY - rect.top - canvas.height / 2 - camY) / zoom;
    const isoX = (x / (TILE_WIDTH / 2) + y / (TILE_HEIGHT / 2)) / 2;
    const isoY = (y / (TILE_HEIGHT / 2) - x / (TILE_WIDTH / 2)) / 2;
    return { x: Math.floor(isoX), y: Math.floor(isoY) };
}

// System Information Mapping (GEMINI Mandate)
const SYSTEM_INFO_MAP = {
    'CPU': 'CENTRAL_CONTROL_UNIT: Orchestrates thread scheduling and instruction pipeline.',
    'RAM': 'VOLATILE_MEMORY_BANK: High-speed buffer for active agent cognition states.',
    'SSD': 'PERSISTENT_STORAGE_HIVE: Hashed storage for historical agent memories.',
    'GPU': 'PARALLEL_COMPUTE_ARRAY: Offloads heavy visual rendering and matrix math.',
    'LLM': 'NEURAL_INFERENCE_CORE: Powered by H2O-Danube for agent decision logic.',
    'AGENT': 'ACTIVE_KERNEL_PROCESS: A living process mapped from the host machine.',
    'HOSPITAL': 'SYSTEM_RECOVERY_NODE: Restores stability to corrupted agent sub-sectors.',
    'BANK': 'DEPIN_LEDGER_AUTHORITY: Manages SPRITE minting and SHA-256 verification.'
};

const BUILD_TYPES = {
    'ABSOLUTE-Z': { 
        color: '#821af2', 
        label: 'Absolute-Zero Thermal Throttling Bypass', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Absolute-Zero Thermal Throttling Bypass node.' 
    },
    'TRITON-ENG': { 
        color: '#4e3095', 
        label: 'Triton-Engine Zero-Copy Weight Swapping', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Triton-Engine Zero-Copy Weight Swapping node.' 
    },
    'NON-ECC_BI': { 
        color: '#9ccb89', 
        label: 'Non-ECC Bit-Flip Mitigation for SLM Inference', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Non-ECC Bit-Flip Mitigation for SLM Inference node.' 
    },
    'H2O-DANUBE': { 
        color: '#3adde5', 
        label: 'H2O-Danube-1.8B Post-Training Quantization', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced H2O-Danube-1.8B Post-Training Quantization node.' 
    },
    'ADVANCED_B': { 
        color: '#1a5f1c', 
        label: 'Advanced Branch Predictor (95% Accuracy)', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Advanced Branch Predictor (95% Accuracy) node.' 
    },
    'SMOLLM-135': { 
        color: '#99cbe3', 
        label: 'SmolLM-135M Distributed Inference Handshake', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced SmolLM-135M Distributed Inference Handshake node.' 
    },
    'NON-ECC_BI': { 
        color: '#9ccb89', 
        label: 'Non-ECC Bit-Flip Mitigation for SLM Inference', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Non-ECC Bit-Flip Mitigation for SLM Inference node.' 
    },
    'ABSOLUTE-Z': { 
        color: '#821af2', 
        label: 'Absolute-Zero Thermal Throttling Bypass', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Absolute-Zero Thermal Throttling Bypass node.' 
    },
    'ADVANCED_B': { 
        color: '#1a5f1c', 
        label: 'Advanced Branch Predictor (95% Accuracy)', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Advanced Branch Predictor (95% Accuracy) node.' 
    },
    'NON-ECC_BI': { 
        color: '#9ccb89', 
        label: 'Non-ECC Bit-Flip Mitigation for SLM Inference', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Non-ECC Bit-Flip Mitigation for SLM Inference node.' 
    },
    'SMOLLM-135': { 
        color: '#99cbe3', 
        label: 'SmolLM-135M Distributed Inference Handshake', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced SmolLM-135M Distributed Inference Handshake node.' 
    },
    'NON-ECC_BI': { 
        color: '#9ccb89', 
        label: 'Non-ECC Bit-Flip Mitigation for SLM Inference', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Non-ECC Bit-Flip Mitigation for SLM Inference node.' 
    },
    'NON-ECC_BI': { 
        color: '#9ccb89', 
        label: 'Non-ECC Bit-Flip Mitigation for SLM Inference', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Non-ECC Bit-Flip Mitigation for SLM Inference node.' 
    },
    'ADVANCED_B': { 
        color: '#1a5f1c', 
        label: 'Advanced Branch Predictor (95% Accuracy)', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Advanced Branch Predictor (95% Accuracy) node.' 
    },
    'TRITON-ENG': { 
        color: '#4e3095', 
        label: 'Triton-Engine Zero-Copy Weight Swapping', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Triton-Engine Zero-Copy Weight Swapping node.' 
    },
    'ADVANCED_B': { 
        color: '#1a5f1c', 
        label: 'Advanced Branch Predictor (95% Accuracy)', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Advanced Branch Predictor (95% Accuracy) node.' 
    },
    'TRITON-ENG': { 
        color: '#4e3095', 
        label: 'Triton-Engine Zero-Copy Weight Swapping', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Triton-Engine Zero-Copy Weight Swapping node.' 
    },
    'PREDICTIVE': { 
        color: '#c73137', 
        label: 'Predictive Prefetching Logic Injection', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Predictive Prefetching Logic Injection node.' 
    },
    'MULTI-CHAN': { 
        color: '#063b41', 
        label: 'Multi-Channel DMA Memory Access', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Multi-Channel DMA Memory Access node.' 
    },
    'ADVANCED_B': { 
        color: '#1a5f1c', 
        label: 'Advanced Branch Predictor (95% Accuracy)', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Advanced Branch Predictor (95% Accuracy) node.' 
    },
    'H2O-DANUBE': { 
        color: '#3adde5', 
        label: 'H2O-Danube-1.8B Post-Training Quantization', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced H2O-Danube-1.8B Post-Training Quantization node.' 
    },
    'SMOLLM-135': { 
        color: '#99cbe3', 
        label: 'SmolLM-135M Distributed Inference Handshake', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced SmolLM-135M Distributed Inference Handshake node.' 
    },
    'MULTI-CHAN': { 
        color: '#063b41', 
        label: 'Multi-Channel DMA Memory Access', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Multi-Channel DMA Memory Access node.' 
    },
    'ABSOLUTE-Z': { 
        color: '#821af2', 
        label: 'Absolute-Zero Thermal Throttling Bypass', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Absolute-Zero Thermal Throttling Bypass node.' 
    },
    'MULTI-CHAN': { 
        color: '#063b41', 
        label: 'Multi-Channel DMA Memory Access', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Multi-Channel DMA Memory Access node.' 
    },
    'TRITON-ENG': { 
        color: '#4e3095', 
        label: 'Triton-Engine Zero-Copy Weight Swapping', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Triton-Engine Zero-Copy Weight Swapping node.' 
    },
    'ABSOLUTE-Z': { 
        color: '#821af2', 
        label: 'Absolute-Zero Thermal Throttling Bypass', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Absolute-Zero Thermal Throttling Bypass node.' 
    },
    'ABSOLUTE-Z': { 
        color: '#821af2', 
        label: 'Absolute-Zero Thermal Throttling Bypass', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Absolute-Zero Thermal Throttling Bypass node.' 
    },
    'TRITON-ENG': { 
        color: '#4e3095', 
        label: 'Triton-Engine Zero-Copy Weight Swapping', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Triton-Engine Zero-Copy Weight Swapping node.' 
    },
    'ADVANCED_B': { 
        color: '#1a5f1c', 
        label: 'Advanced Branch Predictor (95% Accuracy)', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Advanced Branch Predictor (95% Accuracy) node.' 
    },
    'ABSOLUTE-Z': { 
        color: '#821af2', 
        label: 'Absolute-Zero Thermal Throttling Bypass', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Absolute-Zero Thermal Throttling Bypass node.' 
    },
    'PREDICTIVE': { 
        color: '#c73137', 
        label: 'Predictive Prefetching Logic Injection', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Predictive Prefetching Logic Injection node.' 
    },
    'H2O-DANUBE': { 
        color: '#3adde5', 
        label: 'H2O-Danube-1.8B Post-Training Quantization', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced H2O-Danube-1.8B Post-Training Quantization node.' 
    },
    'QWEN-2-1.5': { 
        color: '#661761', 
        label: 'Qwen-2-1.5B 4-bit KV-Cache Compression', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Qwen-2-1.5B 4-bit KV-Cache Compression node.' 
    },
    'SMOLLM-135': { 
        color: '#99cbe3', 
        label: 'SmolLM-135M Distributed Inference Handshake', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced SmolLM-135M Distributed Inference Handshake node.' 
    },
    'MULTI-CHAN': { 
        color: '#063b41', 
        label: 'Multi-Channel DMA Memory Access', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Multi-Channel DMA Memory Access node.' 
    },
    'ADVANCED_B': { 
        color: '#1a5f1c', 
        label: 'Advanced Branch Predictor (95% Accuracy)', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Advanced Branch Predictor (95% Accuracy) node.' 
    },
    'CAS_LATENC': { 
        color: '#74d7d5', 
        label: 'CAS Latency Reduction (CL32 -> CL28)', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced CAS Latency Reduction (CL32 -> CL28) node.' 
    },
    'NON-ECC_BI': { 
        color: '#9ccb89', 
        label: 'Non-ECC Bit-Flip Mitigation for SLM Inference', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Non-ECC Bit-Flip Mitigation for SLM Inference node.' 
    },
    'MULTI-CHAN': { 
        color: '#063b41', 
        label: 'Multi-Channel DMA Memory Access', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Multi-Channel DMA Memory Access node.' 
    },
    'QWEN-2-1.5': { 
        color: '#661761', 
        label: 'Qwen-2-1.5B 4-bit KV-Cache Compression', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Qwen-2-1.5B 4-bit KV-Cache Compression node.' 
    },
    'CAS_LATENC': { 
        color: '#74d7d5', 
        label: 'CAS Latency Reduction (CL32 -> CL28)', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced CAS Latency Reduction (CL32 -> CL28) node.' 
    },
    'TRITON-ENG': { 
        color: '#4e3095', 
        label: 'Triton-Engine Zero-Copy Weight Swapping', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Triton-Engine Zero-Copy Weight Swapping node.' 
    },
    'PREDICTIVE': { 
        color: '#c73137', 
        label: 'Predictive Prefetching Logic Injection', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Predictive Prefetching Logic Injection node.' 
    },
    'ABSOLUTE-Z': { 
        color: '#821af2', 
        label: 'Absolute-Zero Thermal Throttling Bypass', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Absolute-Zero Thermal Throttling Bypass node.' 
    },
    'TRITON-ENG': { 
        color: '#4e3095', 
        label: 'Triton-Engine Zero-Copy Weight Swapping', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Triton-Engine Zero-Copy Weight Swapping node.' 
    },
    'TRITON-ENG': { 
        color: '#4e3095', 
        label: 'Triton-Engine Zero-Copy Weight Swapping', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Triton-Engine Zero-Copy Weight Swapping node.' 
    },
    'NON-ECC_BI': { 
        color: '#9ccb89', 
        label: 'Non-ECC Bit-Flip Mitigation for SLM Inference', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Non-ECC Bit-Flip Mitigation for SLM Inference node.' 
    },
    'MULTI-CHAN': { 
        color: '#063b41', 
        label: 'Multi-Channel DMA Memory Access', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Multi-Channel DMA Memory Access node.' 
    },
    'QWEN-2-1.5': { 
        color: '#661761', 
        label: 'Qwen-2-1.5B 4-bit KV-Cache Compression', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Qwen-2-1.5B 4-bit KV-Cache Compression node.' 
    },
    'MULTI-CHAN': { 
        color: '#063b41', 
        label: 'Multi-Channel DMA Memory Access', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Multi-Channel DMA Memory Access node.' 
    },
    'SMOLLM-135': { 
        color: '#99cbe3', 
        label: 'SmolLM-135M Distributed Inference Handshake', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced SmolLM-135M Distributed Inference Handshake node.' 
    },
    'SMOLLM-135': { 
        color: '#99cbe3', 
        label: 'SmolLM-135M Distributed Inference Handshake', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced SmolLM-135M Distributed Inference Handshake node.' 
    },
    'CAS_LATENC': { 
        color: '#74d7d5', 
        label: 'CAS Latency Reduction (CL32 -> CL28)', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced CAS Latency Reduction (CL32 -> CL28) node.' 
    },
    'NON-ECC_BI': { 
        color: '#9ccb89', 
        label: 'Non-ECC Bit-Flip Mitigation for SLM Inference', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Non-ECC Bit-Flip Mitigation for SLM Inference node.' 
    },
    'SMOLLM-135': { 
        color: '#99cbe3', 
        label: 'SmolLM-135M Distributed Inference Handshake', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced SmolLM-135M Distributed Inference Handshake node.' 
    },
    'QWEN-2-1.5': { 
        color: '#661761', 
        label: 'Qwen-2-1.5B 4-bit KV-Cache Compression', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Qwen-2-1.5B 4-bit KV-Cache Compression node.' 
    },
    'TRITON-ENG': { 
        color: '#4e3095', 
        label: 'Triton-Engine Zero-Copy Weight Swapping', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Triton-Engine Zero-Copy Weight Swapping node.' 
    },
    'ABSOLUTE-Z': { 
        color: '#821af2', 
        label: 'Absolute-Zero Thermal Throttling Bypass', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Absolute-Zero Thermal Throttling Bypass node.' 
    },
    'ABSOLUTE-Z': { 
        color: '#821af2', 
        label: 'Absolute-Zero Thermal Throttling Bypass', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Absolute-Zero Thermal Throttling Bypass node.' 
    },
    'MULTI-CHAN': { 
        color: '#063b41', 
        label: 'Multi-Channel DMA Memory Access', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Multi-Channel DMA Memory Access node.' 
    },
    'MULTI-CHAN': { 
        color: '#063b41', 
        label: 'Multi-Channel DMA Memory Access', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Multi-Channel DMA Memory Access node.' 
    },
    'QWEN-2-1.5': { 
        color: '#661761', 
        label: 'Qwen-2-1.5B 4-bit KV-Cache Compression', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Qwen-2-1.5B 4-bit KV-Cache Compression node.' 
    },
    'TRITON-ENG': { 
        color: '#4e3095', 
        label: 'Triton-Engine Zero-Copy Weight Swapping', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Triton-Engine Zero-Copy Weight Swapping node.' 
    },
    'SMOLLM-135': { 
        color: '#99cbe3', 
        label: 'SmolLM-135M Distributed Inference Handshake', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced SmolLM-135M Distributed Inference Handshake node.' 
    },
    'TRITON-ENG': { 
        color: '#4e3095', 
        label: 'Triton-Engine Zero-Copy Weight Swapping', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Triton-Engine Zero-Copy Weight Swapping node.' 
    },
    'SMOLLM-135': { 
        color: '#99cbe3', 
        label: 'SmolLM-135M Distributed Inference Handshake', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced SmolLM-135M Distributed Inference Handshake node.' 
    },
    'ABSOLUTE-Z': { 
        color: '#821af2', 
        label: 'Absolute-Zero Thermal Throttling Bypass', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Absolute-Zero Thermal Throttling Bypass node.' 
    },
    'SMOLLM-135': { 
        color: '#99cbe3', 
        label: 'SmolLM-135M Distributed Inference Handshake', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced SmolLM-135M Distributed Inference Handshake node.' 
    },
    'SMOLLM-135': { 
        color: '#99cbe3', 
        label: 'SmolLM-135M Distributed Inference Handshake', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced SmolLM-135M Distributed Inference Handshake node.' 
    },
    'TRITON-ENG': { 
        color: '#4e3095', 
        label: 'Triton-Engine Zero-Copy Weight Swapping', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Triton-Engine Zero-Copy Weight Swapping node.' 
    },
    'MULTI-CHAN': { 
        color: '#063b41', 
        label: 'Multi-Channel DMA Memory Access', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Multi-Channel DMA Memory Access node.' 
    },
    'TRITON-ENG': { 
        color: '#4e3095', 
        label: 'Triton-Engine Zero-Copy Weight Swapping', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Triton-Engine Zero-Copy Weight Swapping node.' 
    },
    'ADVANCED_B': { 
        color: '#1a5f1c', 
        label: 'Advanced Branch Predictor (95% Accuracy)', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Advanced Branch Predictor (95% Accuracy) node.' 
    },
    'MULTI-CHAN': { 
        color: '#063b41', 
        label: 'Multi-Channel DMA Memory Access', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Multi-Channel DMA Memory Access node.' 
    },
    'QWEN-2-1.5': { 
        color: '#661761', 
        label: 'Qwen-2-1.5B 4-bit KV-Cache Compression', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Qwen-2-1.5B 4-bit KV-Cache Compression node.' 
    },
    'TRITON-ENG': { 
        color: '#4e3095', 
        label: 'Triton-Engine Zero-Copy Weight Swapping', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Triton-Engine Zero-Copy Weight Swapping node.' 
    },
    'QWEN-2-1.5': { 
        color: '#661761', 
        label: 'Qwen-2-1.5B 4-bit KV-Cache Compression', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Qwen-2-1.5B 4-bit KV-Cache Compression node.' 
    },
    'MULTI-CHAN': { 
        color: '#063b41', 
        label: 'Multi-Channel DMA Memory Access', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Multi-Channel DMA Memory Access node.' 
    },
    'QWEN-2-1.5': { 
        color: '#661761', 
        label: 'Qwen-2-1.5B 4-bit KV-Cache Compression', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Qwen-2-1.5B 4-bit KV-Cache Compression node.' 
    },
    'MULTI-CHAN': { 
        color: '#063b41', 
        label: 'Multi-Channel DMA Memory Access', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Multi-Channel DMA Memory Access node.' 
    },
    'ADVANCED_B': { 
        color: '#1a5f1c', 
        label: 'Advanced Branch Predictor (95% Accuracy)', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Advanced Branch Predictor (95% Accuracy) node.' 
    },
    'TRITON-ENG': { 
        color: '#4e3095', 
        label: 'Triton-Engine Zero-Copy Weight Swapping', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Triton-Engine Zero-Copy Weight Swapping node.' 
    },
    'SMOLLM-135': { 
        color: '#99cbe3', 
        label: 'SmolLM-135M Distributed Inference Handshake', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced SmolLM-135M Distributed Inference Handshake node.' 
    },
    'PREDICTIVE': { 
        color: '#c73137', 
        label: 'Predictive Prefetching Logic Injection', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Predictive Prefetching Logic Injection node.' 
    },
    'ADVANCED_B': { 
        color: '#1a5f1c', 
        label: 'Advanced Branch Predictor (95% Accuracy)', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Advanced Branch Predictor (95% Accuracy) node.' 
    },
    'ABSOLUTE-Z': { 
        color: '#821af2', 
        label: 'Absolute-Zero Thermal Throttling Bypass', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Absolute-Zero Thermal Throttling Bypass node.' 
    },
    'ABSOLUTE-Z': { 
        color: '#821af2', 
        label: 'Absolute-Zero Thermal Throttling Bypass', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Absolute-Zero Thermal Throttling Bypass node.' 
    },
    'H2O-DANUBE': { 
        color: '#3adde5', 
        label: 'H2O-Danube-1.8B Post-Training Quantization', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced H2O-Danube-1.8B Post-Training Quantization node.' 
    },
    'CAS_LATENC': { 
        color: '#74d7d5', 
        label: 'CAS Latency Reduction (CL32 -> CL28)', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced CAS Latency Reduction (CL32 -> CL28) node.' 
    },
    'ABSOLUTE-Z': { 
        color: '#821af2', 
        label: 'Absolute-Zero Thermal Throttling Bypass', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Absolute-Zero Thermal Throttling Bypass node.' 
    },
    'ABSOLUTE-Z': { 
        color: '#821af2', 
        label: 'Absolute-Zero Thermal Throttling Bypass', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Absolute-Zero Thermal Throttling Bypass node.' 
    },
    'QWEN-2-1.5': { 
        color: '#661761', 
        label: 'Qwen-2-1.5B 4-bit KV-Cache Compression', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Qwen-2-1.5B 4-bit KV-Cache Compression node.' 
    },
    'ADVANCED_B': { 
        color: '#1a5f1c', 
        label: 'Advanced Branch Predictor (95% Accuracy)', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Advanced Branch Predictor (95% Accuracy) node.' 
    },
    'MULTI-CHAN': { 
        color: '#063b41', 
        label: 'Multi-Channel DMA Memory Access', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Multi-Channel DMA Memory Access node.' 
    },
    'TRITON-ENG': { 
        color: '#4e3095', 
        label: 'Triton-Engine Zero-Copy Weight Swapping', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Triton-Engine Zero-Copy Weight Swapping node.' 
    },
    'NON-ECC_BI': { 
        color: '#9ccb89', 
        label: 'Non-ECC Bit-Flip Mitigation for SLM Inference', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Non-ECC Bit-Flip Mitigation for SLM Inference node.' 
    },
    'QWEN-2-1.5': { 
        color: '#661761', 
        label: 'Qwen-2-1.5B 4-bit KV-Cache Compression', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Qwen-2-1.5B 4-bit KV-Cache Compression node.' 
    },
    'PREDICTIVE': { 
        color: '#c73137', 
        label: 'Predictive Prefetching Logic Injection', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Predictive Prefetching Logic Injection node.' 
    },
    'NON-ECC_BI': { 
        color: '#9ccb89', 
        label: 'Non-ECC Bit-Flip Mitigation for SLM Inference', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Non-ECC Bit-Flip Mitigation for SLM Inference node.' 
    },
    'TRITON-ENG': { 
        color: '#4e3095', 
        label: 'Triton-Engine Zero-Copy Weight Swapping', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Triton-Engine Zero-Copy Weight Swapping node.' 
    },
    'CAS_LATENC': { 
        color: '#74d7d5', 
        label: 'CAS Latency Reduction (CL32 -> CL28)', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced CAS Latency Reduction (CL32 -> CL28) node.' 
    },
    'SMOLLM-135': { 
        color: '#99cbe3', 
        label: 'SmolLM-135M Distributed Inference Handshake', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced SmolLM-135M Distributed Inference Handshake node.' 
    },
    'ADVANCED_B': { 
        color: '#1a5f1c', 
        label: 'Advanced Branch Predictor (95% Accuracy)', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Advanced Branch Predictor (95% Accuracy) node.' 
    },
    'ABSOLUTE-Z': { 
        color: '#821af2', 
        label: 'Absolute-Zero Thermal Throttling Bypass', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Absolute-Zero Thermal Throttling Bypass node.' 
    },
    'TRITON-ENG': { 
        color: '#4e3095', 
        label: 'Triton-Engine Zero-Copy Weight Swapping', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Triton-Engine Zero-Copy Weight Swapping node.' 
    },
    'ADVANCED_B': { 
        color: '#1a5f1c', 
        label: 'Advanced Branch Predictor (95% Accuracy)', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Advanced Branch Predictor (95% Accuracy) node.' 
    },
    'SMOLLM-135': { 
        color: '#99cbe3', 
        label: 'SmolLM-135M Distributed Inference Handshake', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced SmolLM-135M Distributed Inference Handshake node.' 
    },
    'ADVANCED_B': { 
        color: '#1a5f1c', 
        label: 'Advanced Branch Predictor (95% Accuracy)', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Advanced Branch Predictor (95% Accuracy) node.' 
    },
    'CAS_LATENC': { 
        color: '#74d7d5', 
        label: 'CAS Latency Reduction (CL32 -> CL28)', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced CAS Latency Reduction (CL32 -> CL28) node.' 
    },
    'PREDICTIVE': { 
        color: '#c73137', 
        label: 'Predictive Prefetching Logic Injection', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Predictive Prefetching Logic Injection node.' 
    },
    'QWEN-2-1.5': { 
        color: '#661761', 
        label: 'Qwen-2-1.5B 4-bit KV-Cache Compression', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Qwen-2-1.5B 4-bit KV-Cache Compression node.' 
    },
    'MULTI-CHAN': { 
        color: '#063b41', 
        label: 'Multi-Channel DMA Memory Access', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Multi-Channel DMA Memory Access node.' 
    },
    'QWEN-2-1.5': { 
        color: '#661761', 
        label: 'Qwen-2-1.5B 4-bit KV-Cache Compression', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Qwen-2-1.5B 4-bit KV-Cache Compression node.' 
    },
    'ABSOLUTE-Z': { 
        color: '#821af2', 
        label: 'Absolute-Zero Thermal Throttling Bypass', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Absolute-Zero Thermal Throttling Bypass node.' 
    },
    'ABSOLUTE-Z': { 
        color: '#821af2', 
        label: 'Absolute-Zero Thermal Throttling Bypass', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Absolute-Zero Thermal Throttling Bypass node.' 
    },
    'SMOLLM-135': { 
        color: '#99cbe3', 
        label: 'SmolLM-135M Distributed Inference Handshake', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced SmolLM-135M Distributed Inference Handshake node.' 
    },
    'SMOLLM-135': { 
        color: '#99cbe3', 
        label: 'SmolLM-135M Distributed Inference Handshake', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced SmolLM-135M Distributed Inference Handshake node.' 
    },
    'TRITON-ENG': { 
        color: '#4e3095', 
        label: 'Triton-Engine Zero-Copy Weight Swapping', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Triton-Engine Zero-Copy Weight Swapping node.' 
    },
    'PREDICTIVE': { 
        color: '#c73137', 
        label: 'Predictive Prefetching Logic Injection', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Predictive Prefetching Logic Injection node.' 
    },
    'QWEN-2-1.5': { 
        color: '#661761', 
        label: 'Qwen-2-1.5B 4-bit KV-Cache Compression', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Qwen-2-1.5B 4-bit KV-Cache Compression node.' 
    },
    'CAS_LATENC': { 
        color: '#74d7d5', 
        label: 'CAS Latency Reduction (CL32 -> CL28)', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced CAS Latency Reduction (CL32 -> CL28) node.' 
    },
    'TRITON-ENG': { 
        color: '#4e3095', 
        label: 'Triton-Engine Zero-Copy Weight Swapping', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Triton-Engine Zero-Copy Weight Swapping node.' 
    },
    'SMOLLM-135': { 
        color: '#99cbe3', 
        label: 'SmolLM-135M Distributed Inference Handshake', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced SmolLM-135M Distributed Inference Handshake node.' 
    },
    'TRITON-ENG': { 
        color: '#4e3095', 
        label: 'Triton-Engine Zero-Copy Weight Swapping', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Triton-Engine Zero-Copy Weight Swapping node.' 
    },
    'ABSOLUTE-Z': { 
        color: '#821af2', 
        label: 'Absolute-Zero Thermal Throttling Bypass', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Absolute-Zero Thermal Throttling Bypass node.' 
    },
    'SMOLLM-135': { 
        color: '#99cbe3', 
        label: 'SmolLM-135M Distributed Inference Handshake', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced SmolLM-135M Distributed Inference Handshake node.' 
    },
    'SMOLLM-135': { 
        color: '#99cbe3', 
        label: 'SmolLM-135M Distributed Inference Handshake', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced SmolLM-135M Distributed Inference Handshake node.' 
    },
    'TRITON-ENG': { 
        color: '#4e3095', 
        label: 'Triton-Engine Zero-Copy Weight Swapping', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Triton-Engine Zero-Copy Weight Swapping node.' 
    },
    'MULTI-CHAN': { 
        color: '#063b41', 
        label: 'Multi-Channel DMA Memory Access', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Multi-Channel DMA Memory Access node.' 
    },
    'ADVANCED_B': { 
        color: '#1a5f1c', 
        label: 'Advanced Branch Predictor (95% Accuracy)', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Advanced Branch Predictor (95% Accuracy) node.' 
    },
    'CAS_LATENC': { 
        color: '#74d7d5', 
        label: 'CAS Latency Reduction (CL32 -> CL28)', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced CAS Latency Reduction (CL32 -> CL28) node.' 
    },
    'TRITON-ENG': { 
        color: '#4e3095', 
        label: 'Triton-Engine Zero-Copy Weight Swapping', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Triton-Engine Zero-Copy Weight Swapping node.' 
    },
    'DYNAMIC_UR': { 
        color: '#0c7e4f', 
        label: 'Dynamic Urban Zoning Algorithms', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Dynamic Urban Zoning Algorithms node.' 
    },
    'ZERO-COPY_': { 
        color: '#1abf88', 
        label: 'Zero-copy InfiniBand Networking', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Zero-copy InfiniBand Networking node.' 
    },
    'HEADLESS_U': { 
        color: '#40a842', 
        label: 'Headless UI Vision & Automated Grading', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Headless UI Vision & Automated Grading node.' 
    },
    'GENERATIVE': { 
        color: '#1beaf8', 
        label: 'Generative AI Agent Chat prompt engineering', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Generative AI Agent Chat prompt engineering node.' 
    },
    'DEPIN_STOC': { 
        color: '#f178a3', 
        label: 'DePIN Stock Market Volatility Heuristics', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced DePIN Stock Market Volatility Heuristics node.' 
    },
    'RUST-BASED': { 
        color: '#2101e5', 
        label: 'Rust-based Node Auto-Scaling', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Rust-based Node Auto-Scaling node.' 
    },
    'ZERO-COPY_': { 
        color: '#1abf88', 
        label: 'Zero-copy InfiniBand Networking', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Zero-copy InfiniBand Networking node.' 
    },
    'ADVANCED_G': { 
        color: '#1fb154', 
        label: 'Advanced Graph RAG Schemas', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Advanced Graph RAG Schemas node.' 
    },
    'GENERATIVE': { 
        color: '#1beaf8', 
        label: 'Generative AI Agent Chat prompt engineering', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Generative AI Agent Chat prompt engineering node.' 
    },
    'DYNAMIC_UR': { 
        color: '#0c7e4f', 
        label: 'Dynamic Urban Zoning Algorithms', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Dynamic Urban Zoning Algorithms node.' 
    },
    'AES-256_GE': { 
        color: '#f6dc2e', 
        label: 'AES-256 Genetic Data Encryption', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced AES-256 Genetic Data Encryption node.' 
    },
    'ADVANCED_G': { 
        color: '#1fb154', 
        label: 'Advanced Graph RAG Schemas', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Advanced Graph RAG Schemas node.' 
    },
    'GENERATIVE': { 
        color: '#1beaf8', 
        label: 'Generative AI Agent Chat prompt engineering', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Generative AI Agent Chat prompt engineering node.' 
    },
    'DEPIN_CRYP': { 
        color: '#c1e945', 
        label: 'DePIN Crypto Tokenomics via Smart Contracts', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced DePIN Crypto Tokenomics via Smart Contracts node.' 
    },
    'ZERO-COPY_': { 
        color: '#1abf88', 
        label: 'Zero-copy InfiniBand Networking', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Zero-copy InfiniBand Networking node.' 
    },
    'RUST-BASED': { 
        color: '#2101e5', 
        label: 'Rust-based Node Auto-Scaling', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Rust-based Node Auto-Scaling node.' 
    },
    'GENERATIVE': { 
        color: '#1beaf8', 
        label: 'Generative AI Agent Chat prompt engineering', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Generative AI Agent Chat prompt engineering node.' 
    },
    'ISOMETRIC_': { 
        color: '#9ef5c6', 
        label: 'Isometric WebGL rendering optimization', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Isometric WebGL rendering optimization node.' 
    },
    'GENERATIVE': { 
        color: '#1beaf8', 
        label: 'Generative AI Agent Chat prompt engineering', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Generative AI Agent Chat prompt engineering node.' 
    },
    'A*_PATHFIN': { 
        color: '#dfd4f8', 
        label: 'A* Pathfinding for Swarm Agents', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced A* Pathfinding for Swarm Agents node.' 
    },
    'RUST-BASED': { 
        color: '#2101e5', 
        label: 'Rust-based Node Auto-Scaling', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Rust-based Node Auto-Scaling node.' 
    },
    'LOW-LATENC': { 
        color: '#eef3ce', 
        label: 'Low-latency Packet Interconnects', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Low-latency Packet Interconnects node.' 
    },
    'DEPIN_STOC': { 
        color: '#f178a3', 
        label: 'DePIN Stock Market Volatility Heuristics', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced DePIN Stock Market Volatility Heuristics node.' 
    },
    'AES-256_GE': { 
        color: '#f6dc2e', 
        label: 'AES-256 Genetic Data Encryption', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced AES-256 Genetic Data Encryption node.' 
    },
    'DYNAMIC_UR': { 
        color: '#0c7e4f', 
        label: 'Dynamic Urban Zoning Algorithms', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Dynamic Urban Zoning Algorithms node.' 
    },
    'LOW-LATENC': { 
        color: '#eef3ce', 
        label: 'Low-latency Packet Interconnects', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Low-latency Packet Interconnects node.' 
    },
    'HEADLESS_U': { 
        color: '#40a842', 
        label: 'Headless UI Vision & Automated Grading', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Headless UI Vision & Automated Grading node.' 
    },
    'DEPIN_STOC': { 
        color: '#f178a3', 
        label: 'DePIN Stock Market Volatility Heuristics', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced DePIN Stock Market Volatility Heuristics node.' 
    },
    'ZERO-COPY_': { 
        color: '#1abf88', 
        label: 'Zero-copy InfiniBand Networking', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Zero-copy InfiniBand Networking node.' 
    },
    'LOW-LATENC': { 
        color: '#eef3ce', 
        label: 'Low-latency Packet Interconnects', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Low-latency Packet Interconnects node.' 
    },
    'PROCEDURAL': { 
        color: '#71de20', 
        label: 'Procedural Building Asset Generation', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Procedural Building Asset Generation node.' 
    },
    'DYNAMIC_UR': { 
        color: '#0c7e4f', 
        label: 'Dynamic Urban Zoning Algorithms', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Dynamic Urban Zoning Algorithms node.' 
    },
    'GENERATIVE': { 
        color: '#1beaf8', 
        label: 'Generative AI Agent Chat prompt engineering', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Generative AI Agent Chat prompt engineering node.' 
    },
    'A*_PATHFIN': { 
        color: '#dfd4f8', 
        label: 'A* Pathfinding for Swarm Agents', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced A* Pathfinding for Swarm Agents node.' 
    },
    'LOW-LATENC': { 
        color: '#eef3ce', 
        label: 'Low-latency Packet Interconnects', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Low-latency Packet Interconnects node.' 
    },
    'DYNAMIC_UR': { 
        color: '#0c7e4f', 
        label: 'Dynamic Urban Zoning Algorithms', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Dynamic Urban Zoning Algorithms node.' 
    },
    'DYNAMIC_UR': { 
        color: '#0c7e4f', 
        label: 'Dynamic Urban Zoning Algorithms', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Dynamic Urban Zoning Algorithms node.' 
    },
    'PROCEDURAL': { 
        color: '#71de20', 
        label: 'Procedural Building Asset Generation', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Procedural Building Asset Generation node.' 
    },
    'DYNAMIC_UR': { 
        color: '#0c7e4f', 
        label: 'Dynamic Urban Zoning Algorithms', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Dynamic Urban Zoning Algorithms node.' 
    },
    'HEADLESS_U': { 
        color: '#40a842', 
        label: 'Headless UI Vision & Automated Grading', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Headless UI Vision & Automated Grading node.' 
    },
    'DEPIN_CRYP': { 
        color: '#c1e945', 
        label: 'DePIN Crypto Tokenomics via Smart Contracts', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced DePIN Crypto Tokenomics via Smart Contracts node.' 
    },
    'RUST-BASED': { 
        color: '#2101e5', 
        label: 'Rust-based Node Auto-Scaling', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Rust-based Node Auto-Scaling node.' 
    },
    'GENERATIVE': { 
        color: '#1beaf8', 
        label: 'Generative AI Agent Chat prompt engineering', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced Generative AI Agent Chat prompt engineering node.' 
    },
    'CPU': { color: '#ff4d4d', label: 'Silicon Central', locked: false, category: 'Hardware', desc: 'Central compute core.' },
    'RAM': { color: '#4dff88', label: 'Memory Matrix', locked: false, category: 'Hardware', desc: 'Volatile data pool.' },
    'GPU': { color: '#4d94ff', label: 'Graphics Grid', locked: false, category: 'Hardware', desc: 'Parallel math array.' },
    'SSD': { color: '#ffffff', label: 'NVMe SSD', locked: false, category: 'Hardware', desc: 'Persistent storage node.' },
    'NORTHBRIDGE': { color: '#00ffff', label: 'Northbridge', locked: false, category: 'Hardware', desc: 'High-speed system link.' },
    'SOUTHBRIDGE': { color: '#0055ff', label: 'Southbridge', locked: false, category: 'Hardware', desc: 'I/O peripheral hub.' },
    'REGISTRY': { color: '#ffff00', label: 'Registry Hive', locked: false, category: 'Logic', desc: 'System configuration keys.' },
    'MEM_CTRL': { color: '#aa00ff', label: 'Mem Controller', locked: false, category: 'Hardware', desc: 'Data retrieval unit.' },
    'LLM': { color: '#00ffff', label: 'AI Intelligence', category: 'Software', desc: 'Neural inference cluster.' },
    'AGENT': { color: '#ffcc00', label: 'Agent Hub', category: 'Urban', desc: 'Deployment node for AI Kernels.' },
    'VDB': { color: '#ff00ff', label: 'Knowledge DB', category: 'Software', desc: 'Vectorized memory indexing.' },
    'PLANT': { color: '#fa0', label: 'Swarm Factory', category: 'Industrial', desc: 'Automation unit production.' },
    'SCHOOL': { color: '#4facfe', label: 'Education Node', category: 'Urban', desc: 'Agent alignment & training.' },
    'HOSPITAL': { color: '#ff4444', label: 'Sanctuary', category: 'Urban', desc: 'System healing & restoration.' },
    'BANK': { color: '#ffd700', label: 'Crypto Bank', category: 'Finance', desc: 'SHA256 Ledger & Sprite vault.' },
    'HOUSE': { color: '#888', label: 'Kernel Housing', category: 'Urban', desc: 'Resident agent sub-sectors.' },
    'TREE': { color: '#0a3d0a', label: 'Logic Foliage', category: 'Env', desc: 'Atmospheric entropy sinks.' },
    'WATER': { color: '#0055ff', label: 'Data Cooling', category: 'Env', desc: 'Thermal dissipation reservoirs.' },
    'ROAD': { color: '#222', label: 'Protocol Path', category: 'Network', desc: 'Static dataflow trajectory.' },
    'RESEARCH': { color: '#00ffcc', label: 'Research Nexus', category: 'Logic', desc: 'Advanced hyperparameter tuning and model optimization pipeline.' }
};

let districts = [
    { x: 0, y: 0, type: 'CPU', label: 'Silicon_Main' },
    { x: 3, y: 0, type: 'RAM', label: 'Mem_Pool' },
    { x: -3, y: 0, type: 'GPU', label: 'Graphics_Grid' },
    { x: 1, y: 1, type: 'NORTHBRIDGE', label: 'HS_Link' },
    { x: 1, y: -1, type: 'SOUTHBRIDGE', label: 'IO_Hub' },
    { x: -5, y: -5, type: 'SSD', label: 'Storage_Hive' },
    { x: 5, y: -5, type: 'REGISTRY', label: 'Config_Hive' },
    { x: -10, y: -10, type: 'LLM', label: 'Desktop_Layer' },
    { x: 10, y: 10, type: 'MODEM', settings: {ip: '192.168.1.1'} },
    { x: 5, y: 5, type: 'LLM', label: 'Intelligence' },
    { x: 7, y: 5, type: 'PLANT', label: 'Fabricator' },
    { x: -5, y: 5, type: 'HOSPITAL', label: 'Healing_Node' }
];

const RENDER_LOG = [];
function addRenderLog(msg) {
    RENDER_LOG.push(`[${new Date().toLocaleTimeString()}] ${msg}`);
    if(RENDER_LOG.length > 20) RENDER_LOG.shift();
}

function drawStructure(isoX, isoY, color, type, locked) {
    const bSize = 16 * zoom;
    let h = (locked ? 10 : 32) * zoom;
    if (type === 'TREE') h = 8 * zoom;
    if (type === 'WATER') h = 2 * zoom;
    if (type === 'ROAD') h = 1 * zoom;
    if (type === 'AGENT') h = 12 * zoom;

    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.moveTo(isoX - bSize, isoY); ctx.lineTo(isoX, isoY + bSize/2);
    ctx.lineTo(isoX, isoY + bSize/2 - h); ctx.lineTo(isoX - bSize, isoY - h);
    ctx.closePath(); ctx.fill();
    
    ctx.fillStyle = ctx.fillStyle.replace(')', ', 0.7)').replace('rgb', 'rgba');
    ctx.beginPath();
    ctx.moveTo(isoX, isoY + bSize/2); ctx.lineTo(isoX + bSize, isoY);
    ctx.lineTo(isoX + bSize, isoY - h); ctx.lineTo(isoX, isoY + bSize/2 - h);
    ctx.closePath(); ctx.fill();

    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.moveTo(isoX, isoY - h); ctx.lineTo(isoX + bSize, isoY - bSize/2 - h);
    ctx.lineTo(isoX, isoY - bSize - h); ctx.lineTo(isoX - bSize, isoY - bSize/2 - h);
    ctx.closePath(); ctx.fill();
    
    if (type !== 'WATER' && type !== 'ROAD') {
        ctx.strokeStyle = '#fff'; ctx.lineWidth = 0.5 * zoom; ctx.stroke();
    }
}

function drawTile(x, y, color = '#050a05', isHovered = false, districtMap) {
    // PERFORMANCE OPTIMIZATION: Inline isometric calculations to avoid object allocation (saves 3,600 allocations/frame!)
    const halfW = 32 * zoom; // TILE_WIDTH / 2
    const halfH = 16 * zoom; // TILE_HEIGHT / 2
    const centerX = canvas.width / 2 + camX;
    const centerY = canvas.height / 2 + camY;
    const isoX = (x - y) * halfW + centerX;
    const isoY = (x + y) * halfH + centerY;

    const tw = TILE_WIDTH * zoom, th = TILE_HEIGHT * zoom;
    if (isoX < -tw || isoX > canvas.width + tw || isoY < -th || isoY > canvas.height + th) return;
    
    let finalColor = color;
    const d = districtMap[`${x},${y}`];
    const isHardware = d && BUILD_TYPES[d.type] && BUILD_TYPES[d.type].category === 'Hardware';
    
    ctx.beginPath();
    ctx.moveTo(isoX, isoY); ctx.lineTo(isoX + tw / 2, isoY + th / 2);
    ctx.lineTo(isoX, isoY + th); ctx.lineTo(isoX - tw / 2, isoY + th / 2);
    ctx.closePath();
    ctx.fillStyle = isHovered ? '#102510' : finalColor;
    ctx.fill();
    ctx.strokeStyle = isHardware ? '#00ffff44' : '#001a00'; 
    ctx.lineWidth = isHardware ? 2 : 1;
    ctx.stroke();

    if (d) {
        let info = BUILD_TYPES[d.type] || { color: 'gray' };
        drawStructure(isoX, isoY + th/2, info.color, d.type, info.locked);
        ctx.fillStyle = 'white'; ctx.font = `bold ${Math.max(10, 14*zoom)}px Arial`;
        ctx.fillText(d.label || d.type, isoX - 12*zoom, isoY - 20*zoom);
    }
}

const packets = [];

function spawnPacket(fx, fy, tx, ty, color, protocol, speed) {
    packets.push({
        fx: fx, fy: fy,
        tx: tx, ty: ty,
        progress: 0.0,
        color: color,
        protocol: protocol,
        speed: speed || 0.02
    });
}

function drawPackets() {
    for (let i = packets.length - 1; i >= 0; i--) {
        const p = packets[i];
        p.progress += p.speed;
        if (p.progress >= 1.0) {
            packets.splice(i, 1);
            continue;
        }
        
        const fromScreen = toIso(p.fx, p.fy);
        const toScreen = toIso(p.tx, p.ty);
        
        // Lerp positions
        const x = fromScreen.isoX + (toScreen.isoX - fromScreen.isoX) * p.progress;
        const y = fromScreen.isoY + (toScreen.isoY - fromScreen.isoY) * p.progress;
        
        // Render packet particle core
        ctx.fillStyle = p.color;
        ctx.beginPath();
        ctx.arc(x, y, 4 * zoom, 0, Math.PI * 2);
        ctx.fill();
        
        // Render glowing veil
        ctx.fillStyle = p.color + "22";
        ctx.beginPath();
        ctx.arc(x, y, 8 * zoom, 0, Math.PI * 2);
        ctx.fill();
        
        // Render floating text of the active protocols
        ctx.fillStyle = '#00ffff';
        ctx.font = `${Math.max(6, 7 * zoom)}px monospace`;
        ctx.fillText(p.protocol, x + 6 * zoom, y - 2 * zoom);
    }
}

function drawTraffic(typeMap) {
    if (!window.activeLinks) return;
    
    window.activeLinks.forEach(link => {
        const fromNodes = typeMap[link.from] || [];
        const toNodes = typeMap[link.to] || [];
        
        if (fromNodes.length > 0 && toNodes.length > 0) {
            fromNodes.forEach(fNode => {
                toNodes.forEach(tNode => {
                    const from = toIso(fNode.x, fNode.y);
                    const to = toIso(tNode.x, tNode.y);
                    
                    // Draw Data Pipe
                    ctx.strokeStyle = link.color + '44'; // Semi-transparent
                    ctx.lineWidth = 1 * zoom;
                    ctx.beginPath();
                    ctx.moveTo(from.isoX, from.isoY);
                    ctx.lineTo(to.isoX, to.isoY);
                    ctx.stroke();
                    
                    // Animate Packets
                    if (Math.random() < 0.03) {
                        spawnPacket(fNode.x, fNode.y, tNode.x, tNode.y, link.color, link.protocol, link.speed || 0.02);
                    }
                });
            });
        }
    });
}

const weatherParticles = [];

function drawWeather() {
    const weather = window.systemWeather || "CLEAR";
    if (weather === "CLEAR") return;
    
    // Seed new rain particles
    if (weatherParticles.length < 150) {
        weatherParticles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * -100,
            speed: 5 + Math.random() * 8,
            length: 10 + Math.random() * 15,
            color: weather === "DATA_RAIN" ? "#00ffff" : (weather === "CYBER_STORM" ? "#ffd700" : "#ff4444")
        });
    }
    
    // Draw and update falling particles
    for (let i = weatherParticles.length - 1; i >= 0; i--) {
        const p = weatherParticles[i];
        p.y += p.speed;
        
        ctx.strokeStyle = p.color + "66";
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(p.x, p.y);
        ctx.lineTo(p.x - 2, p.y + p.length);
        ctx.stroke();
        
        if (p.y > canvas.height) {
            weatherParticles.splice(i, 1);
        }
    }
    
    // Draw stormy lightning flash
    if ((weather === "CYBER_STORM" || weather === "ACID_CORRUPTION") && Math.random() < 0.02) {
        ctx.fillStyle = weather === "CYBER_STORM" ? "rgba(255, 215, 0, 0.15)" : "rgba(255, 68, 68, 0.12)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // Short retro sound bleep for atmospheric thunder
        // PERFORMANCE OPTIMIZATION: Reuse global AudioContext to avoid system device limits and warning alerts
        try {
            if (!window.globalAudioCtx) {
                window.globalAudioCtx = new (window.AudioContext || window.webkitAudioContext)();
            }
            const audioCtx = window.globalAudioCtx;
            if (audioCtx.state === 'suspended') {
                audioCtx.resume();
            }
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(45 + Math.random() * 30, audioCtx.currentTime);
            gain.gain.setValueAtTime(0.02, audioCtx.currentTime);
            osc.start();
            gain.gain.exponentialRampToValueAtTime(0.00001, audioCtx.currentTime + 0.35);
            osc.stop(audioCtx.currentTime + 0.4);
        } catch(e) {}
    }
}

// PERFORMANCE OPTIMIZATION: Cache spatial map for O(1) rendering lookups to avoid rebuilding maps 60 times a second
let cachedDistrictMap = {};
let cachedTypeMap = {};
let cachedDistrictsLength = -1;

function updateDistrictMapsIfNeeded() {
    if (districts.length !== cachedDistrictsLength) {
        cachedDistrictMap = {};
        cachedTypeMap = {};
        districts.forEach(d => {
            cachedDistrictMap[`${d.x},${d.y}`] = d;
            if (!cachedTypeMap[d.type]) cachedTypeMap[d.type] = [];
            cachedTypeMap[d.type].push(d);
        });
        cachedDistrictsLength = districts.length;
    }
}

let lastFrameTime = 0;
const fpsInterval = 1000 / 24; // Cap at 24 FPS (Cinematic Isometric Speed)

function draw(timestamp) {
    requestAnimationFrame(draw);
    
    if (!timestamp) timestamp = performance.now();
    const elapsed = timestamp - lastFrameTime;
    
    if (elapsed < fpsInterval) {
        return;
    }
    lastFrameTime = timestamp - (elapsed % fpsInterval);

    // PERFORMANCE OPTIMIZATION: If canvas is hidden (e.g. active 3D WebGL mode), skip entire draw loop to conserve CPU/GPU!
    if (canvas.style.display === 'none') {
        return;
    }

    let shakeX = 0, shakeY = 0;
    const weather = window.systemWeather || "CLEAR";
    if (weather === "CYBER_STORM" || weather === "ACID_CORRUPTION") {
        shakeX = (Math.random() - 0.5) * 3;
        shakeY = (Math.random() - 0.5) * 3;
    }
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.save();
    ctx.translate(shakeX, shakeY);
    
    updateDistrictMapsIfNeeded();
    const districtMap = cachedDistrictMap;
    const typeMap = cachedTypeMap;
    
    // --- VISUAL CHARGE LEAKAGE (Row Hammer Shield) ---
    if (window.chargeLeakage > 0) {
        ctx.fillStyle = `rgba(0, 255, 255, ${Math.min(0.2, window.chargeLeakage * 0.1)})`;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    }

    for (let x = -20; x < MAP_SIZE; x++) {
        for (let y = -20; y < MAP_SIZE; y++) {
            drawTile(x, y, '#050a05', (x === selectedTile.x && y === selectedTile.y), districtMap);
        }
    }

    drawTraffic(typeMap); // RENDER DATA PIPES
    drawPackets();        // ANIMATE DYNAMIC GLOWING PACKETS

    window.agents.forEach(agent => {
        // TIMESTAMP: 2026-05-29T02:54:00.000Z
        // PROJECT_ID: SimsMerged-v1.3-Metropolis
        // AGENT_ID: Antigravity-Agent
        // Asynchronous Frame Interpolation (Task 2: Asynchronous Frame Bridge protocol)
        // Lerp agent positions smoothly at 60fps instead of snapping on 1s polling intervals
        if (agent.ix === undefined) agent.ix = agent.x;
        if (agent.iy === undefined) agent.iy = agent.y;
        
        agent.ix += (agent.x - agent.ix) * 0.08;
        agent.iy += (agent.y - agent.iy) * 0.08;
        
        const { isoX, isoY } = toIso(agent.ix, agent.iy);
        const margin = 60 * zoom;
        // Viewport Culling: Skip drawing agents scrolled off-screen
        if (isoX < -margin || isoX > canvas.width + margin || isoY < -margin || isoY > canvas.height + margin) return;

        const color = agent.role === 'DOCTOR' ? '#ff4444' : (agent.role === 'TEACHER' ? '#4facfe' : '#ffcc00');
        
        // --- DRAW SSPRITE (Animated Agent) ---
        const bob = Math.sin(Date.now() * 0.005) * 5 * zoom;
        const baseSize = 8 * zoom;

        // Ground shadow (Premium depth mapping)
        ctx.fillStyle = 'rgba(0, 0, 0, 0.25)';
        ctx.beginPath();
        const shadowScale = Math.max(0.6, 1.0 - (bob / 25.0)); // scale based on bob height
        ctx.ellipse(isoX, isoY + 6 * zoom, 12 * zoom * shadowScale, 5 * zoom * shadowScale, 0, 0, Math.PI * 2);
        ctx.fill();
        
        // Body (MS Paint Style)
        ctx.fillStyle = color;
        ctx.fillRect(isoX - baseSize, isoY - baseSize*2 + bob, baseSize*2, baseSize*3);
        ctx.strokeStyle = '#000'; ctx.lineWidth = 1; ctx.strokeRect(isoX - baseSize, isoY - baseSize*2 + bob, baseSize*2, baseSize*3);
        
        // Head
        ctx.beginPath();
        ctx.arc(isoX, isoY - baseSize*3 + bob, baseSize, 0, Math.PI * 2);
        ctx.fill(); ctx.stroke();
        
        // Eyes (Blinking simulation)
        const isBlinking = Math.random() < 0.01;
        if (!isBlinking) {
            ctx.fillStyle = '#000';
            ctx.fillRect(isoX - 3*zoom, isoY - baseSize*3.2 + bob, 2*zoom, 2*zoom);
            ctx.fillRect(isoX + 1*zoom, isoY - baseSize*3.2 + bob, 2*zoom, 2*zoom);
        }

        // Draw Label
        ctx.fillStyle = 'white'; ctx.font = `${Math.max(8, 10*zoom)}px Arial`;
        ctx.fillText(`[Lvl ${agent.level}] ${agent.title || 'Agent'}`, isoX - 30*zoom, isoY - 55*zoom + bob);
        ctx.fillText(agent.name, isoX - 15*zoom, isoY - 45*zoom + bob);

        // Draw Pedagogy/Training visual glow ring
        if (agent.last_action === 'teach') {
            ctx.strokeStyle = 'rgba(0, 255, 255, 0.6)';
            ctx.lineWidth = 2 * zoom;
            ctx.beginPath();
            ctx.ellipse(isoX, isoY + bob, 15 * zoom, 7 * zoom, 0, 0, Math.PI * 2);
            ctx.stroke();
            
            // Floating tag
            ctx.fillStyle = '#00ffff';
            ctx.font = `bold ${Math.max(7, 8 * zoom)}px monospace`;
            ctx.fillText("ALIGNING_WEIGHTS...", isoX - 35 * zoom, isoY - 67 * zoom + bob);
        }
    });

    apply_interaction_logic();
    ctx.restore();
    drawWeather();
}

function apply_interaction_logic() {
    const hoveredNode = districts.find(d => d.x === selectedTile.x && d.y === selectedTile.y);
    const hoveredAgent = window.agents.find(a => a.x === selectedTile.x && a.y === selectedTile.y);

    if (hoveredAgent) {
        tooltip.style.display = 'block'; 
        tooltip.style.left = (lastMouseX + 20) + 'px'; 
        tooltip.style.top = (lastMouseY + 20) + 'px';
        
        const n = hoveredAgent.sims_needs || { energy: 100, comfort: 100, social: 100, hygiene: 100, hunger: 100 };
        
        tooltip.innerHTML = `
            <div class="tooltip-header" style="color: #ff00ff; border-bottom: 1px solid #ff00ff; margin-bottom:5px; padding-bottom:5px;">${hoveredAgent.name} <span class="sys-info-tag" style="border-color:#ff00ff; color:#ff00ff; float:right;">AI_AGENT</span></div>
            <div class="tooltip-row"><span class="tooltip-label">VOCATION:</span><span class="tooltip-value" style="color:#0f0;">${hoveredAgent.role} [Lvl ${hoveredAgent.level}]</span></div>
            <div class="tooltip-row"><span class="tooltip-label">EMOTION:</span><span class="tooltip-value" style="color:#0ff;">${hoveredAgent.state}</span></div>
            <div class="tooltip-row"><span class="tooltip-label">CONFIDENCE:</span><span class="tooltip-value" style="color:#ffd700;">${(hoveredAgent.confidence * 100).toFixed(0)}%</span></div>
            
            <div class="tooltip-desc" style="border-top: 1px dashed rgba(255, 0, 255, 0.4); padding-top: 5px; margin-top: 5px;">
                <div style="font-weight:bold; color:#ffaa00; font-size:10px; margin-bottom:5px; text-transform:uppercase;">Live Wants & Needs:</div>
                
                <div style="margin-bottom: 4px;">
                    <div style="display:flex; justify-content:space-between; font-size:9px;">
                        <span>ENERGY RECHARGE:</span><span>${n.energy}%</span>
                    </div>
                    <div style="height:4px; background:rgba(255,255,255,0.1);"><div style="height:100%; width:${n.energy}%; background:#ff4d4d;"></div></div>
                </div>
                <div style="margin-bottom: 4px;">
                    <div style="display:flex; justify-content:space-between; font-size:9px;">
                        <span>COMFORT (ALIGNMENT):</span><span>${n.comfort}%</span>
                    </div>
                    <div style="height:4px; background:rgba(255,255,255,0.1);"><div style="height:100%; width:${n.comfort}%; background:#4facfe;"></div></div>
                </div>
                <div style="margin-bottom: 4px;">
                    <div style="display:flex; justify-content:space-between; font-size:9px;">
                        <span>SOCIAL EXCHANGE:</span><span>${n.social}%</span>
                    </div>
                    <div style="height:4px; background:rgba(255,255,255,0.1);"><div style="height:100%; width:${n.social}%; background:#ffd700;"></div></div>
                </div>
                <div style="margin-bottom: 4px;">
                    <div style="display:flex; justify-content:space-between; font-size:9px;">
                        <span>HYGIENE CACHE:</span><span>${n.hygiene}%</span>
                    </div>
                    <div style="height:4px; background:rgba(255,255,255,0.1);"><div style="height:100%; width:${n.hygiene}%; background:#ff00ff;"></div></div>
                </div>
                <div>
                    <div style="display:flex; justify-content:space-between; font-size:9px;">
                        <span>HUNGER STARVATION:</span><span>${n.hunger}%</span>
                    </div>
                    <div style="height:4px; background:rgba(255,255,255,0.1);"><div style="height:100%; width:${n.hunger}%; background:#00ff00;"></div></div>
                </div>
            </div>
        `;
    } else if (hoveredNode) {
        const info = BUILD_TYPES[hoveredNode.type] || { label: hoveredNode.type, desc: 'Infrastructure component.' };
        const sysPart = SYSTEM_INFO_MAP[hoveredNode.type] || 'Standard Infrastructure Component';
        
        tooltip.style.display = 'block'; 
        tooltip.style.left = (lastMouseX + 20) + 'px'; 
        tooltip.style.top = (lastMouseY + 20) + 'px';
        
        tooltip.innerHTML = `
            <div class="tooltip-header">${info.label} <span class="sys-info-tag">SYSTEM_INFO</span></div>
            <div class="tooltip-row"><span class="tooltip-label">COORDINATES:</span><span class="tooltip-value">[${selectedTile.x}, ${selectedTile.y}]</span></div>
            <div class="tooltip-desc" style="color: #00ffff; font-weight: bold; margin-bottom: 5px;">${sysPart}</div>
            <div class="tooltip-desc">${info.desc || ''}</div>
        `;
    } else {
        tooltip.style.display = 'none';
    }
}

canvas.addEventListener('dragover', (e) => e.preventDefault());
canvas.addEventListener('drop', (e) => {
    e.preventDefault();
    const type = e.dataTransfer.getData('text/plain');
    if (BUILD_TYPES[type]) {
        const tile = fromIso(e.clientX, e.clientY);
        districts.push({ x: tile.x, y: tile.y, type: type, label: `${type}_Node` });
        addRenderLog(`GENESIS: Deployed ${type} at [${tile.x}, ${tile.y}]`);
    }
});

draw();
