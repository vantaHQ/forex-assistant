from dotenv import load_dotenv
import os
import MetaTrader5 as mt5

load_dotenv()
LOGIN = int(os.getenv("LOGIN"))
PASSWORD = os.getenv("PASSWORD")
SERVER = os.getenv("SERVER")
PATH = os.getenv("PATH")

if not mt5.initialize(path=PATH, login=LOGIN, password=PASSWORD, server=SERVER):
    print("❌ Initialization failed:", mt5.last_error())
else:
    acc = mt5.account_info()
    print(f"✅ Connected to XM MT5 | Account: {acc.login} | Balance: {acc.balance}")
    mt5.shutdown()
