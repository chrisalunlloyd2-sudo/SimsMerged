class ResourceMonitor {
    constructor() {
        this.cpuHistory = new Array(50).fill(0);
        this.memHistory = new Array(50).fill(0);
        this.initUI();
        this.startLoop();
    }

    initUI() {
        const win = document.createElement('div');
        win.id = 'resource-monitor';
        win.style.cssText = `
            position: absolute; top: 220px; right: 20px; width: 300px; height: 500px;
            background: #c0c0c0; border: 2px solid #fff; border-right: 2px solid #808080;
            border-bottom: 2px solid #808080; box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
            display: flex; flex-direction: column; z-index: 1000; font-family: 'Tahoma', sans-serif;
        `;

        win.innerHTML = `
            <div style="background: linear-gradient(90deg, #000080, #1084d0); color: white; padding: 3px 5px; font-weight: bold; font-size: 12px; display: flex; justify-content: space-between;">
                <span>Resource Monitor</span>
                <span style="cursor:pointer;" onclick="this.parentElement.parentElement.style.display='none'">X</span>
            </div>
            <div style="padding: 10px; flex-grow: 1; display: flex; flex-direction: column; gap: 8px; overflow-y: auto;">
                <div style="font-size: 11px; font-weight: bold;">CPU Usage History</div>
                <canvas id="cpu-chart" width="280" height="80" style="background: #000; border: 1px solid #808080;"></canvas>
                <div style="font-size: 11px; font-weight: bold;">Memory Usage History</div>
                <canvas id="mem-chart" width="280" height="80" style="background: #000; border: 1px solid #808080;"></canvas>
                
                <div style="font-size: 10px; font-weight: bold;">16-Core Virtual CPU Affinity Matrix</div>
                <div id="core-grid-matrix" style="display: grid; grid-template-columns: repeat(8, 1fr); gap: 3px; background: #000; border: 1px inset #808080; padding: 5px; margin-bottom: 2px;">
                    <!-- 16 affinity cores loaded dynamically -->
                </div>
                
                <div id="machine-details" style="font-size: 10px; background: #fff; border: 1px inset #808080; padding: 5px; height: 80px; overflow-y: auto;">
                    Linking to host machine...
                </div>
            </div>
        `;
        document.body.appendChild(win);
        this.cpuCtx = document.getElementById('cpu-chart').getContext('2d');
        this.memCtx = document.getElementById('mem-chart').getContext('2d');
    }

    drawChart(ctx, history, label) {
        const w = 280, h = 80;
        ctx.clearRect(0, 0, w, h);
        
        // Grid
        ctx.strokeStyle = '#004400';
        ctx.lineWidth = 1;
        for(let i=0; i<w; i+=20) { ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i, h); ctx.stroke(); }
        for(let i=0; i<h; i+=20) { ctx.beginPath(); ctx.moveTo(0, i); ctx.lineTo(w, i); ctx.stroke(); }

        // Line
        ctx.strokeStyle = '#00ff00';
        ctx.lineWidth = 2;
        ctx.beginPath();
        for(let i=0; i<history.length; i++) {
            const x = (i / (history.length-1)) * w;
            const y = h - (history[i] * h);
            if(i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        }
        ctx.stroke();
    }

    async startLoop() {
        while(true) {
            try {
                const res = await fetch('http://localhost:8000/api/machine-heartbeat');
                if(res.ok) {
                    const data = await res.json();
                    this.cpuHistory.push(data.real_cpu_load);
                    this.cpuHistory.shift();
                    this.memHistory.push(data.real_mem_pct);
                    this.memHistory.shift();

                    this.drawChart(this.cpuCtx, this.cpuHistory, 'CPU');
                    this.drawChart(this.memCtx, this.memHistory, 'MEM');

                    // Sync simulated 16-Core virtual load matrix dynamically
                    const coreGrid = document.getElementById('core-grid-matrix');
                    if (coreGrid) {
                        let html = '';
                        const coreLoad = window.coreLoad || {};
                        for (let i = 0; i < 16; i++) {
                            const load = parseFloat(coreLoad[i] || 0.0);
                            const r = Math.min(255, Math.floor(load * 255));
                            const g = Math.max(0, Math.min(255, Math.floor((1.0 - load) * 255)));
                            const color = `rgb(${r}, ${g}, 0)`;
                            html += `<div style="height: 10px; background: ${color}; border: 1px solid #333;" title="Core ${i}: ${(load * 100).toFixed(0)}%"></div>`;
                        }
                        coreGrid.innerHTML = html;
                    }

                    document.getElementById('machine-details').innerHTML = `
                        <b>HOST:</b> LOCAL_WIN32<br>
                        <b>CLOCK:</b> ${data.real_cpu_mhz} MHz<br>
                        <b>TOTAL_MEM:</b> ${(data.real_mem_total_kb / 1024 / 1024).toFixed(2)} GB<br>
                        <b>LOAD:</b> ${(data.real_cpu_load * 100).toFixed(1)}%<br>
                        <b>TIMESTAMP:</b> ${new Date().toLocaleTimeString()}
                    `;
                }
            } catch(e) {}
            await new Promise(r => setTimeout(r, 2000));
        }
    }
}

window.resourceMonitor = new ResourceMonitor();

window.openResourceMonitor = function() {
    const win = document.getElementById('resource-monitor');
    if (win) {
        win.style.display = 'flex';
    }
};
