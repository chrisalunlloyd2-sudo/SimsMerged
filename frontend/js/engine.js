const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const tooltip = document.getElementById('hover-tooltip');

function resize() {
    const parent = canvas.parentElement;
    canvas.width = parent.clientWidth || window.innerWidth - 280;
    canvas.height = parent.clientHeight || window.innerHeight;
}
window.addEventListener('resize', resize);
resize();

const TILE_WIDTH = 64, TILE_HEIGHT = 32, MAP_SIZE = 40;
let selectedTile = { x: 0, y: 0 };
window.agents = window.agents || [];
let currentBuildType = 'VSCODE', contextMenu = null;
let camX = 0, camY = 0, zoom = 0.8;
let isDragging = false, lastMouseX = 0, lastMouseY = 0;

// Generated Urban Decorations (Logic Trees)
const decorations = [];
for(let i=0; i<100; i++) {
    decorations.push({
        x: Math.floor(Math.random() * MAP_SIZE * 2 - MAP_SIZE),
        y: Math.floor(Math.random() * MAP_SIZE * 2 - MAP_SIZE),
        type: Math.random() > 0.5 ? 'tree' : 'lamp'
    });
}

const BUILD_TYPES = {
    'CPU': { color: '#ff4d4d', label: 'Silicon Central', locked: true, category: 'Hardware', desc: 'Central compute core.' },
    'RAM': { color: '#4dff88', label: 'Memory Matrix', locked: true, category: 'Hardware', desc: 'Volatile data pool.' },
    'GPU': { color: '#4d94ff', label: 'Graphics Grid', locked: true, category: 'Hardware', desc: 'Parallel math array.' },
    'SSD': { color: '#ffffff', label: 'Storage Hive', locked: true, category: 'Hardware', desc: 'Persistent storage node.' },
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
    { x: 10, y: 10, type: 'MODEM', settings: {ip: '192.168.1.1'} },
    { x: 5, y: 5, type: 'LLM', label: 'Intelligence' },
    { x: 7, y: 5, type: 'PLANT', label: 'Fabricator' },
    { x: -5, y: 5, type: 'HOSPITAL', label: 'Healing_Node' }
];

const PROTOCOLS = {
    'TCP': { name: 'Walk', speed: 0.005, color: '#00ff00', desc: 'Reliable, ordered flow.' },
    'UDP': { name: 'Bike', speed: 0.02, color: '#ffff00', desc: 'Fast, lossy jitter flow.' },
    'BUS': { name: 'File Bus', speed: 0.01, color: '#ff00ff', desc: 'Bulk data transfer.' }
};

let packets = [];
function spawnPacket(fromX, fromY, toX, toY, color, protocol, speed) {
    packets.push({ x: fromX, y: fromY, tx: toX, ty: toY, p: 0, color, protocol, speed });
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

    // Front face
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.moveTo(isoX - bSize, isoY);
    ctx.lineTo(isoX, isoY + bSize/2);
    ctx.lineTo(isoX, isoY + bSize/2 - h);
    ctx.lineTo(isoX - bSize, isoY - h);
    ctx.closePath(); ctx.fill();
    
    // Side face
    ctx.fillStyle = ctx.fillStyle.replace(')', ', 0.7)').replace('rgb', 'rgba');
    ctx.beginPath();
    ctx.moveTo(isoX, isoY + bSize/2);
    ctx.lineTo(isoX + bSize, isoY);
    ctx.lineTo(isoX + bSize, isoY - h);
    ctx.lineTo(isoX, isoY + bSize/2 - h);
    ctx.closePath(); ctx.fill();

    // Top face
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.moveTo(isoX, isoY - h);
    ctx.lineTo(isoX + bSize, isoY - bSize/2 - h);
    ctx.lineTo(isoX, isoY - bSize - h);
    ctx.lineTo(isoX - bSize, isoY - bSize/2 - h);
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

    if (x % 5 === 0 || y % 5 === 0) {
        ctx.strokeStyle = 'rgba(0, 255, 255, 0.05)';
        ctx.stroke();
    }

    drawDistricts(x, y, isoX, isoY, th);
}

function drawDistricts(x, y, isoX, isoY, th) {
    const d = districts.find(d => d.x === x && d.y === y);
    if (d) {
        const info = BUILD_TYPES[d.type] || { color: 'gray' };
        drawStructure(isoX, isoY + th/2, info.color, d.type, info.locked);
        
        const bSize = 16 * zoom;
        const h = (info.locked ? 10 : 32) * zoom;
        if(!info.locked && info.category !== 'Env') {
            ctx.fillStyle = "rgba(0, 255, 255, 0.3)";
            for(let i=0; i<3; i++) {
                for(let j=0; j<2; j++) {
                    ctx.fillRect(isoX - bSize + 5*zoom + j*7*zoom, isoY + th/2 - h + 5*zoom + i*8*zoom, 2*zoom, 2*zoom);
                }
            }
        }

        ctx.fillStyle = 'white'; ctx.font = `bold ${Math.max(10, Math.floor(14*zoom))}px Arial`;
        ctx.fillText(d.label || d.type, isoX - 12*zoom, isoY - 20*zoom);
    }
}

function drawTrajectories() {
    const links = window.activeLinks || [
        { from: 'CPU', to: 'RAM', protocol: 'BUS' },
        { from: 'CPU', to: 'GPU', protocol: 'BUS' },
        { from: 'CPU', to: 'MODEM', protocol: 'TCP' },
        { from: 'CPU', to: 'LLM', protocol: 'TCP' }
    ];

    links.forEach(l => {
        const from = districts.find(d => d.type === l.from), to = districts.find(d => d.type === l.to);
        if(from && to) {
            const p1 = toIso(from.x, from.y), p2 = toIso(to.x, to.y);
            const proto = PROTOCOLS[l.protocol] || PROTOCOLS['TCP'];
            
            ctx.setLineDash(l.protocol === 'BUS' ? [] : [10, 5]);
            ctx.strokeStyle = proto.color + "44"; ctx.lineWidth = 1;
            ctx.beginPath(); ctx.moveTo(p1.isoX, p1.isoY); 
            ctx.quadraticCurveTo((p1.isoX+p2.isoX)/2, (p1.isoY+p2.isoY)/2 - 50*zoom, p2.isoX, p2.isoY);
            ctx.stroke();
            
            if(Math.random() < 0.03) {
                spawnPacket(from.x, from.y, to.x, to.y, proto.color, l.protocol, proto.speed);
            }
        }
    });
}

function drawBindingChains() {
    window.agents.forEach(agent => {
        if (agent.state === 'DEPRESSED' || agent.emotional_state === 'DEPRESSED') {
            const hospital = districts.find(d => d.type === 'HOSPITAL');
            if (hospital) {
                const p1 = toIso(agent.x, agent.y);
                const p2 = toIso(hospital.x, hospital.y);
                ctx.strokeStyle = '#ff00ff';
                ctx.lineWidth = 4;
                ctx.setLineDash([5, 5]);
                ctx.beginPath();
                ctx.moveTo(p1.isoX, p1.isoY);
                ctx.lineTo(p2.isoX, p2.isoY);
                ctx.stroke();
                ctx.setLineDash([]);
            }
        }
    });
}

function drawThermalMonitor() {
    const temp = 35 + (window.agents.length * 2) + (Math.sin(Date.now() / 1000) * 2);
    ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
    ctx.fillRect(10, 10, 180, 40);
    ctx.strokeStyle = temp > 60 ? '#ff0000' : '#00ff00';
    ctx.lineWidth = 2;
    ctx.strokeRect(10, 10, 180, 40);
    
    ctx.fillStyle = '#fff';
    ctx.font = '12px Courier New';
    ctx.fillText(`SYSTEM_TEMPERATURE: ${temp.toFixed(2)}Â°C`, 20, 25);
    ctx.fillText(`ACTIVE_KERNELS: ${window.agents.length}`, 20, 40);
}

function drawHolograms() {
    districts.forEach(d => {
        if (d.type === 'CPU' || d.type === 'RAM') {
            const { isoX, isoY } = toIso(d.x, d.y);
            const th = TILE_HEIGHT * zoom;
            const time = Date.now() / 1000;
            const pulse = Math.sin(time * 5) * 0.5 + 0.5;
            
            ctx.save();
            ctx.translate(isoX, isoY + th/2 - 45 * zoom);
            
            ctx.strokeStyle = `rgba(0, 255, 255, ${0.2 + pulse * 0.3})`;
            ctx.lineWidth = 2;
            const size = 8 * zoom;
            
            ctx.beginPath();
            ctx.moveTo(0, -size); ctx.lineTo(size, -size/2); ctx.lineTo(0, 0); ctx.lineTo(-size, -size/2); ctx.closePath();
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(0, 0); ctx.lineTo(0, size); ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(size, -size/2); ctx.lineTo(size, size - size/2); ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(-size, -size/2); ctx.lineTo(-size, size - size/2); ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(0, size); ctx.lineTo(size, size - size/2); ctx.lineTo(0, size + size); ctx.lineTo(-size, size - size/2); ctx.closePath();
            ctx.stroke();

            ctx.beginPath();
            ctx.ellipse(0, size/2, (15 + pulse * 20) * zoom, (7 + pulse * 10) * zoom, 0, 0, Math.PI * 2);
            ctx.strokeStyle = `rgba(0, 255, 255, ${0.5 - pulse * 0.5})`;
            ctx.stroke();
            
            ctx.restore();
        }
    });
}

let cryptoBalance = 0;
let lastCryptoTick = Date.now();

function drawCryptoSprites() {
    let mintRate = 0;
    
    districts.forEach(d => {
        if (d.type === 'BANK') {
            let baseMint = parseFloat(d.settings?.sprite_mint || 500);
            let gas = parseFloat(d.settings?.gas_fee || 0.01);
            let burn = parseFloat(d.settings?.burn_rate || 1.5) / 100.0;
            
            let netYield = baseMint - (baseMint * gas) - (baseMint * burn);
            mintRate += netYield;

            const { isoX, isoY } = toIso(d.x, d.y);
            const time = Date.now() / 1000;
            const bounce = Math.sin(time * 3) * 10 * zoom;
            
            ctx.save();
            ctx.translate(isoX, isoY - 40 * zoom - bounce);
            
            ctx.shadowBlur = 15;
            ctx.shadowColor = '#ffd700';
            ctx.fillStyle = '#ffd700';
            ctx.beginPath();
            ctx.ellipse(0, 0, 10 * zoom, 15 * zoom, 0, 0, Math.PI * 2);
            ctx.fill();
            
            ctx.shadowBlur = 0;
            ctx.strokeStyle = '#cca300';
            ctx.lineWidth = 2 * zoom;
            ctx.beginPath();
            ctx.ellipse(0, 0, 6 * zoom, 10 * zoom, 0, 0, Math.PI * 2);
            ctx.stroke();
            
            ctx.fillStyle = '#fff';
            ctx.font = old \px Arial;
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText('S', 0, 0);
            
            ctx.restore();
        }
    });
    
    const now = Date.now();
    const dt = (now - lastCryptoTick) / 1000.0;
    lastCryptoTick = now;
    
    if (mintRate > 0) {
        cryptoBalance += mintRate * dt;
        const rateEl = document.getElementById('mint-rate');
        const balEl = document.getElementById('crypto-balance');
        if (rateEl) rateEl.innerText = mintRate.toFixed(2) + ' SPRITE/s';
        if (balEl) balEl.innerText = cryptoBalance.toFixed(2);
    }
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const mouseTile = selectedTile;
    
    for (let x = -20; x < MAP_SIZE; x++) {
        for (let y = -20; y < MAP_SIZE; y++) {
            drawTile(x, y, '#050a05', (x === mouseTile.x && y === mouseTile.y));
        }
    }

    drawTrajectories();
    drawBindingChains();
    drawThermalMonitor();
    drawHolograms();
    drawCryptoSprites();

    // 6. Sprite AI Sentience & MSN Chatter
    const now = Date.now();
    if (!window.lastMsnTick || now - window.lastMsnTick > 5000) {
        window.lastMsnTick = now;
        const agent = window.agents[Math.floor(Math.random() * window.agents.length)];
        if (agent) {
            const msgs = [
                `Synchronizing DePIN node at [${agent.x}, ${agent.y}]`,
                `SHA256 Hash Verified: 0x${Math.random().toString(16).slice(2, 10)}...`,
                `H2O-Danube optimization cycle complete. Stability: ${window.systemStability}`,
                `Dual-Watchdog active. No memory leaks detected.`,
                `Routing packets via ${Object.keys(PROTOCOLS)[Math.floor(Math.random()*3)]} protocol.`,
                `Prime Directive: Heal and Automate sectors.`,
                `Recording automation script for coordinate ${Math.floor(agent.x)},${Math.floor(agent.y)}`
            ];
            if (window.msnChat) window.msnChat(agent.name || 'AGENT_CORE', msgs[Math.floor(Math.random() * msgs.length)]);
            
            // Clipboard Ability (Simulated)
            if (Math.random() < 0.1 && agent.settings?.clipboard) {
                const state = `SIM_STATE: ${agent.name} at ${agent.x},${agent.y} | STATUS: ${agent.state}`;
                navigator.clipboard.writeText(state).catch(() => {});
                window.logToConsole(`AGENT_EVENT: ${agent.name} copied state to clipboard.`);
            }
        }
    }

    packets.forEach((pkt, i) => {
        pkt.p += pkt.speed || 0.01;
        const curX = pkt.x + (pkt.tx - pkt.x) * pkt.p, curY = pkt.y + (pkt.ty - pkt.y) * pkt.p, pos = toIso(curX, curY);
        let finalX = pos.isoX, finalY = pos.isoY;
        if(pkt.protocol !== 'BUS') finalY -= Math.sin(pkt.p * Math.PI) * 60 * zoom;
        ctx.fillStyle = pkt.color; ctx.shadowBlur = 10; ctx.shadowColor = pkt.color;
        ctx.beginPath(); ctx.arc(finalX, finalY, 2*zoom, 0, Math.PI*2); ctx.fill();
        ctx.shadowBlur = 0;
        if(pkt.p >= 1) packets.splice(i, 1);
    });

    const hoveredNode = districts.find(d => d.x === selectedTile.x && d.y === selectedTile.y);
    if (hoveredNode) {
        const info = BUILD_TYPES[hoveredNode.type];
        tooltip.style.display = 'block'; tooltip.style.left = (lastMouseX + 20) + 'px'; tooltip.style.top = (lastMouseY + 20) + 'px';
        
        let specHtml = `<div class="tooltip-header">${info.label}</div><div class="tooltip-desc">${info.desc}</div>`;
        
        // Exhaustive Hardware Data Injection
        const specs = window.hardwareSpecs ? window.hardwareSpecs[hoveredNode.type] : null;
        if (specs) {
            specHtml += `<div style="margin-top:10px; border-top:1px solid #005555; padding-top:5px; font-size:10px;">`;
            for (const [key, value] of Object.entries(specs)) {
                if (typeof value === 'object') {
                    specHtml += `<div class="tooltip-row"><span class="tooltip-label">${key.toUpperCase()}:</span></div>`;
                    for (const [subKey, subVal] of Object.entries(value)) {
                        specHtml += `<div class="tooltip-row" style="padding-left:10px;"><span class="tooltip-label">${subKey}:</span><span class="tooltip-value">${subVal}</span></div>`;
                    }
                } else {
                    specHtml += `<div class="tooltip-row"><span class="tooltip-label">${key.toUpperCase()}:</span><span class="tooltip-value">${value}</span></div>`;
                }
            }
            specHtml += `</div>`;
        }
        
        tooltip.innerHTML = specHtml;
    } else { tooltip.style.display = 'none'; }

    window.agents.forEach(agent => {
        const pos = toIso(agent.x, agent.y);
        ctx.fillStyle = agent.role === 'ADMIN' ? '#fff' : '#0ff';
        ctx.beginPath(); ctx.arc(pos.isoX, pos.isoY, 4*zoom, 0, Math.PI * 2); ctx.fill();
        ctx.strokeStyle = 'white'; ctx.stroke();
    });

    requestAnimationFrame(draw);
}

// 7. Drag-and-Drop Genesis Engine
canvas.addEventListener('dragover', (e) => e.preventDefault());
canvas.addEventListener('drop', (e) => {
    e.preventDefault();
    const type = e.dataTransfer.getData('text/plain');
    if (BUILD_TYPES[type]) {
        const rect = canvas.getBoundingClientRect();
        const tile = fromIso(e.clientX - rect.left, e.clientY - rect.top);
        
        const existing = districts.find(d => d.x === tile.x && d.y === tile.y);
        if (existing && BUILD_TYPES[existing.type].locked) return;
        
        districts = districts.filter(d => d.x !== tile.x || d.y !== tile.y);
        districts.push({ 
            x: tile.x, y: tile.y, type: type, 
            label: `${type}_Node_${Math.floor(Math.random()*1000)}`,
            settings: JSON.parse(JSON.stringify(window.currentSettings || {})) 
        });
        
        window.logToConsole(`GENESIS_EVENT: Deployed ${type} at [${tile.x}, ${tile.y}]`);
        if (window.msnChat) window.msnChat('SYSTEM', `New DePIN node ${type} initialized with SHA256: 0x${Math.random().toString(16).slice(2, 10)}`);
    }
});

const paletteButtons = document.querySelectorAll('.tool-btn');
paletteButtons.forEach(btn => {
    btn.addEventListener('dragstart', (e) => {
        e.dataTransfer.setData('text/plain', btn.getAttribute('data-type'));
    });
});

window.setBuildType = function(type) { currentBuildType = type; };
canvas.addEventListener('wheel', (e) => { e.preventDefault(); if(e.deltaY < 0) zoom *= 1.1; else zoom /= 1.1; zoom = Math.min(Math.max(0.1, zoom), 5); });
canvas.addEventListener('mousedown', (e) => {
    if(e.button === 1 || (e.button === 0 && e.shiftKey)) { isDragging = true; lastMouseX = e.clientX; lastMouseY = e.clientY; }
    else if(e.button === 0) {
        const target = districts.find(d => d.x === selectedTile.x && d.y === selectedTile.y);
        if (target && BUILD_TYPES[target.type].locked) return;
        districts = districts.filter(d => d.x !== selectedTile.x || d.y !== selectedTile.y);
        districts.push({ x: selectedTile.x, y: selectedTile.y, type: currentBuildType, settings: JSON.parse(JSON.stringify(window.currentSettings || {})) });
    }
});
window.addEventListener('mousemove', (e) => {
    lastMouseX = e.clientX; lastMouseY = e.clientY;
    if(isDragging) { camX += (e.clientX - lastMouseX); camY += (e.clientY - lastMouseY); }
    const rect = canvas.getBoundingClientRect(); selectedTile = fromIso(e.clientX - rect.left, e.clientY - rect.top);
});
window.addEventListener('mouseup', () => { isDragging = false; });

const legendContent = document.getElementById('legend-content');
if (legendContent) {
    legendContent.innerHTML = '';
    Object.entries(BUILD_TYPES).forEach(([key, info]) => {
        const item = document.createElement('div');
        item.className = 'legend-item';
        item.innerHTML = `<div class="legend-color" style="background: ${info.color}"></div><span>${info.label}</span>`;
        legendContent.appendChild(item);
    });
}

window.agents = [ { x: 0, y: 0, name: 'ADMIN_ROOT', role: 'ADMIN' } ];
draw();



