// TIMESTAMP: 2026-05-30T01:05:00.452Z
// PROJECT_ID: SimsMerged-v1.3-Metropolis
// AGENT_ID: Gemini-CLI-Architect

(function() {
    let is3DMode = false;
    const btn = document.getElementById('toggle-3d-btn');
    const container2D = document.getElementById('gameCanvas');
    const container3D = document.getElementById('webgl-container');
    const overlays = [document.getElementById('scanner-overlay'), document.getElementById('vignette')];

    if (typeof THREE === 'undefined') {
        console.warn("[WebGL] Three.js not loaded. 3D WebGL mode disabled.");
        if (btn) btn.style.display = 'none';
        return;
    }

    // Three.js setup
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x000500);
    const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 50, 50);
    camera.lookAt(0, 0, 0);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container3D.clientWidth || window.innerWidth - 320, container3D.clientHeight || window.innerHeight);
    container3D.appendChild(renderer.domElement);

    // Lighting
    const ambientLight = new THREE.AmbientLight(0x404040);
    scene.add(ambientLight);
    const dirLight = new THREE.DirectionalLight(0xffffff, 0.5);
    dirLight.position.set(20, 50, 20);
    scene.add(dirLight);

    // Objects map
    const meshes = {
        districts: new Map(),
        agents: new Map()
    };

    const BUILD_COLORS = {
        'CPU': 0xff4d4d, 'RAM': 0x4dff88, 'GPU': 0x4d94ff, 'SSD': 0xffffff,
        'NORTHBRIDGE': 0x00ffff, 'SOUTHBRIDGE': 0x0055ff, 'REGISTRY': 0xffff00,
        'LLM': 0x00ffff, 'AGENT': 0xffcc00, 'VDB': 0xff00ff, 'PLANT': 0xffaa00,
        'SCHOOL': 0x4facfe, 'HOSPITAL': 0xff4444, 'BANK': 0xffd700,
        'HOUSE': 0x888888, 'TREE': 0x0a3d0a, 'WATER': 0x0055ff, 'ROAD': 0x222222, 'RESEARCH': 0x00ffcc
    };

    function getGridPos(x, y) {
        // Isometric to 3D grid mapping
        return { x: x * 2, z: y * 2 };
    }

    let lastDistrictsLength = -1;
    let lastAgentsString = "";

    function syncScene() {
        if (!is3DMode) return;

        // Sync Districts (Only run if list changes to save iterations)
        if (window.districts && window.districts.length !== lastDistrictsLength) {
            window.districts.forEach((d, i) => {
                const id = `dist_${d.x}_${d.y}_${d.type}`;
                if (!meshes.districts.has(id)) {
                    const geometry = new THREE.BoxGeometry(1.8, d.type === 'ROAD' ? 0.2 : (d.type === 'WATER' ? 0.5 : 2), 1.8);
                    const material = new THREE.MeshLambertMaterial({ color: BUILD_COLORS[d.type] || 0x888888 });
                    const mesh = new THREE.Mesh(geometry, material);
                    const pos = getGridPos(d.x, d.y);
                    mesh.position.set(pos.x, geometry.parameters.height / 2, pos.z);
                    scene.add(mesh);
                    meshes.districts.set(id, mesh);
                }
            });
            lastDistrictsLength = window.districts.length;
        }

        // Sync Agents (Only process changes when list content/positions shift)
        if (window.agents) {
            const agentsJSON = JSON.stringify(window.agents.map(a => ({ id: a.id, x: a.x, y: a.y, role: a.role })));
            if (agentsJSON !== lastAgentsString) {
                const currentAgentIds = new Set(window.agents.map(a => a.id));
                // Remove old
                for (let [id, mesh] of meshes.agents) {
                    if (!currentAgentIds.has(id)) {
                        scene.remove(mesh);
                        meshes.agents.delete(id);
                    }
                }
                // Update/Add new
                window.agents.forEach(a => {
                    let mesh = meshes.agents.get(a.id);
                    if (!mesh) {
                        const geometry = new THREE.SphereGeometry(0.5, 16, 16);
                        const color = a.role === 'DOCTOR' ? 0xff4444 : (a.role === 'TEACHER' ? 0x4facfe : 0xffcc00);
                        const material = new THREE.MeshLambertMaterial({ color: color });
                        mesh = new THREE.Mesh(geometry, material);
                        scene.add(mesh);
                        meshes.agents.set(a.id, mesh);
                    }
                    const pos = getGridPos(a.x, a.y);
                    mesh.position.lerp(new THREE.Vector3(pos.x, 3, pos.z), 0.1);
                });
                lastAgentsString = agentsJSON;
            } else {
                // If structure is stable, still perform frame-to-frame smooth physics lerp
                window.agents.forEach(a => {
                    const mesh = meshes.agents.get(a.id);
                    if (mesh) {
                        const pos = getGridPos(a.x, a.y);
                        mesh.position.lerp(new THREE.Vector3(pos.x, 3, pos.z), 0.1);
                    }
                });
            }
        }
    }

    let lastAnimateTime = 0;
    const animateInterval = 1000 / 24; // 24 FPS

    function animate(timestamp) {
        requestAnimationFrame(animate);
        
        if (!is3DMode) return;
        
        if (!timestamp) timestamp = performance.now();
        const elapsed = timestamp - lastAnimateTime;
        if (elapsed < animateInterval) return;
        
        lastAnimateTime = timestamp - (elapsed % animateInterval);

        syncScene();
        // Slow camera rotation for nice effect
        const timer = Date.now() * 0.0001;
        camera.position.x = Math.cos(timer) * 50;
        camera.position.z = Math.sin(timer) * 50;
        camera.lookAt(0, 0, 0);
        renderer.render(scene, camera);
    }

    animate();

    if(btn) {
        btn.addEventListener('click', () => {
            is3DMode = !is3DMode;
            if (is3DMode) {
                container2D.style.display = 'none';
                overlays.forEach(o => { if(o) o.style.display = 'none'; });
                container3D.style.display = 'block';
                btn.innerText = "TOGGLE 2D ISOMETRIC";
                const width = container3D.clientWidth || window.innerWidth - 320;
                const height = container3D.clientHeight || window.innerHeight;
                renderer.setSize(width, height);
                camera.aspect = width / height;
                camera.updateProjectionMatrix();
            } else {
                container2D.style.display = 'block';
                overlays.forEach(o => { if(o) o.style.display = 'block'; });
                container3D.style.display = 'none';
                btn.innerText = "TOGGLE 3D WEBGL";
            }
        });
    }

    window.addEventListener('resize', () => {
        if (is3DMode) {
            const width = container3D.clientWidth || window.innerWidth - 320;
            const height = container3D.clientHeight || window.innerHeight;
            renderer.setSize(width, height);
            camera.aspect = width / height;
            camera.updateProjectionMatrix();
        }
    });
})();