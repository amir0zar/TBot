import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext
import sqlite3

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Database handling functions

def get_available_config(config_type, category):
    """Fetch an unused config from the database."""
    conn = sqlite3.connect('configs.db')  # Your .sql file path
    cursor = conn.cursor()
    
    # Query to get the first available config
    cursor.execute("""
        SELECT id, config_data FROM configs 
        WHERE type = ? AND category = ? AND used = 0
        LIMIT 1
    """, (config_type, category))
    
    config = cursor.fetchone()
    conn.close()
    
    return config

def mark_config_as_used(config_id):
    """Mark a config as used after delivery."""
    conn = sqlite3.connect('configs.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE configs SET used = 1 WHERE id = ?
    """, (config_id,))
    
    conn.commit()
    conn.close()

# Bot command handlers

async def start(update: Update, context: CallbackContext) -> None:
    """Sends a message with several buttons."""
    keyboard = [
        [InlineKeyboardButton("خرید کانفیگ", callback_data="buy_config")],
        [InlineKeyboardButton("آموزش های مورد نیاز", callback_data="tutorials")],
        [InlineKeyboardButton("نرم افزار های مورد نیاز", callback_data="software")],
        [InlineKeyboardButton("تماس با ما", callback_data="contact")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome! Choose an option:", reply_markup=reply_markup)

async def handle_buy_specific(query, context, category, config_type):
    """Handle specific config purchase requests."""
    config = get_available_config(config_type, category)
    
    if config:
        config_id, config_data = config
        await query.message.reply_text(f"Your config: {config_data}")
        mark_config_as_used(config_id)  # Mark the config as used
    else:
        await query.message.reply_text("No available configs in this category.")

async def handle_buy_config(query, context):
    """Display config categories for the user to choose from."""
    keyboard = [
        [InlineKeyboardButton("1 user - 1 month", callback_data="buy_1u_1m")],
        [InlineKeyboardButton("1 user - 2 months", callback_data="buy_1u_2m")],
        [InlineKeyboardButton("1 user - 3 months", callback_data="buy_1u_3m")],
        [InlineKeyboardButton("2 users - 1 month", callback_data="buy_2u_1m")],
        [InlineKeyboardButton("2 users - 2 months", callback_data="buy_2u_2m")],
        [InlineKeyboardButton("2 users - 3 months", callback_data="buy_2u_3m")],
        [InlineKeyboardButton("Back", callback_data="back")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Select a category:", reply_markup=reply_markup)

async def button_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "buy_config":
        await handle_buy_config(query, context)
    elif query.data == "buy_1u_1m":
        await handle_buy_specific(query, context, "1 user - 1 month", "v2ray")
    elif query.data == "buy_1u_2m":
        await handle_buy_specific(query, context, "1 user - 2 months", "v2ray")
    elif query.data == "buy_1u_3m":
        await handle_buy_specific(query, context, "1 user - 3 months", "v2ray")
    elif query.data == "buy_2u_1m":
        await handle_buy_specific(query, context, "2 users - 1 month", "ssh")
    elif query.data == "buy_2u_2m":
        await handle_buy_specific(query, context, "2 users - 2 months", "ssh")
    elif query.data == "buy_2u_3m":
        await handle_buy_specific(query, context, "2 users - 3 months", "ssh")
    elif query.data == "back":
        await start(query, context)

async def main() -> None:
    """Start the bot."""
    application = Application.builder().token("YOUR_BOT_TOKEN").build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_click))
    
    # Start the bot
    await application.start()
    await application.idle()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
