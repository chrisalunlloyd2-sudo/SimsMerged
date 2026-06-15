# TIMESTAMP: 2026-06-09
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: viper_cli-architectssj4
# DESCRIPTION: Phase 6 - Analytics Dashboard & Reporting API

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import sqlite3
import pandas as pd
import os
import logging
from typing import Dict, Any

logger = logging.getLogger("AnalyticsAPI")
logger.setLevel(logging.INFO)

app = FastAPI(title="DePIN Analytics Dashboard API", version="1.0")

DB_DEPIN = r"C:\Users\viper\Desktop\SimsMerged\backend\depin_ledger.db"

class AnalyticsEngine:
    @staticmethod
    def get_depin_economy_stats() -> Dict[str, Any]:
        """Step 52: Build DePIN economic dashboard backend."""
        if not os.path.exists(DB_DEPIN):
            return {"error": "Ledger DB not found."}
            
        with sqlite3.connect(DB_DEPIN) as conn:
            df = pd.read_sql_query("SELECT * FROM wallets", conn)
            df_tx = pd.read_sql_query("SELECT * FROM transactions", conn)
            
        total_supply = df['balance'].sum() if not df.empty else 0
        total_burned = abs(df_tx[df_tx['tx_type'] == 'INFERENCE_BURN']['amount'].sum()) if not df_tx.empty else 0
        
        return {
            "total_active_agents": len(df[df['status'] == 'ACTIVE']) if not df.empty else 0,
            "total_suspended_agents": len(df[df['status'] == 'SUSPENDED']) if not df.empty else 0,
            "total_token_supply": float(total_supply),
            "total_tokens_burned": float(total_burned)
        }

    @staticmethod
    def get_anonymized_export() -> Dict[str, Any]:
        """Step 56: Implement data anonymization for exports."""
        if not os.path.exists(DB_DEPIN):
            return {"error": "Ledger DB not found."}
            
        with sqlite3.connect(DB_DEPIN) as conn:
            df = pd.read_sql_query("SELECT agent_id, balance, status FROM wallets", conn)
            
        if not df.empty:
            # Mask agent IDs
            df['agent_id'] = df['agent_id'].apply(lambda x: f"AGENT_***{x[-4:]}" if len(x)>4 else "AGENT_***")
            
        return df.to_dict(orient="records")

@app.get("/api/v1/analytics/economy")
async def economy_endpoint():
    return AnalyticsEngine.get_depin_economy_stats()

@app.get("/api/v1/analytics/export_anonymized")
async def export_endpoint():
    return AnalyticsEngine.get_anonymized_export()

if __name__ == "__main__":
    # Running on 8010 to avoid port collisions with MSN Metropolis (8000/8002) and Ide Mock (8001)
    uvicorn.run(app, host="127.0.0.1", port=8010)
