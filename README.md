# 📈 EMA Crossover Telegram Bot

Bot ini memantau harga kripto dari Binance dan mengirim sinyal BUY/SELL ke Telegram jika harga menembus EMA 20 atau EMA 50.

## 🔧 Konfigurasi

Edit file `main.py`:

- `BOT_TOKEN`: Token Bot Telegram kamu
- `CHAT_ID`: ID pengguna/channel untuk menerima sinyal
- `SYMBOLS`: Daftar simbol seperti "ETHUSDT"
- `INTERVAL`: Timeframe (misal "15m")
- `RISK_PERCENTAGE`: Persentase resiko (misal 0.01 = 1%)
- `RR_RATIO`: Risk-reward ratio (1:3 default)

## 🚀 Cara Menjalankan

```bash
pip install -r requirements.txt
python main.py
```

## ☁️ Deploy ke Render

- Buat service baru di [https://render.com](https://render.com)
- Pilih **Background Worker**
- Isi `Start Command`: `python main.py`
- Upload file project ke GitHub, lalu sambungkan ke Render
