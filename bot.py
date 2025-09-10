import os
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import Dispatcher, CommandHandler, CallbackContext

# ========== CONFIG ==========
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # your BotFather token

BOOKS = {
    # Physics
    "hcverma": {"title": "Concepts of Physics - H C Verma", "affiliate_url": "https://www.amazon.in/dp/XXXXXXXX?tag=YOUR_ID"},
    "dc_pandey1": {"title": "DC Pandey Mechanics", "affiliate_url": "https://www.amazon.in/dp/YYYYYYYY?tag=YOUR_ID"},
    "dc_pandey2": {"title": "DC Pandey Electricity & Magnetism", "affiliate_url": "https://www.amazon.in/dp/ZZZZZZZZ?tag=YOUR_ID"},
    "dc_pandey3": {"title": "DC Pandey Modern Physics", "affiliate_url": "https://www.amazon.in/dp/AAAAAAAA?tag=YOUR_ID"},
    "physics_galaxy": {"title": "Physics Galaxy - Ashish Arora", "affiliate_url": "https://www.amazon.in/dp/BBBBBBBB?tag=YOUR_ID"},
    "irodov": {"title": "Problems in General Physics - I.E. Irodov", "affiliate_url": "https://www.amazon.in/dp/CCCCCCCC?tag=YOUR_ID"},
    "ms_chouhan_phy": {"title": "MS Chouhan Physics Problems", "affiliate_url": "https://www.amazon.in/dp/DDDDDDDD?tag=YOUR_ID"},
    "vk_jaiswal_phy": {"title": "VK Jaiswal Physics Practice", "affiliate_url": "https://www.amazon.in/dp/EEEEEEEE?tag=YOUR_ID"},

    # Chemistry
    "ms_chouhan_org": {"title": "MS Chouhan Organic Chemistry", "affiliate_url": "https://www.amazon.in/dp/FFFFFFFF?tag=YOUR_ID"},
    "vk_jaiswal_inorg": {"title": "VK Jaiswal Inorganic Chemistry", "affiliate_url": "https://www.amazon.in/dp/GGGGGGGG?tag=YOUR_ID"},
    "n_avar": {"title": "N. Awasthi Physical Chemistry", "affiliate_url": "https://www.amazon.in/dp/HHHHHHHH?tag=YOUR_ID"},
    "jd_lee": {"title": "JD Lee Inorganic Chemistry", "affiliate_url": "https://www.amazon.in/dp/IIIIIIII?tag=YOUR_ID"},
    "op_tandon": {"title": "O.P. Tandon Physical Chemistry", "affiliate_url": "https://www.amazon.in/dp/JJJJJJJJ?tag=YOUR_ID"},
    "cengage_chem": {"title": "Cengage Chemistry Series", "affiliate_url": "https://www.amazon.in/dp/KKKKKKKK?tag=YOUR_ID"},
    "arihhant_chem": {"title": "Arihant Chemistry Practice", "affiliate_url": "https://www.amazon.in/dp/LLLLLLLL?tag=YOUR_ID"},

    # Mathematics
    "arihant_math1": {"title": "Arihant Algebra", "affiliate_url": "https://www.amazon.in/dp/MMMMMMMM?tag=YOUR_ID"},
    "arihant_math2": {"title": "Arihant Calculus", "affiliate_url": "https://www.amazon.in/dp/NNNNNNNN?tag=YOUR_ID"},
    "arihant_math3": {"title": "Arihant Coordinate Geometry", "affiliate_url": "https://www.amazon.in/dp/OOOOOOOO?tag=YOUR_ID"},
    "cengage_math1": {"title": "Cengage Algebra & Trigonometry", "affiliate_url": "https://www.amazon.in/dp/PPPPPPPP?tag=YOUR_ID"},
    "cengage_math2": {"title": "Cengage Calculus", "affiliate_url": "https://www.amazon.in/dp/QQQQQQQQ?tag=YOUR_ID"},
    "ml_khanna": {"title": "ML Khanna IIT Mathematics", "affiliate_url": "https://www.amazon.in/dp/RRRRRRRR?tag=YOUR_ID"},
    "black_book": {"title": "Black Book - Math for JEE", "affiliate_url": "https://www.amazon.in/dp/SSSSSSSS?tag=YOUR_ID"},
    "arora_math": {"title": "RD Arora Mathematics Practice", "affiliate_url": "https://www.amazon.in/dp/TTTTTTTT?tag=YOUR_ID"},
    "sk_goel": {"title": "SK Goel Problem Solving", "affiliate_url": "https://www.amazon.in/dp/UUUUUUUU?tag=YOUR_ID"},
    "mukherjee": {"title": "Mukherjee JEE Mathematics", "affiliate_url": "https://www.amazon.in/dp/VVVVVVVV?tag=YOUR_ID"},
    "resnick": {"title": "Resnick Halliday for Physics Math", "affiliate_url": "https://www.amazon.in/dp/WWWWWWWW?tag=YOUR_ID"},
    
    # More Physics books
    "halliday": {"title": "Halliday & Resnick Physics", "affiliate_url": "https://www.amazon.in/dp/XXXXXXXX?tag=YOUR_ID"},
    "serway": {"title": "Serway Physics for JEE", "affiliate_url": "https://www.amazon.in/dp/YYYYYYYY?tag=YOUR_ID"},
    "pbhatt": {"title": "P Bahadur Physics", "affiliate_url": "https://www.amazon.in/dp/ZZZZZZZZ?tag=YOUR_ID"},
    "vibrations": {"title": "Vibrations & Waves Books", "affiliate_url": "https://www.amazon.in/dp/AAAAAAAA?tag=YOUR_ID"},

    # More Chemistry books
    "morrison": {"title": "Morrison Boyd Organic Chemistry", "affiliate_url": "https://www.amazon.in/dp/BBBBBBBB?tag=YOUR_ID"},
    "solomons": {"title": "Solomons Organic Chemistry", "affiliate_url": "https://www.amazon.in/dp/CCCCCCCC?tag=YOUR_ID"},
    "paul": {"title": "Paul Organic Chemistry", "affiliate_url": "https://www.amazon.in/dp/DDDDDDDD?tag=YOUR_ID"},

    # More Math books
    "arma": {"title": "Arihant RM Agarwal Math Practice", "affiliate_url": "https://www.amazon.in/dp/EEEEEEEE?tag=YOUR_ID"},
    "gelfand": {"title": "Gelfand Problems for Math Olympiad/JEE", "affiliate_url": "https://www.amazon.in/dp/FFFFFFFF?tag=YOUR_ID"},
    "titu": {"title": "Titu Andreescu Math Problems", "affiliate_url": "https://www.amazon.in/dp/GGGGGGGG?tag=YOUR_ID"},
    "sk_singh": {"title": "SK Singh Mathematics for JEE", "affiliate_url": "https://www.amazon.in/dp/HHHHHHHH?tag=YOUR_ID"},
}

# ============================

app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)

# Telegram command handlers
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hi! I'm JEE Bot 📘. Use /books to get recommended JEE books with links.")

def books(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    buttons = []
    for book_id, data in BOOKS.items():
        buttons.append([InlineKeyboardButton(data["title"], url=data["affiliate_url"])])
    update.message.reply_text(
        "📚 Recommended JEE Books:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("books", books))

# Webhook route
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

# Health check
@app.route("/")
def index():
    return "JEE Bot is running!"

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=PORT)
