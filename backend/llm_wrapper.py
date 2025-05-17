import os
import requests

def get_llm_response(prompt: str, tools: dict = {}) -> str:
    backend = os.getenv("LLM_BACKEND", "openai").lower()

    if backend == "ollama":
        model = os.getenv("OLLAMA_MODEL", "llama3")
        response = requests.post(
            "http://host.docker.internal:11434/api/generate",
            json={"model": model, "prompt": prompt},
            timeout=30,
        ).json()
        return response.get("response", "").strip()

    elif backend == "openai":
        from openai import OpenAI

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
        )
        return response.choices[0].message.content.strip()

    else:
        return f"Unknown LLM backend: {backend}"


# Alias for compatibility with main.py
def call_llm(prompt: str) -> str:
    return get_llm_response(prompt)