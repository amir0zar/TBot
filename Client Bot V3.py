from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
)

# Your bot token
TOKEN = "7502162456:AAGSW83AB6wk9kiaUdzC6OROWke-9vY6CL8"


# Function to update user context with the previous page
def set_last_page(context, page_name):
    context.user_data["last_page"] = page_name


# Function to get the last page from the context
def get_last_page(context):
    return context.user_data.get("last_page", None)


async def start(update: Update, context: CallbackContext) -> None:
    """Handles the /start command, presenting the initial options to the user."""
    set_last_page(context, "start")

    keyboard = [
        [InlineKeyboardButton("خرید کانفیگ", callback_data="buy_config")],
        [InlineKeyboardButton("آموزش های مورد نیاز", callback_data="tutorial")],
        [InlineKeyboardButton("نرم افزار های مورد نیاز", callback_data="software")],
        [InlineKeyboardButton("تماس با ما", callback_data="contact")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "به ربات ------ خوش آمدید! لیست قیمت ها به شکل زیر است: ",
        reply_markup=reply_markup,
    )


async def button_click(update: Update, context: CallbackContext) -> None:
    """Handles button clicks and triggers appropriate actions."""
    query = update.callback_query
    await query.answer()

    if query.data == "back":
        last_page = get_last_page(context)
        if last_page == "tutorial":
            await handle_tutorial(query, context)
        elif last_page == "software":
            await handle_software(query, context)
        elif last_page == "contact":
            await handle_contact(query, context)
        elif last_page == "buy_config":
            await handle_buy_config(query, context)
        else:
            await start(query, context)
    elif query.data == "tutorial":
        set_last_page(context, "tutorial")
        await handle_tutorial(query, context)
    elif query.data == "software":
        set_last_page(context, "software")
        await handle_software(query, context)
    elif query.data == "contact":
        set_last_page(context, "contact")
        await handle_contact(query, context)
    elif query.data == "buy_config":
        set_last_page(context, "buy_config")
        await handle_buy_config(query, context)
    elif query.data == "send_v2ray_video":
        await send_v2ray_video(update, context)
    elif query.data == "send_ssh_video":
        await send_ssh_video(update, context)
    elif query.data == "send_v2ray_apk":
        await send_v2ray_apk(update, context)
    elif query.data == "send_ssh_apk":
        await send_ssh_apk(update, context)
    elif query.data.startswith("buy_"):
        await handle_buy_specific(query, context)
    elif query.data.startswith("config_"):
        await handle_config_payment(query, context)


async def handle_tutorial(query, context):
    """Handles the TUTORIAL button click and uploads videos."""
    keyboard = [
        [InlineKeyboardButton("V2RAY-NG", callback_data="send_v2ray_video")],
        [InlineKeyboardButton("SSH", callback_data="send_ssh_video")],
        [InlineKeyboardButton("بازگشت", callback_data="back")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="یک گزینه را انتخاب کنید:", reply_markup=reply_markup
    )


async def send_v2ray_video(update: Update, context: CallbackContext) -> None:
    """Sends the V2RAY-NG video tutorial."""
    video_path = "E:/TBot/Sales/src/Darkside.mp4"
    await update.callback_query.message.reply_video(video=open(video_path, "rb"))
    await update.callback_query.answer()


async def send_ssh_video(update: Update, context: CallbackContext) -> None:
    """Sends the SSH video tutorial."""
    video_path = "E:/TBot/Sales/src/Numb.mp4"
    await update.callback_query.message.reply_video(video=open(video_path, "rb"))
    await update.callback_query.answer()


async def handle_software(query, context):
    """Handles the Necessary Software button click and sends .apk files."""
    keyboard = [
        [InlineKeyboardButton("SSH-Client", callback_data="send_ssh_apk")],
        [InlineKeyboardButton("V2ray-NG", callback_data="send_v2ray_apk")],
        [InlineKeyboardButton("بازگشت", callback_data="back")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="نرم افزار مورد نیاز را انتخاب کنید:", reply_markup=reply_markup
    )


async def send_ssh_apk(update: Update, context: CallbackContext) -> None:
    """Sends the SSH-Client .apk file."""
    apk_path = (
        "E:/TBot/Sales/src/WDCFree_11.0.9.823.apk"  # Assuming the file is .apk now
    )
    await update.callback_query.message.reply_document(document=open(apk_path, "rb"))
    await update.callback_query.answer()


async def send_v2ray_apk(update: Update, context: CallbackContext) -> None:
    """Sends the V2ray-NG .apk file."""
    apk_path = "E:/TBot/Sales/src/OperaGXSetup_3.apk"  # Assuming the file is .apk now
    await update.callback_query.message.reply_document(document=open(apk_path, "rb"))
    await update.callback_query.answer()


async def handle_contact(query, context):
    """Handles the Contact Us button click."""
    # Add the relevant code to handle contact information here
    # Example:
    await query.edit_message_text(
        text="برای تماس با ما، لطفا از طریق ایمیل contact@example.com اقدام کنید."
    )


async def handle_buy_config(query, context):
    """Handles the Buy Config button click."""
    # Add the relevant code to handle config buying process here
    # Example:
    await query.edit_message_text(
        text="برای خرید کانفیگ، لطفا یکی از گزینه‌های زیر را انتخاب کنید:"
    )


async def handle_buy_specific(query, context):
    """Handles specific buy options."""
    # Implement logic for specific buy options
    await query.edit_message_text(text="شما یک گزینه خرید خاص را انتخاب کرده‌اید.")


async def handle_config_payment(query, context):
    """Handles the config payment process."""
    # Implement logic for handling config payment
    await query.edit_message_text(text="در حال پردازش پرداخت کانفیگ...")


def main() -> None:
    """Main entry point for the bot."""
    application = Application.builder().token(TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_click))

    # Start polling for updates
    application.run_polling()


if __name__ == "__main__":
    main()
