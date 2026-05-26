// sprite_engine.js
// TIMESTAMP: 2026-05-25T05:00:00.000Z
// PROJECT_ID: SimsMerged-v1.3
// AGENT_ID: Gemini-CLI-Architect
// PROTOCOL_250: STEP 50/250
// MANDATE: Darwinian Sprite Evolution. Local ONLY.

const db = require('./database/db_wrapper');
const ai = require('./wrappers/ai_tools_wrapper');
const iso = require('./wrappers/isometric_engine');
const crypto = require('crypto');

class Sprite {
    constructor(id, name, role) {
        this.id = id;
        this.name = name;
        this.role = role;
        this.generation = 1;
    }

    async reason(task) {
        // Semantic Memory Retrieval (Vector-like)
        const memories = await db.searchSemanticMemory(task.title);
        const memoryContext = memories.map(m => m.content).join("\n");

        // Genetic Trait Retrieval (Best Prompts)
        const traits = await db.getBestGeneticTraits("SystemPrompt");
        const systemPrompt = traits[0] || `You are ${this.name}, a ${this.role} sprite in SimAgentCity. Use ReAct (Reasoning + Action).`;

        // Calculate a test isometric position for reasoning context
        const testPos = iso.cartesianToIso(5, 5);

        const prompt = `
        ${systemPrompt}
        CONTEXT FROM SEMANTIC MEMORY:
        ${memoryContext}
        
        ISOMETRIC GRID STATUS: Active (Reference Point [5,5] -> ISO [${testPos.x}, ${testPos.y}])
        
        TASK: ${task.description}
        
        THOUGHT (Reasoning):
        `;

        const thought = ai.callAichat(prompt);
        const hash = crypto.createHash('sha256').update(thought).digest('hex');
        await db.logThought(this.id, thought, hash);
        await db.addSemanticMemory(this.id, thought, JSON.stringify({ role: this.role, task: task.title }));
        
        return thought;
    }

    async act(thought, task) {
        console.log(`[${this.name}] Acting on thought...`);
        // Aider-based mutation
        const actionPrompt = `Based on this thought: ${thought.slice(0, 500)}, implement the required backend logic.`;
        const result = ai.callAider(actionPrompt, [`SimAgentCity/backend_${this.role.toLowerCase()}.js`]);
        
        // Darwinian Feedback (Fitness calculation)
        const fitness = result.includes("SUCCESS") ? 1.0 : 0.2;
        await db.addGeneticTrait(this.id, "SystemPrompt", `Elite ${this.role} Prompt: ${thought.slice(0, 100)}`, this.generation);
        
        return result;
    }
}

async function startSpriteEcosystem() {
    await db.initDb();
    
    // Initialize the 3 Backend Sprites
    const minerId = await db.addAgent("Miner-Core", "Miner");
    const processorId = await db.addAgent("Processor-Core", "Processor");
    const shipperId = await db.addAgent("Shipper-Core", "Shipper");

    const sprites = [
        new Sprite(minerId, "Miner-Core", "Miner"),
        new Sprite(processorId, "Processor-Core", "Processor"),
        new Sprite(shipperId, "Shipper-Core", "Shipper")
    ];

    console.log("--- SPRITE ECOSYSTEM ACTIVE (PROTOCOL 250: STEP 60) ---");

    while (true) {
        for (const sprite of sprites) {
            const task = await db.getPendingTask();
            if (task) {
                console.log(`[System] ${sprite.name} picked up task: ${task.title}`);
                await db.updateTaskStatus(task.id, 'ACTIVE', sprite.id);
                
                const thought = await sprite.reason(task);
                const actionResult = await sprite.act(thought, task);
                
                await db.updateTaskStatus(task.id, 'COMPLETED', sprite.id);
                console.log(`[System] ${sprite.name} completed task with result length: ${actionResult.length}`);
            }
        }
        // SSD Fence Delay: 5 Minutes between sprite sweeps
        await new Promise(resolve => setTimeout(resolve, 300000));
    }
}

if (require.main === module) {
    startSpriteEcosystem().catch(console.error);
}
