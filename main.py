from core.forex_assistant import ForexAssistant
from explain import user_chat

if __name__ == "__main__":
    print("🟢 Welcome to your Forex Assistant\n")
    mode = input("Choose mode: (1) Stream + Signal (2) Chat: ")

    if mode == "1":
        assistant = ForexAssistant()
        assistant.connect()
        assistant.stream_and_signal()
        assistant.disconnect()
    elif mode == "2":
        user_chat()
