def explain_signal(prompt):
    # Simulated LLM response (replace with actual Ollama connection if needed)
    if "BUY" in prompt:
        return "RSI is below 30 and EMA5 has crossed above EMA20 — conditions suggest bullish momentum."
    elif "SELL" in prompt:
        return "RSI is above 70 and EMA5 is below EMA20 — indicating bearish pressure may increase."
    else:
        return "No strong signal detected — market trend appears neutral."
