
import asyncio
import json
import urllib.request
import time

async def test_ollama():
    model = "smollm:135m"
    prompt = "Hello, respond with 'OLLAMA_OK' if you can hear me."
    options = {"num_ctx": 512, "num_predict": 50, "temperature": 0.7, "num_thread": 1}

    print(f"Testing model: {model}...")
    start_time = time.perf_counter()

    def _call():
        req = urllib.request.Request("http://localhost:11434/api/generate", headers={"Content-Type": "application/json"})
        data = json.dumps({
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": options
        }).encode('utf-8')
        with urllib.request.urlopen(req, data=data, timeout=180.0) as response:
            return json.loads(response.read().decode('utf-8'))

    try:
        raw_res = await asyncio.to_thread(_call)
        latency = time.perf_counter() - start_time
        print(f"Success! Latency: {latency:.2f}s")
        print(f"Response: {raw_res.get('response')}")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_ollama())
