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
let camX = 0, camY = 0, zoom = 0.8;
let isDragging = false, lastMouseX = 0, lastMouseY = 0;

const BUILD_TYPES = {
    'CPU': { color: '#ff4d4d', label: 'Silicon Central', locked: true, category: 'Hardware', desc: 'Central compute core.' },
    'RAM': { color: '#4dff88', label: 'Memory Matrix', locked: true, category: 'Hardware', desc: 'Volatile data pool.' },
    'GPU': { color: '#4d94ff', label: 'Graphics Grid', locked: true, category: 'Hardware', desc: 'Parallel math array.' },
    'SSD': { color: '#ffffff', label: 'NVMe SSD', locked: true, category: 'Hardware', desc: 'Persistent storage node.' },
    'NORTHBRIDGE': { color: '#00ffff', label: 'Northbridge', locked: true, category: 'Hardware', desc: 'High-speed system link.' },
    'SOUTHBRIDGE': { color: '#0055ff', label: 'Southbridge', locked: true, category: 'Hardware', desc: 'I/O peripheral hub.' },
    'REGISTRY': { color: '#ffff00', label: 'Registry Hive', locked: true, category: 'Logic', desc: 'System configuration keys.' },
    'MEM_CTRL': { color: '#aa00ff', label: 'Mem Controller', locked: true, category: 'Hardware', desc: 'Data retrieval unit.' },
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

function drawRenderFile() {
    ctx.save();
    ctx.fillStyle = 'rgba(0, 20, 0, 0.8)';
    ctx.fillRect(10, canvas.height - 220, 300, 200);
    ctx.strokeStyle = '#0f0'; ctx.lineWidth = 1;
    ctx.strokeRect(10, canvas.height - 220, 300, 200);
    
    ctx.fillStyle = '#0f0'; ctx.font = '10px Courier New';
    ctx.fillText("RENDER_FILE.SYS (Live Draw-Calls)", 20, canvas.height - 205);
    RENDER_LOG.forEach((line, i) => {
        ctx.fillText(line, 20, canvas.height - 185 + (i * 10));
    });
    ctx.restore();
}

const PROTOCOLS = {
    'TCP': { name: 'Walk', speed: 0.005, color: '#00ff00', desc: 'Reliable, ordered flow.' },
    'UDP': { name: 'Bike', speed: 0.02, color: '#ffff00', desc: 'Fast, lossy jitter flow.' },
    'BUS': { name: 'File Bus', speed: 0.01, color: '#ff00ff', desc: 'Bulk data transfer.' }
};

let packets = [];
function spawnPacket(fromX, fromY, toX, toY, color, protocol, speed) {
    packets.push({ x: fromX, y: fromY, tx: toX, ty: toY, p: 0, color, protocol, speed });
    addRenderLog(`SPAWN_PACKET: ${protocol} at [${fromX},${fromY}] -> [${toX},${toY}]`);
}

function toIso(x, y) {
    return { 
        isoX: (x - y) * (TILE_WIDTH / 2) * zoom + canvas.width / 2 + camX, 
        isoY: (x + y) * (TILE_HEIGHT / 2) * zoom + canvas.height / 2 + camY 
    };
}

function fromIso(isoX, isoY) {
    const screenX = (isoX - canvas.width / 2 - camX) / zoom;
    const screenY = (isoY - canvas.height / 2 - camY) / zoom;
    const x = (screenX / (TILE_WIDTH / 2) + screenY / (TILE_HEIGHT / 2)) / 2;
    const y = (screenY / (TILE_HEIGHT / 2) - screenX / (TILE_WIDTH / 2)) / 2;
    return { x: Math.floor(x), y: Math.floor(y) };
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

function drawTile(x, y, color = '#050a05', isHovered = false) {
    const { isoX, isoY } = toIso(x, y);
    const tw = TILE_WIDTH * zoom, th = TILE_HEIGHT * zoom;
    if (isoX < -tw || isoX > canvas.width + tw || isoY < -th || isoY > canvas.height + th) return;
    
    ctx.beginPath();
    ctx.moveTo(isoX, isoY); ctx.lineTo(isoX + tw / 2, isoY + th / 2);
    ctx.lineTo(isoX, isoY + th); ctx.lineTo(isoX - tw / 2, isoY + th / 2);
    ctx.closePath();
    ctx.fillStyle = isHovered ? '#102510' : color;
    ctx.fill();
    ctx.strokeStyle = '#001a00'; ctx.stroke();

    const d = districts.find(d => d.x === x && d.y === y);
    if (d) {
        let info = BUILD_TYPES[d.type] || { color: 'gray' };
        let finalColor = info.color;
        
        // Real-world Heat Tinting for CPU
        if (d.type === 'CPU') {
            const heat = window.systemHeat || 35;
            const r = Math.min(255, 100 + (heat * 1.5));
            finalColor = `rgb(${r}, 77, 77)`;
        }
        
        // SSD Swap Glow (Step 26 Option B)
        if (d.type === 'SSD' && window.isSwapping) {
            ctx.shadowBlur = 20; ctx.shadowColor = '#ffaa00';
            finalColor = '#ffaa00';
        }

        drawStructure(isoX, isoY + th/2, finalColor, d.type, info.locked);
        ctx.shadowBlur = 0;
        
        ctx.fillStyle = 'white'; ctx.font = `bold ${Math.max(10, 14*zoom)}px Arial`;
        ctx.fillText(d.label || d.type, isoX - 12*zoom, isoY - 20*zoom);
    }
}

let cryptoBalance = 0;
let lastCryptoTick = Date.now();

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const mouseTile = selectedTile;
    const freq = window.systemFrequency || 5.2;
    const speedMult = freq / 5.2;

    for (let x = -20; x < MAP_SIZE; x++) {
        for (let y = -20; y < MAP_SIZE; y++) {
            drawTile(x, y, '#050a05', (x === mouseTile.x && y === mouseTile.y));
        }
    }

    packets.forEach((pkt, i) => {
        // CAS Latency Gating (Step 26 Option A)
        const isMemPacket = pkt.tx === 3 && pkt.ty === 0; // RAM Target
        if (isMemPacket && pkt.p > 0.4 && pkt.p < 0.5) {
            const waitTime = window.casLatency || 32;
            pkt.wait = (pkt.wait || 0) + (1 * speedMult);
            if (pkt.wait < waitTime) return; // Hold packet at controller
        }

        pkt.p += (pkt.speed || 0.01) * speedMult;
        const curX = pkt.x + (pkt.tx - pkt.x) * pkt.p, curY = pkt.y + (pkt.ty - pkt.y) * pkt.p, pos = toIso(curX, curY);
        let finalX = pos.isoX, finalY = pos.isoY;
        if(pkt.protocol !== 'BUS') finalY -= Math.sin(pkt.p * Math.PI) * 60 * zoom;
        ctx.fillStyle = pkt.color; ctx.beginPath(); ctx.arc(finalX, finalY, 2*zoom, 0, Math.PI*2); ctx.fill();
        if(pkt.p >= 1) packets.splice(i, 1);
    });

    const hoveredNode = districts.find(d => d.x === selectedTile.x && d.y === selectedTile.y);
    if (hoveredNode) {
        const info = BUILD_TYPES[hoveredNode.type];
        tooltip.style.display = 'block'; tooltip.style.left = (lastMouseX + 20) + 'px'; tooltip.style.top = (lastMouseY + 20) + 'px';
        let specHtml = `<div class="tooltip-header">${info.label}</div>`;
        const specs = window.hardwareSpecs ? window.hardwareSpecs[hoveredNode.type] : null;
        if (specs) {
            for (const [key, value] of Object.entries(specs)) {
                if (typeof value === 'object') {
                    specHtml += `<div class="tooltip-row"><b>${key}:</b></div>`;
                    for(let [sk, sv] of Object.entries(value)) {
                        specHtml += `<div class="tooltip-row" style="padding-left:10px;"><span>${sk}:</span><span>${sv}</span></div>`;
                    }
                } else {
                    specHtml += `<div class="tooltip-row"><span>${key}:</span><span>${value}</span></div>`;
                }
            }
        }
        tooltip.innerHTML = specHtml;
    } else { tooltip.style.display = 'none'; }

    // Trajectories (Real Data Flow)
    const links = [
        { from: 'CPU', to: 'RAM', protocol: 'BUS' },
        { from: 'CPU', to: 'GPU', protocol: 'BUS' },
        { from: 'CPU', to: 'NORTHBRIDGE', protocol: 'BUS' },
        { from: 'NORTHBRIDGE', to: 'RAM', protocol: 'BUS' },
        { from: 'SOUTHBRIDGE', to: 'SSD', protocol: 'TCP' },
        { from: 'CPU', to: 'LLM', protocol: 'UDP' }
    ];
    links.forEach(l => {
        const from = districts.find(d => d.type === l.from), to = districts.find(d => d.type === l.to);
        if(from && to) {
            const p1 = toIso(from.x, from.y), p2 = toIso(to.x, to.y);
            const proto = PROTOCOLS[l.protocol] || PROTOCOLS['TCP'];
            ctx.strokeStyle = proto.color + "22"; ctx.lineWidth = 1;
            ctx.beginPath(); ctx.moveTo(p1.isoX, p1.isoY); 
            ctx.quadraticCurveTo((p1.isoX+p2.isoX)/2, (p1.isoY+p2.isoY)/2 - 50*zoom, p2.isoX, p2.isoY);
            ctx.stroke();
            if(Math.random() < 0.02 * speedMult) spawnPacket(from.x, from.y, to.x, to.y, proto.color, l.protocol, proto.speed);
        }
    });

    drawRenderFile();
    requestAnimationFrame(draw);
}

canvas.addEventListener('dragover', (e) => e.preventDefault());
canvas.addEventListener('drop', (e) => {
    e.preventDefault();
    const type = e.dataTransfer.getData('text/plain');
    if (BUILD_TYPES[type]) {
        const rect = canvas.getBoundingClientRect();
        const tile = fromIso(e.clientX - rect.left, e.clientY - rect.top);
        districts.push({ x: tile.x, y: tile.y, type: type, label: `${type}_Node` });
        addRenderLog(`GENESIS: Deployed ${type} at [${tile.x}, ${tile.y}]`);
    }
});

const paletteButtons = document.querySelectorAll('.tool-btn');
paletteButtons.forEach(btn => {
    btn.addEventListener('dragstart', (e) => e.dataTransfer.setData('text/plain', btn.getAttribute('data-type')));
});

canvas.addEventListener('mousemove', (e) => {
    lastMouseX = e.clientX; lastMouseY = e.clientY;
    const rect = canvas.getBoundingClientRect();
    selectedTile = fromIso(e.clientX - rect.left, e.clientY - rect.top);
});

draw();
