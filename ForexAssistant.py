import MetaTrader5 as mt5
from datetime import datetime
import pandas as pd
import time


class ForexAssistant:
    def __init__(self, symbol="EURUSD", timeframe=mt5.TIMEFRAME_M1):
        self.symbol = symbol
        self.timeframe = timeframe
        self.initialized = False

    def connect(self):
        self.initialized = mt5.initialize()
        if not self.initialized:
            raise Exception(f"Failed to connect: {mt5.last_error()}")
        print("[✓] MT5 Initialized")

    def disconnect(self):
        mt5.shutdown()
        print("[✓] MT5 Shutdown")

    def get_tick(self):
        return mt5.symbol_info_tick(self.symbol)

    def get_ohlc(self, n=100):
        rates = mt5.copy_rates_from_pos(self.symbol, self.timeframe, 0, n)
        return pd.DataFrame(rates)

    def calculate_signals(self, df):
        df["ema_fast"] = df["close"].ewm(span=5).mean()
        df["ema_slow"] = df["close"].ewm(span=20).mean()
        if (
            df["ema_fast"].iloc[-1] > df["ema_slow"].iloc[-1]
            and df["ema_fast"].iloc[-2] < df["ema_slow"].iloc[-2]
        ):
            return "BUY"
        elif (
            df["ema_fast"].iloc[-1] < df["ema_slow"].iloc[-1]
            and df["ema_fast"].iloc[-2] > df["ema_slow"].iloc[-2]
        ):
            return "SELL"
        return "HOLD"

    def stream_and_signal(self, interval=5):
        print(f"Streaming {self.symbol} every {interval}s...")
        while True:
            df = self.get_ohlc(50)
            signal = self.calculate_signals(df)
            print(f"{datetime.now().strftime('%H:%M:%S')} — Signal: {signal}")
            time.sleep(interval)
