import subprocess


def run_ollama(prompt: str, model: str = "phi") -> str:
    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return result.stdout.decode("utf-8")
    except Exception as e:
        return f"?? Ollama error: {e}"
