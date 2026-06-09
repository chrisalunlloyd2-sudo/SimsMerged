$base_path = "C:\Users\viper\Desktop\SimsMerged"

$parameter_templates = @(
    @{ id="lr"; label="Learning Rate"; type="range"; min=0.0001; max=0.1; step=0.0001; val=0.001 },
    @{ id="batch"; label="Batch Size"; type="number"; val=64 },
    @{ id="epochs"; label="Training Epochs"; type="range"; min=1; max=100; step=1; val=10 },
    @{ id="dropout"; label="Dropout Rate"; type="range"; min=0.0; max=0.9; step=0.05; val=0.2 },
    @{ id="ctx"; label="Context Window (Tokens)"; type="number"; val=32768 },
    @{ id="quant"; label="Quantization Level"; type="text"; val="8-bit Int" },
    @{ id="temp"; label="Inference Temperature"; type="range"; min=0.0; max=2.0; step=0.1; val=0.7 },
    @{ id="rope"; label="RoPE Theta Base"; type="number"; val=10000 },
    @{ id="flash"; label="FlashAttention V2"; type="checkbox"; val=$true },
    @{ id="clip"; label="Gradient Clipping Norm"; type="range"; min=0.1; max=5.0; step=0.1; val=1.0 },
    @{ id="decay"; label="Weight Decay (L2)"; type="range"; min=0.0; max=0.1; step=0.001; val=0.01 },
    @{ id="heads"; label="Attention Heads (GQA)"; type="number"; val=32 },
    @{ id="slide"; label="Sliding Window Size"; type="number"; val=4096 },
    @{ id="act"; label="Activation Func"; type="text"; val="SwiGLU" },
    @{ id="norm"; label="Layer Norm Epsilon"; type="text"; val="1e-5" },
    @{ id="top_p"; label="Top-P (Nucleus)"; type="range"; min=0.1; max=1.0; step=0.05; val=0.9 },
    @{ id="rag_k"; label="RAG Retrieval Top-K"; type="number"; val=10 },
    @{ id="dim"; label="Hidden Dimension Size"; type="number"; val=4096 },
    @{ id="vocab"; label="Tokenizer Vocab Size"; type="number"; val=128256 },
    @{ id="mem"; label="KV Cache Mem Limit (GB)"; type="range"; min=1; max=80; step=1; val=24 }
)

$db = @{}

for ($i=1; $i -le 2700; $i++) {
    $feature_id = "TASK_$i"
    
    # Randomly shuffle and take 15
    $shuffled = $parameter_templates | Sort-Object {Get-Random}
    $selected_params = $shuffled[0..14]
    
    $feature_params = @()
    foreach ($param in $selected_params) {
        $p_copy = @{}
        foreach ($key in $param.Keys) { $p_copy[$key] = $param[$key] }
        
        $multiplier = (Get-Random -Minimum 80 -Maximum 120) / 100.0
        
        if ($p_copy["type"] -eq "number") {
            $p_copy["val"] = [math]::Round($p_copy["val"] * $multiplier)
        } elseif ($p_copy["type"] -eq "range") {
            $p_copy["val"] = [math]::Round($p_copy["val"] * $multiplier, 4)
        }
        
        $feature_params += $p_copy
    }
    
    $db[$feature_id] = $feature_params
}

$target_dir = "$base_path\backend\data"
if (-not (Test-Path $target_dir)) {
    New-Item -ItemType Directory -Force -Path $target_dir | Out-Null
}

$json_data = $db | ConvertTo-Json -Depth 5
Set-Content -Path "$target_dir\ai_attributes.json" -Value $json_data -Encoding UTF8

Write-Host "Successfully generated 40,500 unique hyperparameter settings across 2700 features!"
