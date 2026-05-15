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
let agents = [], selectedTile = { x: 0, y: 0 };
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
    'CPU': { color: '#ff4d4d', label: 'CPU Cluster', locked: true, category: 'Hardware', desc: 'The silicon central processing unit. Executes all high-level arithmetic and logic operations.' },
    'RAM': { color: '#4dff88', label: 'RAM Banks', locked: true, category: 'Hardware', desc: 'Volatile memory pool for high-speed data buffering.' },
    'GPU': { color: '#4d94ff', label: 'GPU Core', locked: true, category: 'Hardware', desc: 'Handles parallel matrix math and graphical environment rendering.' },
    'SSD': { color: '#ffffff', label: 'NVMe SSD', locked: true, category: 'Hardware', desc: 'High-speed persistent storage for system binaries.' },
    'MODEM': { color: '#ff007f', label: 'Modem/Gateway', locked: true, category: 'Network', desc: 'Interface to the external web protocols.' },
    'VSCODE': { color: '#007acc', label: 'VS Code', category: 'Dev', desc: 'Development environment for kernel scripting.' },
    'LLM': { color: '#00ffff', label: 'LLM Node', category: 'Software', desc: 'Intelligence compute cluster.' },
    'VDB': { color: '#ff00ff', label: 'Vector DB', category: 'Software', desc: 'High-dimensional memory indexing.' },
    'HOSPITAL': { color: '#ff4444', label: 'Sanctuary', category: 'Urban', desc: 'Healing hub for depressed kernels.' },
    'PLANT': { color: '#ffaa00', label: 'Sprite Plant', category: 'Industrial', desc: 'Manufacturing node for automation swarm units.' }
};

let districts = [
    { x: 0, y: 0, type: 'CPU', label: 'Silicon_Main', settings: {cores: 8, mult: 16} },
    { x: 1, y: 0, type: 'RAM', label: 'Mem_Pool', settings: {cap: '16GB'} },
    { x: -1, y: 0, type: 'GPU', label: 'Graphics_Bus', settings: {vram: '8GB'} },
    { x: 10, y: 10, type: 'MODEM', settings: {ip: '192.168.1.1'} },
    { x: 5, y: 5, type: 'LLM', label: 'Intelligence' },
    { x: 7, y: 5, type: 'PLANT', label: 'Fabricator' },
    { x: -5, y: 5, type: 'HOSPITAL', label: 'Healing_Node' }
];

let packets = [];
function spawnPacket(fromX, fromY, toX, toY, color, protocol) {
    packets.push({ x: fromX, y: fromY, tx: toX, ty: toY, p: 0, color, protocol });
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
    const bSize = 16 * zoom; // Increased from 12
    const h = (locked ? 10 : 32) * zoom; // Increased from 8/25
    
    // Front face
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.moveTo(isoX - bSize, isoY);
    ctx.lineTo(isoX, isoY + bSize/2);
    ctx.lineTo(isoX, isoY + bSize/2 - h);
    ctx.lineTo(isoX - bSize, isoY - h);
    ctx.closePath(); ctx.fill();
    
    // Side face
    ctx.fillStyle = ctx.fillStyle.replace(')', ', 0.7)').replace('rgb', 'rgba'); // Darken
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
    ctx.strokeStyle = '#fff'; ctx.lineWidth = 1.0; ctx.stroke();
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

    // Roads (visual only)
    if (x % 5 === 0 || y % 5 === 0) {
        ctx.strokeStyle = 'rgba(0, 255, 255, 0.05)';
        ctx.stroke();
    }

    // Draw Decorations
    const deco = decorations.find(d => d.x === x && d.y === y);
    if (deco && !districts.find(d => d.x === x && d.y === y)) {
        ctx.fillStyle = deco.type === 'tree' ? '#0a3d0a' : '#222';
        ctx.beginPath(); ctx.arc(isoX, isoY + th/2, 3*zoom, 0, Math.PI*2); ctx.fill();
        if(deco.type === 'lamp') { ctx.shadowBlur = 10; ctx.shadowColor = '#0ff'; ctx.fillStyle = '#0ff'; ctx.fillRect(isoX-1, isoY, 2, -12*zoom); ctx.shadowBlur = 0; }
    }

    const d = districts.find(d => d.x === x && d.y === y);
    if (d) {
        const info = BUILD_TYPES[d.type] || { color: 'gray' };
        drawStructure(isoX, isoY + th/2, info.color, d.type, info.locked);
        ctx.fillStyle = 'white'; ctx.font = `bold ${Math.max(10, Math.floor(14*zoom))}px Arial`;
        ctx.fillText(d.label || d.type, isoX - 12*zoom, isoY - 20*zoom);
    }
}

function render() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const mouseTile = selectedTile;
    
    // Draw Grid
    for (let x = -20; x < MAP_SIZE; x++) {
        for (let y = -20; y < MAP_SIZE; y++) {
            drawTile(x, y, '#050a05', (x === mouseTile.x && y === mouseTile.y));
        }
    }

    // Protocol Pipes
    const links = [
        { f: 'CPU', t: 'RAM', protocol: 'BUS', c: '#00ff00' },
        { f: 'CPU', t: 'GPU', protocol: 'BUS', c: '#ff00ff' },
        { f: 'CPU', t: 'MODEM', protocol: 'TCP/IP', c: '#00ffff' },
        { f: 'CPU', t: 'LLM', protocol: 'BUS', c: '#00ffff' }
    ];

    links.forEach(l => {
        const from = districts.find(d => d.type === l.f), to = districts.find(d => d.type === l.t);
        if(from && to) {
            const p1 = toIso(from.x, from.y), p2 = toIso(to.x, to.y);
            ctx.setLineDash(l.protocol === 'BUS' ? [] : [10, 5]);
            ctx.strokeStyle = l.c + "22"; ctx.lineWidth = l.protocol === 'BUS' ? 1 : 3;
            ctx.beginPath(); ctx.moveTo(p1.isoX, p1.isoY); 
            if(l.protocol === 'BUS') ctx.lineTo(p2.isoX, p2.isoY);
            else ctx.quadraticCurveTo((p1.isoX+p2.isoX)/2, (p1.isoY+p2.isoY)/2 - 100*zoom, p2.isoX, p2.isoY);
            ctx.stroke();
            if(Math.random() < 0.02) spawnPacket(from.x, from.y, to.x, to.y, l.c, l.protocol);
        }
    });

    packets.forEach((pkt, i) => {
        pkt.p += 0.01;
        const curX = pkt.x + (pkt.tx - pkt.x) * pkt.p, curY = pkt.y + (pkt.ty - pkt.y) * pkt.p, pos = toIso(curX, curY);
        let finalX = pos.isoX, finalY = pos.isoY;
        if(pkt.protocol !== 'BUS') finalY -= Math.sin(pkt.p * Math.PI) * 60 * zoom;
        ctx.fillStyle = pkt.color; ctx.shadowBlur = 10; ctx.shadowColor = pkt.color;
        ctx.beginPath(); ctx.arc(finalX, finalY, 2*zoom, 0, Math.PI*2); ctx.fill();
        ctx.shadowBlur = 0;
        if(pkt.p >= 1) packets.splice(i, 1);
    });

    // Hover Tooltip
    const hoveredNode = districts.find(d => d.x === selectedTile.x && d.y === selectedTile.y);
    if (hoveredNode) {
        const info = BUILD_TYPES[hoveredNode.type];
        tooltip.style.display = 'block'; tooltip.style.left = (lastMouseX + 20) + 'px'; tooltip.style.top = (lastMouseY + 20) + 'px';
        tooltip.innerHTML = `<div class="tooltip-header">${info.label}</div><div class="tooltip-desc">${info.desc}</div>`;
    } else { tooltip.style.display = 'none'; }

    agents.forEach(agent => {
        const pos = toIso(agent.x, agent.y);
        ctx.fillStyle = agent.role === 'ADMIN' ? '#fff' : '#0ff';
        ctx.beginPath(); ctx.arc(pos.isoX, pos.isoY, 4*zoom, 0, Math.PI * 2); ctx.fill();
        ctx.strokeStyle = 'white'; ctx.stroke();
    });

    requestAnimationFrame(render);
}

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

agents = [ { x: 0, y: 0, name: 'ADMIN_ROOT', role: 'ADMIN' } ];
render();
