import os
import json
import hashlib
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
is_vercel = os.environ.get("VERCEL") == "1"
CACHE_FILE = "/tmp/cache.json" if is_vercel else "cache.json"

def carregar_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_cache(cache_data):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache_data, f, ensure_ascii=False, indent=4)

def gerar_hash_prompt(prompt):
    return hashlib.md5(prompt.encode("utf-8")).hexdigest()

def chamar_api_gemini(prompt):
    cache = carregar_cache()
    prompt_hash = gerar_hash_prompt(prompt)

    # Verifica se a resposta já existe no cache
    if prompt_hash in cache:
        print("\n*INFO* Retornando resposta do cache...")
        return cache[prompt_hash]

    print("\n*INFO* Chamando API do Gemini...")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7}
    }

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        try:
            texto_gerado = data["candidates"][0]["content"]["parts"][0]["text"]
            # Salva no cache antes de retornar
            cache[prompt_hash] = texto_gerado
            salvar_cache(cache)
            return texto_gerado
        except (KeyError, IndexError):
            return "Erro ao processar a estrutura de resposta da API."
    else:
        return f"Erro na API: Status Code {response.status_code} - {response.text}"