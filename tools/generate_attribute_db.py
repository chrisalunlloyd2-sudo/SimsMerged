import json
import random
import os

base_path = r"C:\Users\viper\Desktop\SimsMerged"

# Core AI settings that can be safely changed in research
parameter_templates = [
    {"id": "lr", "label": "Learning Rate", "type": "range", "min": 0.0001, "max": 0.1, "step": 0.0001, "val": 0.001},
    {"id": "batch", "label": "Batch Size", "type": "number", "val": 64},
    {"id": "epochs", "label": "Training Epochs", "type": "range", "min": 1, "max": 100, "step": 1, "val": 10},
    {"id": "dropout", "label": "Dropout Rate", "type": "range", "min": 0.0, "max": 0.9, "step": 0.05, "val": 0.2},
    {"id": "ctx", "label": "Context Window (Tokens)", "type": "number", "val": 32768},
    {"id": "quant", "label": "Quantization Level", "type": "text", "val": "8-bit Int"},
    {"id": "temp", "label": "Inference Temperature", "type": "range", "min": 0.0, "max": 2.0, "step": 0.1, "val": 0.7},
    {"id": "rope", "label": "RoPE Theta Base", "type": "number", "val": 10000},
    {"id": "flash", "label": "FlashAttention V2", "type": "checkbox", "val": True},
    {"id": "clip", "label": "Gradient Clipping Norm", "type": "range", "min": 0.1, "max": 5.0, "step": 0.1, "val": 1.0},
    {"id": "decay", "label": "Weight Decay (L2)", "type": "range", "min": 0.0, "max": 0.1, "step": 0.001, "val": 0.01},
    {"id": "heads", "label": "Attention Heads (GQA)", "type": "number", "val": 32},
    {"id": "slide", "label": "Sliding Window Size", "type": "number", "val": 4096},
    {"id": "act", "label": "Activation Func", "type": "text", "val": "SwiGLU"},
    {"id": "norm", "label": "Layer Norm Epsilon", "type": "text", "val": "1e-5"},
    {"id": "top_p", "label": "Top-P (Nucleus)", "type": "range", "min": 0.1, "max": 1.0, "step": 0.05, "val": 0.9},
    {"id": "rag_k", "label": "RAG Retrieval Top-K", "type": "number", "val": 10},
    {"id": "dim", "label": "Hidden Dimension Size", "type": "number", "val": 4096},
    {"id": "vocab", "label": "Tokenizer Vocab Size", "type": "number", "val": 128256},
    {"id": "mem", "label": "KV Cache Mem Limit (GB)", "type": "range", "min": 1, "max": 80, "step": 1, "val": 24}
]

db = {}
# 22 phases, 100 features per phase = 2200 features. 
# We'll generate up to 2700 to match the roadmap items.
for i in range(1, 2701):
    feature_id = f"TASK_{i}"
    # Randomly select 15 parameters from our pool of 20
    selected_params = random.sample(parameter_templates, 15)
    
    # Slightly mutate values to ensure uniqueness
    feature_params = []
    for param in selected_params:
        p_copy = param.copy()
        if p_copy["type"] == "number":
            p_copy["val"] = int(p_copy["val"] * random.uniform(0.8, 1.2))
        elif p_copy["type"] == "range":
            p_copy["val"] = round(p_copy["val"] * random.uniform(0.9, 1.1), 4)
        feature_params.append(p_copy)
        
    db[feature_id] = feature_params

os.makedirs(os.path.join(base_path, "backend", "data"), exist_ok=True)
with open(os.path.join(base_path, "backend", "data", "ai_attributes.json"), "w", encoding="utf-8") as f:
    json.dump(db, f, indent=2)

print(f"Successfully generated 40,500 unique hyperparameter settings across 2700 features!")
