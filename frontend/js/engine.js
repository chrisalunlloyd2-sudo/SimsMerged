const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

function resize() {
    const parent = canvas.parentElement;
    canvas.width = parent.clientWidth;
    canvas.height = parent.clientHeight;
}
window.addEventListener('resize', resize);
resize();

const TILE_WIDTH = 64, TILE_HEIGHT = 32, MAP_SIZE = 30;
let agents = [], pulseStatus = "CONNECTING...", selectedTile = { x: 0, y: 0 };
let currentBuildType = 'CPU', contextMenu = null;
let camX = 0, camY = 0, zoom = 1.0, isDragging = false, lastMouseX = 0, lastMouseY = 0;

const BUILD_TYPES = {
    'BIOS': { color: '#0000ff', label: 'BIOS/UEFI', suite: [{ id: 'sec', label: 'SecureBoot', value: true }] },
    'BOOT': { color: '#ffff00', label: 'Boot Sector', suite: [{ id: 'mbr', label: 'MBR Mode', value: false }] },
    'CPU': { color: '#ff4d4d', label: 'CPU Core', suite: [{ id: 'mult', label: 'Multiplier', value: 16 }] },
    'RAM': { color: '#4dff88', label: 'RAM Module', suite: [{ id: 'lat', label: 'Latency', value: 16 }] },
    'GPU': { color: '#4d94ff', label: 'GPU Accelerator', suite: [{ id: 'clk', label: 'Clock', value: 1800 }] },
    'HDD': { color: '#e6e600', label: 'Storage Drive' },
    'PSU': { color: '#ffffff', label: 'Power Supply' },
    'REG': { color: '#ff00ff', label: 'Registry Hive' },
    'SYS': { color: '#c0c0c0', label: 'System32' },
    'PROG': { color: '#ffa500', label: 'Application' },
    'DSK': { color: '#00ffff', label: 'Desktop Shell' },
    'ROUT': { color: '#ff007f', label: 'Router' },
    'WEB': { color: '#00ccff', label: 'Internet Hub' },
    'SRV': { color: '#7f00ff', label: 'Remote Server' }
};

let districts = [
    { x: -5, y: -5, type: 'BIOS', settings: {sec: true} }, { x: -4, y: -5, type: 'BOOT', settings: {mbr: false} },
    { x: 0, y: 0, type: 'PSU', settings: {} }, { x: 1, y: 1, type: 'CPU', settings: {mult: 16} },
    { x: 2, y: 2, type: 'RAM', settings: {lat: 16} }, { x: 3, y: 1, type: 'GPU', settings: {clk: 1800} },
    { x: -2, y: 2, type: 'HDD', settings: {} }, { x: 0, y: 5, type: 'REG', settings: {} },
    { x: 2, y: 5, type: 'SYS', settings: {} }, { x: 5, y: 5, type: 'PROG', label: 'Explorer', settings: {} },
    { x: 8, y: 8, type: 'DSK', settings: {} }, { x: 12, y: 12, type: 'ROUT', settings: {} },
    { x: 15, y: 15, type: 'WEB', settings: {} }, { x: 18, y: 18, type: 'SRV', settings: {} }
];

const legendContent = document.getElementById('legend-content');
if (legendContent) {
    Object.entries(BUILD_TYPES).forEach(([key, info]) => {
        const item = document.createElement('div');
        item.className = 'legend-item';
        item.innerHTML = `<div class="legend-color" style="background: ${info.color}"></div><span>${info.label}</span>`;
        legendContent.appendChild(item);
    });
}

let packets = [];
function spawnPacket(fromX, fromY, toX, toY, color) {
    packets.push({ x: fromX, y: fromY, tx: toX, ty: toY, p: 0, color: color });
}

function toIso(x, y) {
    return { 
        isoX: (x - y) * (TILE_WIDTH / 2) * zoom + canvas.width / 2 + camX, 
        isoY: (x + y) * (TILE_HEIGHT / 2) * zoom + canvas.height / 4 + camY 
    };
}

function fromIso(isoX, isoY) {
    const screenX = (isoX - canvas.width / 2 - camX) / zoom;
    const screenY = (isoY - canvas.height / 4 - camY) / zoom;
    const x = (screenX / (TILE_WIDTH / 2) + screenY / (TILE_HEIGHT / 2)) / 2;
    const y = (screenY / (TILE_HEIGHT / 2) - screenX / (TILE_WIDTH / 2)) / 2;
    return { x: Math.floor(x), y: Math.floor(y) };
}

function drawTile(x, y, color = '#0a1a0a', isHovered = false) {
    const { isoX, isoY } = toIso(x, y);
    const tw = TILE_WIDTH * zoom, th = TILE_HEIGHT * zoom;
    ctx.beginPath(); ctx.moveTo(isoX, isoY); ctx.lineTo(isoX + tw / 2, isoY + th / 2); ctx.lineTo(isoX, isoY + th); ctx.lineTo(isoX - tw / 2, isoY + th / 2); ctx.closePath();
    ctx.fillStyle = isHovered ? '#1a3a1a' : color; ctx.fill(); ctx.strokeStyle = '#003300'; ctx.stroke();
    const d = districts.find(d => d.x === x && d.y === y);
    if (d) {
        const info = BUILD_TYPES[d.type]; ctx.fillStyle = info.color; const bSize = 12 * zoom;
        ctx.beginPath(); ctx.moveTo(isoX, isoY - bSize); ctx.lineTo(isoX + bSize, isoY); ctx.lineTo(isoX, isoY + bSize); ctx.lineTo(isoX - bSize, isoY); ctx.closePath(); ctx.fill(); ctx.strokeStyle = '#fff'; ctx.stroke();
        ctx.fillStyle = 'white'; ctx.font = `bold ${Math.max(8, Math.floor(10*zoom))}px Arial`; ctx.fillText(d.label || d.type, isoX - 10*zoom, isoY - 15*zoom);
    }
}

function render() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let x = -10; x < MAP_SIZE; x++) for (let y = -10; y < MAP_SIZE; y++) drawTile(x, y, '#0a1a0a', (x === selectedTile.x && y === selectedTile.y));
    const links = [
        { f: 'BIOS', t: 'BOOT', c: '#ffff00' }, { f: 'BOOT', t: 'SYS', c: '#c0c0c0' }, { f: 'SYS', t: 'CPU', c: '#ff4d4d' }, 
        { f: 'CPU', t: 'RAM', c: '#4dff88' }, { f: 'CPU', t: 'GPU', c: '#4d94ff' }, { f: 'CPU', t: 'REG', c: '#ff00ff' }, 
        { f: 'CPU', t: 'ROUT', c: '#ff007f' }, { f: 'ROUT', t: 'WEB', c: '#00ccff' }, { f: 'WEB', t: 'SRV', c: '#7f00ff' }
    ];
    ctx.setLineDash([4, 4]);
    links.forEach(l => {
        const from = districts.find(d => d.type === l.f), to = districts.find(d => d.type === l.t);
        if(from && to) {
            const p1 = toIso(from.x, from.y), p2 = toIso(to.x, to.y);
            ctx.strokeStyle = l.c + "33"; ctx.beginPath(); ctx.moveTo(p1.isoX, p1.isoY); ctx.lineTo(p2.isoX, p2.isoY); ctx.stroke();
            if(Math.random() < 0.02) spawnPacket(from.x, from.y, to.x, to.y, l.c);
        }
    });
    ctx.setLineDash([]);
    packets.forEach((pkt, i) => {
        pkt.p += 0.005; const curX = pkt.x + (pkt.tx - pkt.x) * pkt.p, curY = pkt.y + (pkt.ty - pkt.y) * pkt.p, pos = toIso(curX, curY);
        ctx.fillStyle = pkt.color; ctx.beginPath(); ctx.arc(pos.isoX, pos.isoY, 3*zoom, 0, Math.PI*2); ctx.fill();
        if(pkt.p >= 1) packets.splice(i, 1);
    });
    agents.forEach(agent => {
        const pos = toIso(agent.x || 0, agent.y || 0); ctx.fillStyle = 'cyan'; ctx.beginPath(); ctx.arc(pos.isoX, pos.isoY, 6*zoom, 0, Math.PI*2); ctx.fill(); ctx.strokeStyle = 'white'; ctx.stroke();
    });
    if (contextMenu) {
        ctx.fillStyle = 'rgba(0,0,0,0.9)'; ctx.fillRect(contextMenu.px, contextMenu.py, 180, 100); ctx.strokeStyle = '#00ffff'; ctx.strokeRect(contextMenu.px, contextMenu.py, 180, 100);
        ctx.fillStyle = 'white'; ctx.font = '12px Arial'; ctx.fillText(contextMenu.node.type + " SUITE", contextMenu.px + 10, contextMenu.py + 20);
        let off = 40; const suite = BUILD_TYPES[contextMenu.node.type].suite;
        if(suite) suite.forEach(s => { ctx.fillText(s.label + ": " + contextMenu.node.settings[s.id], contextMenu.px + 10, contextMenu.py + off); off += 20; });
    }
    requestAnimationFrame(render);
}

window.setBuildType = (type) => { currentBuildType = type; };
canvas.addEventListener('wheel', (e) => { e.preventDefault(); if(e.deltaY < 0) zoom *= 1.1; else zoom /= 1.1; zoom = Math.min(Math.max(0.1, zoom), 5); });
canvas.addEventListener('mousedown', (e) => {
    if(e.button === 1 || (e.button === 0 && e.shiftKey)) { isDragging = true; lastMouseX = e.clientX; lastMouseY = e.clientY; }
    else if(e.button === 0) {
        contextMenu = null; districts = districts.filter(d => d.x !== selectedTile.x || d.y !== selectedTile.y);
        const settings = {}; const suite = BUILD_TYPES[currentBuildType].suite; if(suite) suite.forEach(s => settings[s.id] = s.value);
        districts.push({ x: selectedTile.x, y: selectedTile.y, type: currentBuildType, settings: settings });
    }
});
canvas.addEventListener('contextmenu', (e) => {
    e.preventDefault(); const node = districts.find(d => d.x === selectedTile.x && d.y === selectedTile.y);
    if(node) { const rect = canvas.getBoundingClientRect(); contextMenu = { px: e.clientX - rect.left, py: e.clientY - rect.top, node: node }; }
});
window.addEventListener('mousemove', (e) => {
    if(isDragging) { camX += (e.clientX - lastMouseX); camY += (e.clientY - lastMouseY); lastMouseX = e.clientX; lastMouseY = e.clientY; }
    const rect = canvas.getBoundingClientRect(); selectedTile = fromIso(e.clientX - rect.left, e.clientY - rect.top);
});
window.addEventListener('mouseup', () => { isDragging = false; });
render();
