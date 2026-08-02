import os
import re
import threading
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# 1. Mini Web Server (Utk Hosting Cloud)
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "🤖 KoDIT Bot is Live!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

# 2. Token Bot
TOKEN = "8458357251:AAHn5NalFR5IChhJ1yK9En8oeBkAoaqrus4"

keyboard = ReplyKeyboardMarkup(
    [["📖 Cara Guna", "ℹ️ Tentang KoDIT"]],
    resize_keyboard=True
)

WELCOME = """🕌 Assalamualaikum warahmatullahi wabarakatuh.

Selamat datang ke *KoDIT*
*Kamus Kod Tangan Islam Berasaskan Telegram*

KoDIT membantu pengguna mencari video kod tangan Pendidikan Islam.

Sila taip satu perkataan.
Contoh:
• Alif
• Solat
• Al Quran
• Aurat

🎥 Bot akan memaparkan video yang berkaitan.
"""

CARA = """📖 CARA PENGGUNAAN

1. Taip satu perkataan.
2. Huruf besar/kecil tidak menjadi masalah.
3. Anda juga tidak perlu menaip simbol _

Contoh yang semuanya boleh:
Al Quran
al quran
AL_QURAN
al_quran
"""

ABOUT = """ℹ️ TENTANG KoDIT

KoDIT ialah Kamus Kod Tangan Islam Berasaskan Telegram.

Bot ini membantu guru, murid, ibu bapa dan masyarakat mendapatkan video kod tangan dengan cepat.

Versi: 2.0
"""

def normalize(text: str) -> str:
    text = text.strip().lower()
    text = text.replace("-", " ")
    text = re.sub(r"\s+", "_", text)
    return text

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME, parse_mode="Markdown", reply_markup=keyboard)

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.strip()

    if msg == "📖 Cara Guna":
        await update.message.reply_text(CARA, reply_markup=keyboard)
        return

    if msg == "ℹ️ Tentang KoDIT":
        await update.message.reply_text(ABOUT, reply_markup=keyboard)
        return

    filename = normalize(msg) + ".mp4"
    path = os.path.join("videos", filename)

    if os.path.exists(path):
        with open(path, "rb") as v:
            await update.message.reply_video(v)
    else:
        await update.message.reply_text(
            f"❌ Maaf, video bagi '{msg}' belum tersedia dalam KoDIT.",
            reply_markup=keyboard,
        )

# 3. Mula Jalankan Bot
print("🤖 Memulakan bot KoDIT...")

# Jalankan Flask Server di latar belakang
threading.Thread(target=run_flask, daemon=True).start()

# Jalankan Telegram Application
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("✅ Bot KoDIT V2.0 sedia dan sedang berjalan!")
app.run_polling()