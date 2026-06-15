/**
 * TIMESTAMP: 2026-06-09
 * PROJECT_ID: SimsMerged-v1.4.2
 * DESCRIPTION: Phase 1 - Vanilla JS State Manager (Redux/Zustand pattern)
 */

class Store {
    constructor(initialState = {}) {
        this.state = initialState;
        this.listeners = new Set();
    }

    getState() {
        return this.state;
    }

    setState(newState) {
        // Shallow merge
        this.state = { ...this.state, ...newState };
        this.notify();
    }

    subscribe(listener) {
        this.listeners.add(listener);
        // Return unsubscribe function
        return () => this.listeners.delete(listener);
    }

    notify() {
        for (const listener of this.listeners) {
            listener(this.state);
        }
    }
}

// Global Application State
const initialState = {
    systemStatus: 'ONLINE', // ONLINE, PAUSED
    totalDePIN: 0.00,
    agents: {}, // { agentId: { x, y, z, balance, status } }
    chatMessages: [], // { sender, channel, text, timestamp }
    camera: { x: 0, y: 0, zoom: 1.0 },
    selectedAgent: null
};

const appState = new Store(initialState);

// State Mutators (Actions)
const actions = {
    setSystemStatus: (status) => appState.setState({ systemStatus: status }),
    updateDePIN: (amount) => appState.setState({ totalDePIN: amount }),
    upsertAgent: (id, data) => {
        const currentAgents = appState.getState().agents;
        appState.setState({
            agents: {
                ...currentAgents,
                [id]: { ...(currentAgents[id] || {}), ...data }
            }
        });
    },
    addChatMessage: (msg) => {
        const msgs = [...appState.getState().chatMessages, msg];
        // Keep last 100 messages to prevent DOM lag
        if (msgs.length > 100) msgs.shift();
        appState.setState({ chatMessages: msgs });
    },
    updateCamera: (x, y, zoom) => appState.setState({ camera: { x, y, zoom } }),
    selectAgent: (id) => appState.setState({ selectedAgent: id })
};
