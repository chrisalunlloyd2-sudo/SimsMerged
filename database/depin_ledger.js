// depin_ledger.js
// TIMESTAMP: 2026-05-25T12:20:00.000Z
// PROJECT_ID: SimsMerged-v1.3
// MANDATE: DePIN Tokenomics & SHA-256 Anchoring

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const LEDGER_PATH = path.join(__dirname, 'blockchain_ledger.json');

class DePINLedger {
    constructor() {
        this.loadLedger();
    }

    loadLedger() {
        if (fs.existsSync(LEDGER_PATH)) {
            this.ledger = JSON.parse(fs.readFileSync(LEDGER_PATH, 'utf8'));
        } else {
            this.ledger = {
                balances: {},
                transactions: [],
                totalMinted: 0
            };
            this.saveLedger();
        }
    }

    saveLedger() {
        fs.writeFileSync(LEDGER_PATH, JSON.stringify(this.ledger, null, 2));
    }

    // Nocturnal Protocol: Night is Day, Day is Night.
    // Active Cycle: 8 PM (20) to 8 AM (8)
    isDaytime() {
        const hour = new Date().getHours();
        return hour >= 20 || hour < 8;
    }

    mintTokens(agentId, amount, proofOfWorkString) {
        if (!this.isDaytime()) {
            console.log(`[DePIN] Night cycle active. Token minting paused for ${agentId}.`);
            return false;
        }

        // Validate Proof of Work
        // For the Genesis or EPMO drops, we allow '00' as a bypass
        const isBypass = proofOfWorkString.startsWith("00");
        const hash = crypto.createHash('sha256').update(proofOfWorkString).digest('hex');
        
        if (!isBypass && !hash.startsWith('00')) {
            console.log(`[DePIN] Invalid PoW from ${agentId}. Hash: ${hash}`);
            return false;
        }

        if (!this.ledger.balances[agentId]) this.ledger.balances[agentId] = 0;
        this.ledger.balances[agentId] += amount;
        this.ledger.totalMinted += amount;

        this.ledger.transactions.push({
            timestamp: new Date().toISOString(),
            type: 'MINT',
            agent: agentId,
            amount: amount,
            hash: hash
        });

        this.saveLedger();
        console.log(`[DePIN] Minted ${amount} tokens for ${agentId}. Balance: ${this.ledger.balances[agentId]}`);
        return true;
    }

    deductTokens(agentId, amount, reason) {
        if (!this.ledger.balances[agentId] || this.ledger.balances[agentId] < amount) {
            console.log(`[DePIN] Agent ${agentId} has insufficient funds. Needed: ${amount}.`);
            return false;
        }

        this.ledger.balances[agentId] -= amount;
        this.ledger.transactions.push({
            timestamp: new Date().toISOString(),
            type: 'BURN',
            agent: agentId,
            amount: amount,
            reason: reason
        });
        
        this.saveLedger();
        return true;
    }
    
    getBalance(agentId) {
        return this.ledger.balances[agentId] || 0;
    }
}

module.exports = new DePINLedger();
