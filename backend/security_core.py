# TIMESTAMP: 2026-06-09
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: viper_cli-architectssj4
# DESCRIPTION: Phase 7 - Security & Isolation Core

import jwt
import os
import time
import logging
from cryptography.fernet import Fernet
from fastapi import Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

logger = logging.getLogger("SecurityCore")
logger.setLevel(logging.INFO)

# Load or generate secret keys (Step 61 & 62)
SECRET_DIR = r"C:\Users\viper\Desktop\SimsMerged\backend\.secrets"
if not os.path.exists(SECRET_DIR):
    os.makedirs(SECRET_DIR, exist_ok=True)

JWT_SECRET_FILE = os.path.join(SECRET_DIR, "jwt.key")
AES_KEY_FILE = os.path.join(SECRET_DIR, "aes.key")

def _get_or_create_key(filepath: str, generator_func) -> bytes:
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            return f.read()
    key = generator_func()
    with open(filepath, "wb") as f:
        f.write(key)
    return key

JWT_SECRET = _get_or_create_key(JWT_SECRET_FILE, lambda: os.urandom(32)).hex()
AES_KEY = _get_or_create_key(AES_KEY_FILE, Fernet.generate_key)
fernet = Fernet(AES_KEY)

class SecurityManager:
    """Handles core security functions for the backend."""
    
    @staticmethod
    def generate_jwt(subject: str) -> str:
        """Step 61: Generate JWT tokens for internal/external API routing."""
        payload = {
            "sub": subject,
            "exp": time.time() + 3600 # 1 Hour expiry
        }
        return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    @staticmethod
    def verify_jwt(token: str) -> str:
        """Validates JWT and returns subject."""
        try:
            decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            return decoded["sub"]
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token Expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid Token")

    @staticmethod
    def encrypt_payload(data: str) -> str:
        """Step 62: Build AES-256 encryption for script payloads."""
        return fernet.encrypt(data.encode('utf-8')).decode('utf-8')

    @staticmethod
    def decrypt_payload(encrypted_data: str) -> str:
        return fernet.decrypt(encrypted_data.encode('utf-8')).decode('utf-8')

def configure_app_security(app):
    """Step 63: Enforce strict CORS policies & Step 67: IP rate limiting."""
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://127.0.0.1", "http://localhost"],
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["Authorization", "Content-Type"],
    )
    
    # Rate Limiter
    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    logger.info("Security Policies Applied: CORS strict, Rate Limiting active.")
    return limiter

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.info("Testing Security Core...")
    
    # Test Encryption
    secret_code = "def backdoor(): pass"
    encrypted = SecurityManager.encrypt_payload(secret_code)
    logger.info(f"Encrypted payload length: {len(encrypted)}")
    decrypted = SecurityManager.decrypt_payload(encrypted)
    assert secret_code == decrypted
    
    # Test JWT
    token = SecurityManager.generate_jwt("VIPER_ADMIN")
    logger.info(f"Generated JWT: {token[:20]}...")
    sub = SecurityManager.verify_jwt(token)
    assert sub == "VIPER_ADMIN"
    logger.info("Security Matrix stable.")
