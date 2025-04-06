import requests
import pandas as pd
import time

# Ganti dengan token & chat ID kamu
BOT_TOKEN = "8115228898:AAEQGo5YFvXfislxi8l7yzkFPdnogN4CNcA"
CHAT_ID = "kenko_bot"

# Konfigurasi
SYMBOLS = ["ETHUSDT", "SOLUSDT", "XRPUSDT"]
INTERVAL = "15m"
LIMIT = 100
RR_RATIO = 3
RISK_PERCENTAGE = 0.01
SLEEP_TIME = 300  # 5 menit

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, json=payload)

def fetch_candles(symbol):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={INTERVAL}&limit={LIMIT}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])
    df['close'] = df['close'].astype(float)
    return df

def analyze(symbol):
    df = fetch_candles(symbol)
    df['EMA20'] = df['close'].ewm(span=20).mean()
    df['EMA50'] = df['close'].ewm(span=50).mean()

    current_price = df['close'].iloc[-1]
    prev_price = df['close'].iloc[-2]
    ema20_now = df['EMA20'].iloc[-1]
    ema20_prev = df['EMA20'].iloc[-2]
    ema50_now = df['EMA50'].iloc[-1]
    ema50_prev = df['EMA50'].iloc[-2]

    signal = None
    basis = None

    if prev_price < ema20_prev and current_price > ema20_now:
        signal = "BUY"
        basis = "EMA 20"
    elif prev_price > ema20_prev and current_price < ema20_now:
        signal = "SELL"
        basis = "EMA 20"
    elif prev_price < ema50_prev and current_price > ema50_now:
        signal = "BUY"
        basis = "EMA 50"
    elif prev_price > ema50_prev and current_price < ema50_now:
        signal = "SELL"
        basis = "EMA 50"

    if signal:
        entry = current_price
        risk = entry * RISK_PERCENTAGE

        if signal == "BUY":
            sl = entry - risk
            tp = entry + (risk * RR_RATIO)
        else:
            sl = entry + risk
            tp = entry - (risk * RR_RATIO)

        msg = f"""📊 {signal} Signal for {symbol}
Basis: {basis}
Entry: ${entry:.2f}
SL: ${sl:.2f}
TP: ${tp:.2f}"""
        send_telegram_message(msg)

def run():
    while True:
        for symbol in SYMBOLS:
            try:
                analyze(symbol)
            except Exception as e:
                print(f"Error for {symbol}: {e}")
        time.sleep(SLEEP_TIME)

if __name__ == "__main__":
    run()
