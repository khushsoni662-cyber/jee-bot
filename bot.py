@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    # Process update synchronously
    import asyncio
    asyncio.run(application.process_update(update))
    return "OK"
