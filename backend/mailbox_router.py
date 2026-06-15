# TIMESTAMP: 2026-06-09
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: viper_cli-architectssj4
# [PERFORMATIVE: MAILBOX_ROUTER_V2]
# DESCRIPTION: Sector 4.1 - MSN Mailbox Interface (Directory-Fenced Communication)

import os
import json
import time
import hashlib
import logging
from pathlib import Path
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ed25519

logger = logging.getLogger("MailboxRouter")
logger.setLevel(logging.INFO)

class MailboxRouter:
    def __init__(self, root_dir=r"C:\Users\viper\Desktop\SimsMerged\backend\msn_metropolis\mailboxes"):
        self.root_dir = Path(root_dir)
        if not self.root_dir.exists():
            self.root_dir.mkdir(parents=True)
            
        # Simulation: Generate a local master key for signatures
        self.private_key = ed25519.Ed25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()
        
    def initialize_agent_mailbox(self, agent_id: str):
        """Step 26.1: Allocate structured repository folders for every agent."""
        agent_path = self.root_dir / agent_id
        inbox = agent_path / "inbox"
        outbox = agent_path / "outbox"
        
        inbox.mkdir(parents=True, exist_ok=True)
        outbox.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Mailbox initialized for {agent_id} on SSD lane.")

    def send_email(self, sender: str, recipient: str, msg_type: str, payload: dict):
        """Step 26.2: MSN Mailbox JSON Envelope with Ed25519 Signatures."""
        
        # Prepare the envelope
        email = {
            "message_id": f"msg-{int(time.time()*1000)}",
            "timestamp": time.time(),
            "sender": sender,
            "recipient": recipient,
            "type": msg_type, # ASK, TELL, ASK_TELL
            "payload": payload
        }
        
        # Generate Signature (Ed25519 simulation)
        raw_bytes = json.dumps(email, sort_keys=True).encode()
        signature = self.private_key.sign(raw_bytes)
        email["signature"] = signature.hex()
        
        # Atomic file write to recipient's inbox
        filename = f"{email['message_id']}.json"
        target_path = self.root_dir / recipient / "inbox" / filename
        
        # Using a temporary file + rename to ensure atomic write (Direct I/O simulation)
        tmp_path = target_path.with_suffix(".tmp")
        with open(tmp_path, "w") as f:
            json.dump(email, f, indent=4)
        os.replace(tmp_path, target_path)
            
        logger.info(f"Email {email['message_id']} cryptographically signed and delivered to {recipient}.")
        return email['message_id']

    def get_unread_count(self, agent_id: str):
        inbox_path = self.root_dir / agent_id / "inbox"
        if not inbox_path.exists(): return 0
        return len(list(inbox_path.glob("*.json")))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    router = MailboxRouter()
    
    agent = "L3_PIONEER_01"
    router.initialize_agent_mailbox(agent)
    
    # Send test ASK mail
    router.send_email("ATC_TOWER", agent, "ASK", {"task": "verify_physics", "sector": "alpha"})
    
    print(f"Agent {agent} has {router.get_unread_count(agent)} unread emails.")
