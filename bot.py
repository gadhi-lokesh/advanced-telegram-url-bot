
import asyncio
import logging

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from config import BOT_TOKEN

from database import (
    create_database,
    save_user,
    save_url,
    get_history,
    get_stats
)

from url_shortener import shorten_url, validate_url


logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# Save user information
def register_user(user):

    save_user(
        user.id,
        user.username,
        user.first_name
    )


# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    register_user(user)

    message = (
        "Welcome to Advanced URL Shortener Bot!\n\n"
        "I can shorten your long URLs using multiple APIs.\n\n"
        "Commands:\n"
        "/start - Start bot\n"
        "/help - Instructions\n"
        "/shorten - Shorten URL\n"
        "/history - URL history\n"
        "/stats - Your statistics\n\n"
        "Send any valid URL to get started."
    )

    await update.message.reply_text(message)


# Help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = (
        "URL Shortener Bot Help\n\n"
        "Method 1:\n"
        "Send a URL directly.\n\n"
        "Method 2:\n"
        "/shorten https://example.com\n\n"
        "If one API fails, another API will be tried automatically."
    )

    await update.message.reply_text(message)


# Main URL processing function
async def process_url(update: Update, url: str):

    user = update.effective_user

    register_user(user)

    if not validate_url(url):

        await update.message.reply_text(
            "Invalid URL!\n"
            "Please provide a valid HTTP or HTTPS URL."
        )

        return

    status_message = await update.message.reply_text(
        "Processing your URL...\nTrying available services."
    )

    try:

        result = await asyncio.to_thread(
            shorten_url,
            url
        )

        if result["success"]:

            short_url = result["short_url"]
            provider = result["provider"]

            save_url(
                user.id,
                url,
                short_url,
                provider
            )

            message = (
                "URL shortened successfully!\n\n"
                f"Original URL:\n{url}\n\n"
                f"Short URL:\n{short_url}\n\n"
                f"Provider: {provider}"
            )

            await status_message.edit_text(message)

        else:

            await status_message.edit_text(
                "All shortening services failed.\n"
                "Please try again later."
            )

            logger.warning(
                "All APIs failed: %s",
                result["errors"]
            )

    except Exception:

        logger.exception("URL processing error")

        await status_message.edit_text(
            "Something went wrong. Please try again."
        )


# Shorten command
async def shorten_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:

        await update.message.reply_text(
            "Usage:\n/shorten https://example.com"
        )

        return

    url = " ".join(context.args).strip()

    await process_url(update, url)


# Receive normal messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = update.message.text.strip()

    await process_url(update, url)


# URL history
async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    records = get_history(user_id)

    if not records:

        await update.message.reply_text(
            "You have not shortened any URLs yet."
        )

        return

    message = "Your Recent URL History\n\n"

    for index, record in enumerate(records, 1):

        original, short, provider, created = record

        message += (
            f"{index}. {short}\n"
            f"Original: {original}\n"
            f"Provider: {provider}\n"
            f"Date: {created}\n\n"
        )

    await update.message.reply_text(message)


# Statistics
async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    total = get_stats(user_id)

    await update.message.reply_text(
        "Your Statistics\n\n"
        f"Total URLs shortened: {total}"
    )


# Error handler
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):

    logger.error(
        "An error occurred while processing an update",
        exc_info=context.error
    )


# Main function
def main():

    if not BOT_TOKEN:
        raise RuntimeError("Bot token is missing.")

    create_database()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("shorten", shorten_command))
    app.add_handler(CommandHandler("history", history_command))
    app.add_handler(CommandHandler("stats", stats_command))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    app.add_error_handler(error_handler)

    print("Advanced Telegram URL Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
