/**
 * TIMESTAMP: 2026-06-09
 * PROJECT_ID: SimsMerged-v1.4.2
 * DESCRIPTION: Phase 1 - 2:1 Isometric Projection Engine & Render Loop
 */

class IsometricEngine {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d', { alpha: false }); // Optimize for no transparency on base
        
        // Tile dimensions (2:1 ratio for true isometric)
        this.tileWidth = 64;
        this.tileHeight = 32;
        
        // Grid size
        this.gridSizeX = 50;
        this.gridSizeY = 50;
        
        // Interaction state
        this.isDragging = false;
        this.lastMouse = { x: 0, y: 0 };
        
        this.init();
        this.bindEvents();
    }

    init() {
        this.resize();
        window.addEventListener('resize', () => this.resize());
        
        // Center camera initially
        const cx = window.innerWidth / 2;
        const cy = window.innerHeight / 4;
        actions.updateCamera(cx, cy, 1.0);
        
        // Start Render Loop
        requestAnimationFrame(() => this.render());
    }

    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    bindEvents() {
        this.canvas.addEventListener('mousedown', (e) => {
            this.isDragging = true;
            this.lastMouse = { x: e.clientX, y: e.clientY };
        });

        window.addEventListener('mouseup', () => {
            this.isDragging = false;
        });

        window.addEventListener('mousemove', (e) => {
            if (!this.isDragging) return;
            
            const state = appState.getState();
            const dx = e.clientX - this.lastMouse.x;
            const dy = e.clientY - this.lastMouse.y;
            
            actions.updateCamera(
                state.camera.x + dx,
                state.camera.y + dy,
                state.camera.zoom
            );
            
            this.lastMouse = { x: e.clientX, y: e.clientY };
        });

        this.canvas.addEventListener('wheel', (e) => {
            const state = appState.getState();
            let newZoom = state.camera.zoom - (e.deltaY * 0.001);
            newZoom = Math.max(0.2, Math.min(newZoom, 3.0)); // Clamp zoom
            actions.updateCamera(state.camera.x, state.camera.y, newZoom);
        });
    }

    // Mathematical Cartesion to Isometric mapping
    cartToIso(cartX, cartY) {
        const state = appState.getState();
        const isoX = (cartX - cartY) * (this.tileWidth / 2);
        const isoY = (cartX + cartY) * (this.tileHeight / 2);
        
        // Apply camera transforms
        return {
            x: (isoX * state.camera.zoom) + state.camera.x,
            y: (isoY * state.camera.zoom) + state.camera.y
        };
    }

    render() {
        const state = appState.getState();
        
        // Clear background
        this.ctx.fillStyle = '#050505';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw Topological Grid (Phase 6 Visualization)
        this.ctx.lineWidth = 1;
        this.ctx.strokeStyle = 'rgba(0, 255, 204, 0.15)'; // Cyber grid lines
        
        for (let x = 0; x < this.gridSizeX; x++) {
            for (let y = 0; y < this.gridSizeY; y++) {
                this.drawTile(x, y, state.camera.zoom);
            }
        }
        
        // Draw Agents
        this.drawAgents(state.agents, state.camera.zoom);
        
        requestAnimationFrame(() => this.render());
    }

    drawTile(x, y, zoom) {
        const top = this.cartToIso(x, y);
        const right = this.cartToIso(x + 1, y);
        const bottom = this.cartToIso(x + 1, y + 1);
        const left = this.cartToIso(x, y + 1);

        // Basic Frustum Culling: Don't draw tiles off screen
        const maxRadius = this.tileWidth * zoom;
        if (top.x < -maxRadius || top.x > this.canvas.width + maxRadius ||
            top.y < -maxRadius || top.y > this.canvas.height + maxRadius) {
            return;
        }

        this.ctx.beginPath();
        this.ctx.moveTo(top.x, top.y);
        this.ctx.lineTo(right.x, right.y);
        this.ctx.lineTo(bottom.x, bottom.y);
        this.ctx.lineTo(left.x, left.y);
        this.ctx.closePath();
        this.ctx.stroke();
    }

    drawAgents(agents, zoom) {
        for (const [id, agent] of Object.entries(agents)) {
            // Draw a highly visible retro shape for the agent
            const pos = this.cartToIso(agent.x, agent.y);
            
            this.ctx.fillStyle = agent.status === 'SUSPENDED' ? '#ff3366' : '#33ff66';
            this.ctx.beginPath();
            // A diamond shape representing the agent
            this.ctx.arc(pos.x, pos.y - (10 * zoom), 10 * zoom, 0, Math.PI * 2);
            this.ctx.fill();
            
            // Draw Agent ID Text
            this.ctx.fillStyle = '#ffffff';
            this.ctx.font = `${10 * zoom}px Courier New`;
            this.ctx.textAlign = 'center';
            this.ctx.fillText(id, pos.x, pos.y - (25 * zoom));
        }
    }
}
