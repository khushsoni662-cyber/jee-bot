import os
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

# ================= CONFIG =================
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # Your BotFather token
PAGE_SIZE = 10  # Number of books per page

# Categorized books
BOOKS = {
    "Physics": [
        {"title": "Concepts of Physics - H C Verma", "url": "https://www.amazon.in/dp/XXXXXXXX?tag=YOUR_AFFILIATE_ID"},
        {"title": "DC Pandey Mechanics", "url": "https://www.amazon.in/dp/YYYYYYYY?tag=YOUR_AFFILIATE_ID"},
        {"title": "DC Pandey Electricity & Magnetism", "url": "https://www.amazon.in/dp/ZZZZZZZZ?tag=YOUR_AFFILIATE_ID"},
        {"title": "Physics Galaxy - Ashish Arora", "url": "https://www.amazon.in/dp/BBBBBBBB?tag=YOUR_AFFILIATE_ID"},
        {"title": "I.E. Irodov Problems", "url": "https://www.amazon.in/dp/CCCCCCCC?tag=YOUR_AFFILIATE_ID"},
        {"title": "MS Chouhan Physics Problems", "url": "https://www.amazon.in/dp/DDDDDDDD?tag=YOUR_AFFILIATE_ID"},
        {"title": "VK Jaiswal Physics Practice", "url": "https://www.amazon.in/dp/EEEEEEEE?tag=YOUR_AFFILIATE_ID"},
        {"title": "Halliday & Resnick Physics", "url": "https://www.amazon.in/dp/FFFFFFFF?tag=YOUR_AFFILIATE_ID"},
        {"title": "Serway Physics for JEE", "url": "https://www.amazon.in/dp/GGGGGGGG?tag=YOUR_AFFILIATE_ID"},
    ],
    "Chemistry": [
        {"title": "MS Chouhan Organic Chemistry", "url": "https://www.amazon.in/dp/HHHHHHHH?tag=YOUR_AFFILIATE_ID"},
        {"title": "VK Jaiswal Inorganic Chemistry", "url": "https://www.amazon.in/dp/IIIIIIII?tag=YOUR_AFFILIATE_ID"},
        {"title": "N. Awasthi Physical Chemistry", "url": "https://www.amazon.in/dp/JJJJJJJJ?tag=YOUR_AFFILIATE_ID"},
        {"title": "JD Lee Inorganic Chemistry", "url": "https://www.amazon.in/dp/KKKKKKKK?tag=YOUR_AFFILIATE_ID"},
        {"title": "O.P. Tandon Physical Chemistry", "url": "https://www.amazon.in/dp/LLLLLLLL?tag=YOUR_AFFILIATE_ID"},
        {"title": "Cengage Chemistry Series", "url": "https://www.amazon.in/dp/MMMMMMMM?tag=YOUR_AFFILIATE_ID"},
        {"title": "Arihant Chemistry Practice", "url": "https://www.amazon.in/dp/NNNNNNNN?tag=YOUR_AFFILIATE_ID"},
        {"title": "Morrison Boyd Organic Chemistry", "url": "https://www.amazon.in/dp/OOOOOOOO?tag=YOUR_AFFILIATE_ID"},
        {"title": "Solomons Organic Chemistry", "url": "https://www.amazon.in/dp/PPPPPPPP?tag=YOUR_AFFILIATE_ID"},
        {"title": "Paul Organic Chemistry", "url": "https://www.amazon.in/dp/QQQQQQQQ?tag=YOUR_AFFILIATE_ID"},
    ],
    "Mathematics": [
        {"title": "Arihant Algebra", "url": "https://www.amazon.in/dp/RRRRRRRR?tag=YOUR_AFFILIATE_ID"},
        {"title": "Arihant Calculus", "url": "https://www.amazon.in/dp/SSSSSSSS?tag=YOUR_AFFILIATE_ID"},
        {"title": "Arihant Coordinate Geometry", "url": "https://www.amazon.in/dp/TTTTTTTT?tag=YOUR_AFFILIATE_ID"},
        {"title": "Cengage Algebra & Trigonometry", "url": "https://www.amazon.in/dp/UUUUUUUU?tag=YOUR_AFFILIATE_ID"},
        {"title": "Cengage Calculus", "url": "https://www.amazon.in/dp/VVVVVVVV?tag=YOUR_AFFILIATE_ID"},
        {"title": "ML Khanna IIT Mathematics", "url": "https://www.amazon.in/dp/WWWWWWWW?tag=YOUR_AFFILIATE_ID"},
        {"title": "Black Book - Math for JEE", "url": "https://www.amazon.in/dp/XXXXXXXX?tag=YOUR_AFFILIATE_ID"},
        {"title": "RD Arora Mathematics Practice", "url": "https://www.amazon.in/dp/YYYYYYYY?tag=YOUR_AFFILIATE_ID"},
        {"title": "SK Goel Problem Solving", "url": "https://www.amazon.in/dp/ZZZZZZZZ?tag=YOUR_AFFILIATE_ID"},
        {"title": "Mukherjee JEE Mathematics", "url": "https://www.amazon.in/dp/AAAAAAAA?tag=YOUR_AFFILIATE_ID"},
        {"title": "Resnick Halliday for Physics Math", "url": "https://www.amazon.in/dp/BBBBBBBB?tag=YOUR_AFFILIATE_ID"},
        {"title": "Arihant RM Agarwal Math Practice", "url": "https://www.amazon.in/dp/CCCCCCCC?tag=YOUR_AFFILIATE_ID"},
        {"title": "Gelfand Problems for Math Olympiad/JEE", "url": "https://www.amazon.in/dp/DDDDDDDD?tag=YOUR_AFFILIATE_ID"},
        {"title": "Titu Andreescu Math Problems", "url": "https://www.amazon.in/dp/EEEEEEEE?tag=YOUR_AFFILIATE_ID"},
        {"title": "SK Singh Mathematics for JEE", "url": "https://www.amazon.in/dp/FFFFFFFF?tag=YOUR_AFFILIATE_ID"},
    ]
}

# ============================

app = Flask(__name__)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! I'm JEE Bot 📘.\nUse /books to choose a subject and see recommended JEE books."
    )

# /books command — show categories
async def books(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [[InlineKeyboardButton(category, callback_data=f"cat:{category}:0")] for category in BOOKS.keys()]
    await update.message.reply_text(
        "📚 Select a category:", reply_markup=InlineKeyboardMarkup(buttons)
    )

# Callback for category buttons and pagination
async def category_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data  # format: cat:<category>:<page>
    if not data.startswith("cat:"):
        return
    _, category, page_str = data.split(":")
    page = int(page_str)
    books_list = BOOKS[category]
    start_idx = page * PAGE_SIZE
    end_idx = start_idx + PAGE_SIZE
    buttons = [[InlineKeyboardButton(book["title"], url=book["url"])] for book in books_list[start_idx:end_idx]]

    # Add navigation buttons
    nav_buttons = []
    if start_idx > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"cat:{category}:{page-1}"))
    if end_idx < len(books_list):
        nav_buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"cat:{category}:{page+1}"))
    if nav_buttons:
        buttons.append(nav_buttons)

    await query.edit_message_text(
        text=f"📖 {category} Books (Page {page+1}):",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# Build Telegram app
from telegram.ext import Application
application = Application.builder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("books", books))
application.add_handler(CallbackQueryHandler(category_callback))

# Flask webhook route
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    from telegram import Update
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put(update)
    return "OK"

# Health check
@app.route("/")
def index():
    return "JEE Bot running!"

# Run Flask
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)
