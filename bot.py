import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Sample categorized books
BOOKS = {
    "Physics": [
        {"title": "H C Verma Concepts of Physics", "url": "https://www.amazon.in/dp/XXXXXXXX?tag=YOUR_AFFILIATE_ID"},
        {"title": "DC Pandey Mechanics", "url": "https://www.amazon.in/dp/YYYYYYYY?tag=YOUR_AFFILIATE_ID"},
    ],
    "Chemistry": [
        {"title": "MS Chouhan Organic Chemistry", "url": "https://www.amazon.in/dp/HHHHHHHH?tag=YOUR_AFFILIATE_ID"},
    ],
    "Mathematics": [
        {"title": "Arihant Algebra", "url": "https://www.amazon.in/dp/RRRRRRRR?tag=YOUR_AFFILIATE_ID"},
    ]
}

# ---------------- Handlers ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is working! Use /books to see categories.")

async def books(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [[InlineKeyboardButton(cat, callback_data=f"cat:{cat}:0")] for cat in BOOKS.keys()]
    await update.message.reply_text("📚 Choose a category:", reply_markup=InlineKeyboardMarkup(buttons))

async def category_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data.split(":")
    category, page = data[1], int(data[2])
    books_list = BOOKS[category]
    buttons = [[InlineKeyboardButton(b["title"], url=b["url"])] for b in books_list]
    await query.edit_message_text(f"📖 {category} Books:", reply_markup=InlineKeyboardMarkup(buttons))

# ---------------- Build app ----------------

application = Application.builder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("books", books))
application.add_handler(CallbackQueryHandler(category_callback))

# ---------------- Run bot ----------------
if __name__ == "__main__":
    print("Bot is starting...")
    application.run_polling()
