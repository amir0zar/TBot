import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
)

# Replace 'YOUR_TOKEN_HERE' with your actual bot token
TOKEN = "7502162456:AAGSW83AB6wk9kiaUdzC6OROWke-9vY6CL8"

# File path for the configuration list
CONFIG_FILE_PATH = "https://github.com/amir0zar/TBot/blob/80ed5f45427a65818198b96a5b3cf6b28fe25884/src/CONFS.txt"

# Configuration options with prices (modifiable by bot owners)
config_options = {
    "ssh": {
        "یکماهه تک کاربره": 110,
        "دو ماهه تک کاربره": 150,
        "سه ماه تک کاربره": 200,
        "دوکاربره یکماهه": 250,
        "دو کاربره دوماهه": 300,
        "دو کاربره سه ماهه": 350,
    },
    "v2ray": {
        "یک کاربره 10 گیگ": 10,
        "یک کابره 30 گیگ": 30,
        "یک کاربره 50 گیگ": 50,
        "یک کاربره 70 گیگ": 70,
        "یک کاربره 90 گیگ": 90,
        "دو کاربره 10 گیگ": 10,
        "دو کاربره 30 گیگ": 30,
        "دو کاربره 50 گیگ": 50,
        "دو کاربره 70 گیگ": 70,
        "دو کاربره 90 گیگ": 90,
    },
}


def load_configs():
    """Load configurations from the CONFIG_FILE_PATH into a dictionary."""
    configs = {"ssh": [], "v2ray": []}
    current_type = None

    with open(CONFIG_FILE_PATH, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("SSH"):
                current_type = "ssh"
            elif line.startswith("V2ray"):
                current_type = "v2ray"
            elif line.startswith("-") and current_type:
                # Strip off the leading '- ' and add to the respective list
                configs[current_type].append(line[2:].strip('"'))

    return configs


def save_configs(configs):
    """Save the remaining configurations back to the CONFIG_FILE_PATH."""
    with open(CONFIG_FILE_PATH, "w") as file:
        file.write("SSH:\n\n")
        for config in configs["ssh"]:
            file.write(f'- "{config}"\n')

        file.write("\n\nV2ray:\n\n")
        for config in configs["v2ray"]:
            file.write(f'- "{config}"\n')


async def start(update: Update, context: CallbackContext) -> None:
    """Handles the /start command, presenting the initial options to the user."""
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

    if query.data == "tutorial":
        await handle_tutorial(query)
    elif query.data == "software":
        await handle_software(query)
    elif query.data == "contact":
        await handle_contact(query)
    elif query.data == "buy_config":
        await handle_buy_config(query)
    elif query.data.startswith("buy_"):
        await handle_buy_specific(query)
    elif query.data.startswith("config_"):
        await handle_config_payment(query)


async def handle_tutorial(query):
    """Handles the TUTORIAL button click."""
    keyboard = [
        [InlineKeyboardButton("V2RAY-NG", url="src\mood-sad.mp4")],
        [InlineKeyboardButton("SSH", url="src\vpn-https.mp4")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="یک گزینه را انتخاب کنید.:", reply_markup=reply_markup
    )


async def handle_software(query):
    """Handles the Necessary Software button click."""
    keyboard = [
        [
            InlineKeyboardButton(
                "SSH-Client",
                url="https://dl2.apkshub.com/download/com.napsternetlabs.napsternetv-62.0.0-free?dv=6a5c93730fb05508ee3c2a57ec5f5676&st=1723891992",
            )
        ],
        [
            InlineKeyboardButton(
                "V2ray-NG",
                url="https://dl2.apkshub.com/download/com.v2ray.ang-1.8.29-free?dv=32b4962f5e29594b92d70b43ea641735&st=1723892125",
            )
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="نرم افزار مورد نیاز را دانلود کنید.", reply_markup=reply_markup
    )


async def handle_contact(query):
    """Handles the Contact Us button click."""
    await query.edit_message_text(text="تماس با ما: @moz-gojeh")


async def handle_buy_config(query):
    """Handles the Buy The CONFIG button click."""
    keyboard = [
        [InlineKeyboardButton("SSH", callback_data="buy_ssh")],
        [InlineKeyboardButton("V2ray", callback_data="buy_v2ray")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="لطفاً کانفیگ مورد نظر خود را انتخاب کنید:", reply_markup=reply_markup
    )


async def handle_buy_specific(query):
    """Handles specific configuration purchase options."""
    config_type = query.data.split("_")[1]
    keyboard = [
        [
            InlineKeyboardButton(
                f"{option} - {price} هزار تومان",
                callback_data=f"config_{config_type}_{option.lower()}",
            )
        ]
        for option, price in config_options[config_type].items()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="لطفاً کانفیگ موردنظر خود را انتخاب کنید:", reply_markup=reply_markup
    )


async def handle_config_payment(query):
    """Simulates the payment process and distributes the selected configuration."""
    _, config_type, config_name = query.data.split("_")
    price = config_options[config_type][config_name.capitalize()]

    # Simulate payment process
    await query.edit_message_text(
        text=f"لطفاً مبلغ {price} هزار تومان را برای کانفیگ {config_name.capitalize()} {config_type.upper()} پرداخت کنید. درحال انتقال به درگاه پرداخت ..."
    )

    # Simulated payment success
    successful_payment = True

    if successful_payment:
        configs = load_configs()
        if configs[config_type]:
            config = configs[config_type].pop(0)  # Get the first available config
            save_configs(configs)  # Save the updated configs back to the file
            await query.message.reply_text(
                f"پرداخت با موفقیت انجام شد. /n اطلاعات کانفیگ شما به صورت زیر است: /n {config_type.upper()} config:\n\n{config}"
            )
        else:
            await query.message.reply_text(
                f"متأسفانه در حال حاضر کانفیگ {config_type.upper()} ناموجود می باشد."
            )
    else:
        await query.message.reply_text("پرداخت ناموفق بود. لطفاًمجدداً سعی کنید.")


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
