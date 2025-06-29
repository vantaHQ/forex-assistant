import os
import asyncio
import requests
import streamlit as st
import pandas as pd
from datetime import datetime
from core.forex_assistant import ForexAssistant
from explain import explain_signal
from modules import indicators

# === Configuration ===
MODE = st.sidebar.radio(
    "📍 Select Mode", ["Live Trading", "Backtesting"], key="mode_toggle"
)
AUTO_MODE = st.sidebar.toggle("🚀 Auto-Trading ON/OFF", key="auto_toggle")
history_path = "data/trade_log.csv"
os.makedirs("data", exist_ok=True)

bot_token = "7672519259:AAHTcgUf9UWrA4dMIi2midSwoGBwHJnrb90"
chat_id = 7063103001  # e.g. 123456789

# === Initialize Assistant ===
assistant = ForexAssistant()
assistant.connect()
df = assistant.get_ohlc()


# === Utility Functions ===
def log_trade(action, volume, mode, price):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = f"{now},{action.upper()},{volume},{mode},{price:.5f}\n"
    with open(history_path, "a") as f:
        f.write(row)


def send_telegram_alert(message, token, chat_id):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            st.warning(f"Telegram alert failed: {response.text}")
    except Exception as e:
        st.warning(f"Error sending Telegram alert: {e}")


async def auto_trade_loop():
    while st.session_state.get("auto_trading", False):
        df = assistant.get_ohlc()
        signal = assistant.calculate_signals(df)
        last_price = df["close"].iloc[-1]

        if signal in ["BUY", "SELL"]:
            explanation = explain_signal(
                f"Signal: {signal}, RSI: {df['rsi'].iloc[-1]:.2f}, "
                f"EMA5: {df['ema5'].iloc[-1]:.5f}, EMA20: {df['ema20'].iloc[-1]:.5f}"
            )
            if MODE == "Live Trading":
                result = assistant.place_market_order(signal.lower(), volume=0.05)
                status = f"{signal} Executed – Retcode: {result.retcode}"
            else:
                status = f"Simulated {signal} in Backtest mode"

            log_trade(signal, 0.05, MODE, last_price)
            send_telegram_alert(
                f"💹 {status}\n{assistant.symbol} @ {last_price:.5f}\n🧠 {explanation}",
                bot_token,
                chat_id,
            )
            st.toast(status)

        await asyncio.sleep(60)


# === Auto Mode Activation ===
if AUTO_MODE and not st.session_state.get("auto_trading"):
    st.session_state.auto_trading = True
    asyncio.run(auto_trade_loop())
elif not AUTO_MODE and st.session_state.get("auto_trading"):
    st.session_state.auto_trading = False
    st.info("⏹️ Auto-Trading paused")

# === UI Tabs ===
tab1, tab2, tab3, tab4 = st.tabs(
    ["Market View", "Signal Insight", "Ask Assistant", "Trade Log"]
)

with tab1:
    st.subheader("📈 Price Chart with EMAs")
    assistant_df = df.copy()
    assistant_df["EMA5"] = indicators.ema(assistant_df, 5)
    assistant_df["EMA20"] = indicators.ema(assistant_df, 20)
    st.line_chart(assistant_df[["close", "EMA5", "EMA20"]])

    st.subheader("📉 RSI")
    assistant_df["RSI"] = indicators.rsi(assistant_df)
    st.line_chart(assistant_df["RSI"])

with tab2:
    signal = assistant.calculate_signals(df)
    st.metric("Current Signal", signal)

    if signal in ["BUY", "SELL"]:
        prompt = f"""
        Signal: {signal}
        - RSI: {df['rsi'].iloc[-1]:.2f}
        - EMA5: {df['ema5'].iloc[-1]:.5f}
        - EMA20: {df['ema20'].iloc[-1]:.5f}
        Explain this recommendation.
        """
        commentary = explain_signal(prompt)
        st.markdown("🧠 **Ollama Insight**")
        st.write(commentary)

    volume = st.slider("Select Trade Volume", 0.01, 1.0, 0.01, 0.01)
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📈 Buy Now", key="buy_btn"):
            price = df["close"].iloc[-1]
            if MODE == "Live Trading":
                result = assistant.place_market_order("buy", volume)
                st.success(f"✅ LIVE BUY → Retcode: {result.retcode}")
            else:
                st.info("Simulated BUY in Backtest Mode.")
            log_trade("BUY", volume, MODE, price)
            send_telegram_alert(
                f"📈 BUY {assistant.symbol} @ {price:.5f}", bot_token, chat_id
            )

    with col2:
        if st.button("📉 Sell Now", key="sell_btn"):
            price = df["close"].iloc[-1]
            if MODE == "Live Trading":
                result = assistant.place_market_order("sell", volume)
                st.success(f"✅ LIVE SELL → Retcode: {result.retcode}")
            else:
                st.info("Simulated SELL in Backtest Mode.")
            log_trade("SELL", volume, MODE, price)
            send_telegram_alert(
                f"📉 SELL {assistant.symbol} @ {price:.5f}", bot_token, chat_id
            )

with tab3:
    st.subheader("🤖 Ask Ollama Anything")
    user_input = st.text_area("Ask about this symbol or strategy...")
    if st.button("🧠 Get Response", key="ollama_btn") and user_input:
        response = explain_signal(user_input)
        st.markdown("### Ollama says:")
        st.write(response)

with tab4:
    st.subheader("📘 Trade History Log")
    if os.path.exists(history_path):
        hist_df = pd.read_csv(
            history_path, names=["Time", "Action", "Volume", "Mode", "Price"]
        )
        st.dataframe(hist_df[::-1])
    else:
        st.info("No trades logged yet.")
