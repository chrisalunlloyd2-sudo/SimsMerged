// TIMESTAMP: 2026-05-25T01:10:00.123Z
// PROJECT_ID: SimsMerged-v1.3
// AGENT_ID: Antigravity-Agent

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
    'ROAD': { color: '#222', label: 'Protocol Path', category: 'Network', desc: 'Static dataflow trajectory.' }
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
    const { isoX, isoY } = toIso(x, y);
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
                    if (Math.random() < 0.05) {
                        spawnPacket(fNode.x, fNode.y, tNode.x, tNode.y, link.color, link.protocol, link.speed || 0.02);
                    }
                });
            });
        }
    });
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Build spatial map for O(1) rendering lookups
    const districtMap = {};
    const typeMap = {};
    districts.forEach(d => {
        districtMap[`${d.x},${d.y}`] = d;
        if (!typeMap[d.type]) typeMap[d.type] = [];
        typeMap[d.type].push(d);
    });
    
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

    window.agents.forEach(agent => {
        const { isoX, isoY } = toIso(agent.x, agent.y);
        const margin = 60 * zoom;
        // Viewport Culling: Skip drawing agents scrolled off-screen
        if (isoX < -margin || isoX > canvas.width + margin || isoY < -margin || isoY > canvas.height + margin) return;

        const color = agent.role === 'DOCTOR' ? '#ff4444' : (agent.role === 'TEACHER' ? '#4facfe' : '#ffcc00');
        
        // --- DRAW SSPRITE (Animated Agent) ---
        const bob = Math.sin(Date.now() * 0.005) * 5 * zoom;
        const baseSize = 8 * zoom;
        
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
    });

    apply_interaction_logic();
    requestAnimationFrame(draw);
}

function apply_interaction_logic() {
    const hoveredNode = districts.find(d => d.x === selectedTile.x && d.y === selectedTile.y);
    const hoveredAgent = window.agents.find(a => a.x === selectedTile.x && a.y === selectedTile.y);

    if (hoveredNode || hoveredAgent) {
        const info = hoveredNode ? BUILD_TYPES[hoveredNode.type] : { label: hoveredAgent.name, desc: `Role: ${hoveredAgent.role}` };
        const sysPart = hoveredNode ? (SYSTEM_INFO_MAP[hoveredNode.type] || 'Standard Infrastructure Component') : SYSTEM_INFO_MAP['AGENT'];
        
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
