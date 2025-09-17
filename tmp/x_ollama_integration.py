import requests

class OllamaAnalyzer:
    def __init__(self, model="mistral"):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model = model

    def analyze_text(self, text, prompt):
        payload = {
            "model": self.model,
            "prompt": f"{prompt}\n\nTexto: {text}",
            "stream": False
        }
        response = requests.post(self.ollama_url, json=payload)
        return response.json().get("response", "Error en Ollama")