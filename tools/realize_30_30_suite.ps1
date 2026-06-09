$html_path = "C:\Users\viper\Desktop\SimsMerged\frontend\index.html"
$content = Get-Content -Path $html_path -Raw

$new_vars = @"
        const COMPONENT_VARS = {
            'LLM': [
                { id: 'ctx_len', label: 'Max Pos Embeddings', type: 'number', val: 128000 },
                { id: 'rope_theta', label: 'RoPE Theta', type: 'number', val: 1000000 },
                { id: 'flash_attn', label: 'FlashAttention-2', type: 'checkbox', val: true },
                { id: 'kv_quant', label: 'KV Cache Quantization', type: 'text', val: '8-bit' },
                { id: 'gqa_heads', label: 'GQA KV Heads', type: 'number', val: 8 },
                { id: 'sliding_win', label: 'Sliding Window', type: 'number', val: 4096 },
                { id: 'chunk_size', label: 'Context Chunk Size', type: 'number', val: 512 },
                { id: 'compression', label: 'Context Compression', type: 'checkbox', val: true },
                { id: 'max_input', label: 'Max Input Tokens', type: 'number', val: 32768 },
                { id: 'max_output', label: 'Max Output Tokens', type: 'number', val: 4096 },
                { id: 'trunc_strat', label: 'Truncation Strategy', type: 'text', val: 'FIFO-Rolling' },
                { id: 'rag_top_k', label: 'RAG Ingestion Top-K', type: 'number', val: 5 },
                { id: 'soft_prompt', label: 'Soft Prompting Tuning', type: 'checkbox', val: false },
                { id: 'system_pin', label: 'System Prompt Pinning', type: 'checkbox', val: true },
                { id: 'ttft_opt', label: 'TTFT Latency Target', type: 'text', val: '<500ms' }
            ],
            'BANK': [
                { id: 'ledger', label: 'Ledger Protocol', type: 'text', val: 'Proof-of-Stake' },
                { id: 'hash', label: 'Hash Algorithm', type: 'text', val: 'SHA-256' },
                { id: 'block_time', label: 'Block Time (s)', type: 'range', min: 1, max: 60, val: 12 },
                { id: 'gas_fee', label: 'Base Gas Fee', type: 'range', min: 0.001, max: 1.0, step: 0.001, val: 0.01 },
                { id: 'sprite_mint', label: 'Sprite Mint Yield', type: 'number', val: 500 },
                { id: 'stake_yield', label: 'Staking APY %', type: 'range', min: 0, max: 100, val: 12 },
                { id: 'liquidity', label: 'Liquidity Pool', type: 'number', val: 1000000 },
                { id: 'burn_rate', label: 'Auto-Burn Rate %', type: 'range', min: 0, max: 10, step: 0.1, val: 1.5 },
                { id: 'dex_router', label: 'DEX Router', type: 'checkbox', val: true },
                { id: 'zk_snarks', label: 'Zero-Knowledge Proofs', type: 'checkbox', val: true },
                { id: 'validator', label: 'Validator Nodes', type: 'number', val: 64 },
                { id: 'smart_con', label: 'Smart Contracts', type: 'checkbox', val: true },
                { id: 'treasury', label: 'Treasury Wallet', type: 'text', val: '0x00000000000' },
                { id: 'mint_limit', label: 'Max Supply Cap', type: 'number', val: 21000000 },
                { id: 'oracle', label: 'Price Oracle Node', type: 'checkbox', val: true }
            ],
            'AGENT': [
                { id: 'model_wrap', label: 'Model Matrix (30)', type: 'select', options: [
                    'Claw-v1.0', 'Claw-v2.0', 'Claude-3.5', 'Danube-1.8B', 'Llama-3-8B', 'Llama-3-70B', 
                    'Mistral-0.3', 'Gemma-2', 'Phi-3', 'Qwen-2', 'Grok-1.5', 'Gemini-1.5', 
                    'DeepSeek-v2', 'Falcon-2', 'StableLM-2', 'OLMo-1.7', 'OpenELM-3B', 'Aria-MoE', 
                    'BitNet-1.58', 'Mamba-2', 'Jamba-1.0', 'DBRX', 'Command-R', 'XVERSE-v2', 
                    'Yi-1.5', 'StarCoder-2', 'Arctic-v1', 'Bloom-7B', 'Vicuna-1.5', 'Alpaca-Native'
                ], val: 'Claw-v2.0' },
                { id: 'temp', label: 'Inference Temp', type: 'range', min: 0, max: 2, step: 0.1, val: 0.7 },
                { id: 'top_p', label: 'Top-P Sampling', type: 'range', min: 0, max: 1, step: 0.05, val: 0.9 },
                { id: 'top_k', label: 'Top-K Sampling', type: 'number', val: 40 },
                { id: 'min_p', label: 'Min-P Sampling', type: 'range', min: 0, max: 1, step: 0.01, val: 0.05 },
                { id: 'miro_mode', label: 'Mirostat Mode', type: 'number', val: 2 },
                { id: 'miro_tau', label: 'Mirostat Tau', type: 'range', min: 0, max: 10, step: 0.1, val: 5.0 },
                { id: 'miro_eta', label: 'Mirostat Eta', type: 'range', min: 0, max: 1, step: 0.01, val: 0.1 },
                { id: 'freq_pen', label: 'Frequency Penalty', type: 'range', min: 0, max: 2, step: 0.1, val: 0.0 },
                { id: 'pres_pen', label: 'Presence Penalty', type: 'range', min: 0, max: 2, step: 0.1, val: 0.0 },
                { id: 'rep_pen', label: 'Repeat Penalty', type: 'range', min: 1, max: 2, step: 0.05, val: 1.1 },
                { id: 'rep_range', label: 'Penalty Range', type: 'number', val: 64 },
                { id: 'ctx_win', label: 'Context Window', type: 'number', val: 32768 },
                { id: 'max_tok', label: 'Max Output Tokens', type: 'number', val: 4096 },
                { id: 'stop_seq', label: 'Stop Sequences', type: 'text', val: '"\n", "###"' },
                { id: 'seed', label: 'Random Seed', type: 'number', val: 42 },
                { id: 'stream', label: 'Stream Response', type: 'checkbox', val: true },
                { id: 'echo', label: 'Echo Input', type: 'checkbox', val: false },
                { id: 'typical_p', label: 'Typical-P', type: 'range', min: 0, max: 1, step: 0.1, val: 1.0 },
                { id: 'tfs_z', label: 'TFS-Z (Tail-Free)', type: 'range', min: 0, max: 1, step: 0.1, val: 1.0 },
                { id: 'logprobs', label: 'Logprobs Count', type: 'number', val: 0 },
                { id: 'best_of', label: 'Best-Of N', type: 'number', val: 1 },
                { id: 'mqa', label: 'Multi-Query Attn', type: 'checkbox', val: true },
                { id: 'gqa', label: 'Grouped-Query Attn', type: 'checkbox', val: true },
                { id: 'flash', label: 'Flash Attention', type: 'checkbox', val: true },
                { id: 'kv_q', label: 'KV Quantization', type: 'text', val: 'Q4_K_M' },
                { id: 'rope_s', label: 'RoPE Scaling', type: 'text', val: 'linear' },
                { id: 'rope_t', label: 'RoPE Theta', type: 'number', val: 10000 },
                { id: 'soft_p', label: 'Soft Prompt Tuning', type: 'checkbox', val: false },
                { id: 'sys_w', label: 'System Weight', type: 'range', min: 0, max: 1, step: 0.1, val: 0.5 }
            ],
"@

# Insert before currentSettings
$insertion_point = "window.currentSettings = {};"
$content = $content.Replace($insertion_point, $new_vars + "`n        " + $insertion_point)

# Update renderSetting to handle 'select' type
$select_code = @"
            } else if (v.type === 'select') {
                input = document.createElement('select');
                input.style.width = '100%'; input.style.fontSize = '10px';
                v.options.forEach(opt => {
                    const o = document.createElement('option');
                    o.value = o.innerText = opt;
                    if(opt === v.val) o.selected = true;
                    input.appendChild(o);
                });
"@

$target_input = "if (v.type === 'range') {"
$content = $content.Replace($target_input, $select_code + "`n            } else " + $target_input)

Set-Content -Path $html_path -Value $content -Encoding UTF8
Write-Host "30/30 AI Suite Realized!"
