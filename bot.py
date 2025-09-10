import os
import sqlite3
import threading
from flask import Flask, redirect
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ========== CONFIG ==========
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # will be set in Render
PUBLIC_DOMAIN = os.environ.get("PUBLIC_DOMAIN")  # will be set in Render

BOOKS = {
    # 📘 Physics
    "hcverma": {
        "title": "Concepts of Physics - H C Verma",
        "affiliate_url": "https://www.amazon.in/dp/XXXXXXXX?tag=YOUR_ID"
    },
    "dc_pandey": {
        "title": "DC Pandey Objective Physics (Arihant)",
        "affiliate_url": "https://www.amazon.in/dp/YYYYYYYY?tag=YOUR_ID"
    },
    "physics_galaxy": {
        "title": "Physics Galaxy - Ashish Arora",
        "affiliate_url": "https://www.amazon.in/dp/ZZZZZZZZ?tag=YOUR_ID"
    },
    "irodov": {
        "title": "Problems in General Physics - I.E. Irodov",
        "affiliate_url": "https://www.amazon.in/dp/AAAAAAAA?tag=YOUR_ID"
    },

    # 🔬 Chemistry
    "ms_chouhan": {
        "title": "MS Chouhan - Organic Chemistry Problems",
        "affiliate_url": "https://www.amazon.in/dp/BBBBBBBB?tag=YOUR_ID"
    },
    "vk_jaiswal": {
        "title": "VK Jaiswal - Inorganic Chemistry Problems",
        "affiliate_url": "https://www.amazon.in/dp/CCCCCCCC?tag=YOUR_ID"
    },
    "n_avar": {
        "title": "N. Awasthi - Physical Chemistry Problems",
        "affiliate_url": "https://www.amazon.in/dp/DDDDDDDD?tag=YOUR_ID"
    },
    "jd_lee": {
        "title": "JD Lee - Concise Inorganic Chemistry (Adapted for JEE)",
        "affiliate_url": "https://www.amazon.in/dp/EEEEEEEE?tag=YOUR_ID"
    },
    "op_tandon": {
        "title": "O.P. Tandon - Physical Chemistry",
        "affiliate_url": "https://www.amazon.in/dp/FFFFFFFF?tag=YOUR_ID"
    },

    # 📐 Mathematics
    "arihant_math": {
        "title": "Arihant Skills in Mathematics Series",
        "affiliate_url": "https://www.amazon.in/dp/GGGGGGGG?tag=YOUR_ID"
    },
    "cengage_math": {
        "title": "Cengage Mathematics Complete Set",
        "affiliate_url": "https://www.amazon.in/dp/HHHHHHHH?tag=YOUR_ID"
    },
    "ml_khanna": {
        "title": "ML Khanna - IIT Mathematics",
        "affiliate_url": "https://www.amazon.in/dp/IIIIIIII?tag=YOUR_ID"
    },
    "black_book": {
        "title": "Black Book - Mathematics for JEE Advanced",
        "affiliate_url": "https://www.amazon.in/dp/JJJJJJJJ?tag=YOUR_ID"
    },
}
# ============================

DB_PATH = "bot_data.sqlite"

def init_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS clicks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id TEXT,
        chat_id INTEGER,
        clicked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit()
    return conn

db_conn = init_db()

# Flask redirect app
app = Flask(__name__)

@app.route("/r/<book_id>/<int:chat_id>")
def redirect_and_log(book_id, chat_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO clicks (book_id, chat_id) VALUES (?, ?)", (book_id, chat_id))
    conn.commit()
    conn.close()

    entry = BOOKS.get(book_id)
    if not entry:
        return "Invalid book", 404
    return redirect(entry["affiliate_url"], code=302)

def run_flask():
    app.run(host="0.0.0.0", port=10000)

# Telegram bot handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        update.effective_chat.id,
        "Hi! I'm JEE Bot 📘. Use /books to get recommended JEE books with links."
    )

async def books_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    buttons = []
    for book_id, data in BOOKS.items():
        url = f"{PUBLIC_DOMAIN}/r/{book_id}/{chat_id}"
        buttons.append([InlineKeyboardButton(text=data["title"], url=url)])
    await context.bot.send_message(
        chat_id,
        "📚 Recommended JEE Books:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

def main():
    # Run Flask in background thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Run Telegram bot
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("books", books_cmd))
    app_bot.run_polling()

if __name__ == "__main__":
    main()
