$html_path = "C:\Users\viper\Desktop\SimsMerged\frontend\index.html"
$content = Get-Content -Path $html_path -Raw

$start_str = "        function updateParamSuite(type) {"
$end_str = "        buildButtons.forEach(btn => {"

$new_func = @"
        function renderSetting(v, container) {
            const row = document.createElement('div');
            row.style.marginBottom = '10px';
            
            const labelContainer = document.createElement('div');
            labelContainer.style.display = 'flex';
            labelContainer.style.justifyContent = 'space-between';
            
            const label = document.createElement('label');
            label.innerText = v.label;
            
            const valueReadout = document.createElement('span');
            valueReadout.id = `readout-` + v.id;
            valueReadout.style.color = '#0f0';
            valueReadout.innerText = v.val;
            
            labelContainer.appendChild(label);
            labelContainer.appendChild(valueReadout);
            row.appendChild(labelContainer);
            
            let input;
            if (v.type === 'range') {
                input = document.createElement('input');
                input.type = 'range';
                input.min = v.min;
                input.max = v.max;
                if(v.step) input.step = v.step;
                input.value = v.val;
                input.style.width = '100%';
                input.style.cursor = 'pointer';
            } else if (v.type === 'checkbox') {
                input = document.createElement('input');
                input.type = 'checkbox';
                input.checked = v.val;
                valueReadout.innerText = v.val ? 'ON' : 'OFF';
            } else {
                input = document.createElement('input');
                input.type = v.type;
                input.value = v.val;
                input.style.width = '100%';
                input.style.background = '#000';
                input.style.color = '#0f0';
                input.style.border = '1px solid #005555';
                input.style.padding = '2px';
                input.style.fontSize = '10px';
            }

            input.oninput = input.onchange = () => {
                const finalVal = input.type === 'checkbox' ? input.checked : input.value;
                window.currentSettings[v.id] = finalVal;
                valueReadout.innerText = input.type === 'checkbox' ? (finalVal ? 'ON' : 'OFF') : finalVal;
                console.log("PARAM_SYNC:", v.id, finalVal);
            };
            
            window.currentSettings[v.id] = v.val;
            row.appendChild(input);
            container.appendChild(row);
        }

        function updateParamSuite(type) {
            paramSuite.innerHTML = `<div style="font-weight:bold; margin-bottom:10px; color:#0ff; border-bottom:1px solid #005555; padding-bottom:5px;">` + type + ` SYSTEM VARIABLES</div>`;
            window.currentSettings = {};

            if (type === 'RESEARCH') {
                const inputRow = document.createElement('div');
                inputRow.innerHTML = '<label>Task ID (e.g., TASK_1 to TASK_2700):</label><br><input type="text" id="research-task-id" value="TASK_1" style="width:100%; background:#000; color:#0f0; border:1px solid #005555; margin-top:5px; margin-bottom:5px;">';
                
                const loadBtn = document.createElement('button');
                loadBtn.innerText = 'LOAD RESEARCH PARAMS (15)';
                loadBtn.style = 'width:100%; background:#005555; color:#fff; border:none; margin-bottom:10px; padding:5px; cursor:pointer; font-weight:bold;';
                
                const resultsDiv = document.createElement('div');
                
                loadBtn.onclick = async () => {
                    resultsDiv.innerHTML = '<span style="color:#888;">Fetching hyperparams...</span>';
                    try {
                        const res = await fetch('http://127.0.0.1:8000/api/research-features');
                        const data = await res.json();
                        const taskId = document.getElementById('research-task-id').value;
                        const taskData = data[taskId];
                        if (taskData) {
                            resultsDiv.innerHTML = '';
                            taskData.forEach(v => renderSetting(v, resultsDiv));
                            window.logToConsole('RESEARCH: Loaded parameters for ' + taskId);
                        } else {
                            resultsDiv.innerHTML = '<span style="color:#f00;">Task not found in DB.</span>';
                        }
                    } catch(e) {
                        resultsDiv.innerHTML = '<span style="color:#f00;">Backend API Error. Is it running?</span>';
                    }
                };
                
                paramSuite.appendChild(inputRow);
                paramSuite.appendChild(loadBtn);
                paramSuite.appendChild(resultsDiv);
                return;
            }

            const vars = COMPONENT_VARS[type] || [];
            vars.forEach(v => renderSetting(v, paramSuite));
        }

"@

$start_idx = $content.IndexOf($start_str)
$end_idx = $content.IndexOf($end_str)

if ($start_idx -ne -1 -and $end_idx -ne -1) {
    $new_content = $content.Substring(0, $start_idx) + $new_func + $content.Substring($end_idx)
    Set-Content -Path $html_path -Value $new_content -Encoding UTF8
    Write-Host "HTML Patched successfully!"
} else {
    Write-Host "Failed to find injection points."
}
