import requests
import os

LLM_MODEL    = os.environ.get("LLM_MODEL", "llama3.2:3b")
LLM_API_KEY  = os.environ.get("LLM_API_KEY", "")
LLM_BASE_URL = os.environ.get("LLM_BASE_URL", "http://localhost:11434/api")
EMBED_MODEL  = os.environ.get("EMBED_MODEL", "embeddinggemma")
EMBED_BASE_URL = os.environ.get("EMBED_BASE_URL", "http://localhost:11434/api")


def embed(text):
    r = requests.post(
        f"{EMBED_BASE_URL}/embeddings",
        json={"model": EMBED_MODEL, "prompt": text}
    )
    return r.json()["embedding"]


def generate(prompt):
    headers = {"Content-Type": "application/json"}
    if LLM_API_KEY:
        headers["Authorization"] = f"Bearer {LLM_API_KEY}"

    if "localhost" in LLM_BASE_URL or "127.0.0.1" in LLM_BASE_URL:
        r = requests.post(
            f"{LLM_BASE_URL}/generate",
            headers=headers,
            json={"model": LLM_MODEL, "prompt": prompt, "stream": False}
        )
        return r.json()["response"]
    else:
        r = requests.post(
            f"{LLM_BASE_URL}/chat/completions",
            headers=headers,
            json={
                "model": LLM_MODEL,
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        return r.json()["choices"][0]["message"]["content"]