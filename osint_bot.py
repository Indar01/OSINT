import logging  # 'i' small kar diya
import requests
import urllib.parse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryH>

# --- CONFIGURATION ---
TOKEN = "7972645769:AAED-kqyl_Ph0cMe4Iw70tmhnuJvNWnvdXY" # Naya token use karein security ke liye
API_BASE_URL = "http://osintx.info/API/krobetahack.php"
MOBILE_KEY = "ZYROBR0TH3R"
ID_KEY = "XXYYZZZYRO"

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- HELPER FUNCTIONS ---
def generate_map_link(address):
    if not address or address == "N/A":
        return None
    base = "https://www.google.com/maps/search/" # Sahi map base link
    return base + urllib.parse.quote(str(address))

# --- BOT HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_msg = (
        f"🔥 *OSINT Intelligence Bot v6.0* 🔥\n\n"
        f"Welcome {user.first_name}!\n"
        f"Main niche diye gaye modules ka use karke data extract kar sakta hoon.\n\n"
        f"🛡️ *Authorized Pentest Tool*"
    )

    keyboard = [
        [InlineKeyboardButton("📱 Mobile Lookup", callback_data='mode_mobile')],
        [InlineKeyboardButton("🆔 ID/CNIC Lookup", callback_data='mode_id')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(welcome_msg, reply_markup=reply_markup, parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'mode_mobile':
        context.user_data['mode'] = 'mobile'
        await query.edit_message_text("📱 *Mobile Mode Active*\nAb apna Number send karein (e.g. 03xxxxxxxx>
    elif query.data == 'mode_id':
        context.user_data['mode'] = 'id_number'
        await query.edit_message_text("🆔 *ID Mode Active*\nAb apna ID Number send karein:", parse_mode='Ma>

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = context.user_data.get('mode')
    if not mode:
        await update.message.reply_text("❌ Pehle /start dabakar mode select karein!")
        return

    term = update.message.text.strip()
    api_key = MOBILE_KEY if mode == 'mobile' else ID_KEY

    status_msg = await update.message.reply_text("📡 *Searching Database... Please wait.*", parse_mode='Mar>

    try:
        url = f"{API_BASE_URL}?key={api_key}&type={mode}&term={term}"
        response = requests.get(url, timeout=20)
        data = response.json()

        if data:
            result_text = f"🎯 *TARGET INTEL REPORT*\n{'═'*25}\n"
            address_val = None

            # Agar list hai toh pehla item lo, varna dict
            items = data[0] if isinstance(data, list) and len(data) > 0 else data

            if isinstance(items, dict):
                for key, value in items.items():
                    if value and value != "N/A":
                        result_text += f"🔹 *{key.upper()}:* `{value}`\n"
                        if key.lower() in ['address', 'location', 'city', 'permanent_address']:
                            address_val = value
            else:
                result_text += "❌ Data format unknown."

            if address_val:
                map_url = generate_map_link(address_val)
                result_text += f"\n📍 [View on Google Maps]({map_url})"

            result_text += f"\n{'═'*25}\n✅ *Scan Complete*"
            await status_msg.edit_text(result_text, parse_mode='Markdown')
        else:
            await status_msg.edit_text("💀 *GHOST TARGET* - No data found in database.")

    except Exception as e:
        await status_msg.edit_text(f"🛑 *API Error:* {str(e)}")

# --- MAIN ---
def main():
    # Token check
    if TOKEN == "7972645769:AAED-kqyl_Ph0cMe4Iw70tmhnuJvNWnvdXY":
        print("⚠️ Warning: Token purana hai, agar error aaye toh naya token use karein.")

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
