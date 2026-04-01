import telebot
from telebot.types import ReplyKeyboardMarkup
import os
import json
from datetime import datetime
import logging

# Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID", "")  # Your Telegram user ID

if not TOKEN:
    print("❌ BOT_TOKEN required!")
    exit(1)

bot = telebot.TeleBot(TOKEN)

def send_admin_notification(message):
    """Send notification to admin via Telegram"""
    if not ADMIN_CHAT_ID:
        logger.warning("ADMIN_CHAT_ID not set, skipping notification")
        return False
    
    try:
        bot.send_message(ADMIN_CHAT_ID, message, parse_mode='HTML')
        logger.info(f"Notification sent to admin: {message[:50]}...")
        return True
    except Exception as e:
        logger.error(f"Failed to send notification: {e}")
        return False

# Track users
user_analytics = {
    "total_users": set(),
    "daily_users": set(),
    "last_reset": datetime.now().date().isoformat()
}

# Syllabus data (keep your existing syllabus dict)
syllabus = {
    "1stNew": {
        "CE": "https://drive.google.com/uc?export=download&id=1Qd3X732fBWyEax1GTudkBWn7fpe57CgA",
        "CS": "https://drive.google.com/uc?export=download&id=1Zp-UAEgj72UstczPS_wSIBtlPU48USal",
        # ... add all your other semesters
    }
}

def get_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("📚 Syllabus", "📊 Statistics", "ℹ️ Help")
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    username = message.from_user.username or "No username"
    
    # Track user
    user_analytics["total_users"].add(user_id)
    
    # Send welcome message
    bot.send_message(
        user_id,
        "🎓 Welcome to BEU Syllabus Bot!\n\n"
        "Use /help to see available commands.",
        reply_markup=get_main_menu()
    )
    
    # Notify admin
    notification = f"""
<b>🤖 New User Started Bot</b>
User ID: <code>{user_id}</code>
Username: @{username}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total Users: {len(user_analytics['total_users'])}
    """
    send_admin_notification(notification)

@bot.message_handler(commands=['stats'])
def stats(message):
    """Admin only: View bot stats"""
    if str(message.chat.id) != ADMIN_CHAT_ID:
        bot.reply_to(message, "⚠️ Admin only command")
        return
    
    stats_text = f"""
📊 Bot Statistics:
━━━━━━━━━━━━━━━━━━━━━
👥 Total Users: {len(user_analytics['total_users'])}
📅 Daily Active: {len(user_analytics['daily_users'])}
🕐 Last Reset: {user_analytics['last_reset']}
    """
    bot.reply_to(message, stats_text)

@bot.message_handler(func=lambda m: m.text == "📚 Syllabus")
def syllabus_menu(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    # Add your semester buttons
    markup.add("1stNew", "2ndNew", "3rdNew", "4th", "5th", "6th", "7th", "8th")
    markup.add("🔙 Main Menu")
    bot.send_message(message.chat.id, "Select semester:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "📊 Statistics")
def show_stats(message):
    stats_text = f"""
📊 Bot Statistics:
━━━━━━━━━━━━━━━━━━━━━
👥 Total Users: {len(user_analytics['total_users'])}
📅 Active Today: {len(user_analytics['daily_users'])}
    """
    bot.send_message(message.chat.id, stats_text)

@bot.message_handler(func=lambda m: m.text == "ℹ️ Help")
def help_command(message):
    help_text = """
ℹ️ <b>Bot Help</b>
━━━━━━━━━━━━━━━━━━━━━

<b>Commands:</b>
/start - Start the bot
/help - Show this help

<b>How to use:</b>
1. Click 📚 Syllabus
2. Select your semester
3. Choose your branch
4. Download syllabus PDF
    """
    bot.send_message(message.chat.id, help_text, parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "🔙 Main Menu")
def back_to_main(message):
    start(message)

# Handle syllabus selection
@bot.message_handler(func=lambda m: m.text in syllabus.keys())
def sem_select(message):
    user_data = {"sem": message.text}
    available_branches = list(syllabus[message.text].keys())
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for branch in available_branches:
        markup.add(branch)
    markup.add("🔙 Main Menu")
    
    bot.send_message(
        message.chat.id,
        f"Select branch for {message.text}:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.text in ["CE", "CS", "EE", "ECE", "ME", "IOT"])
def send_pdf(message):
    # This needs to track which semester user selected
    # For simplicity, we'll assume you store it
    file_url = "YOUR_GOOGLE_DRIVE_URL"  # Get from syllabus dict
    
    try:
        bot.send_document(
            message.chat.id,
            file_url,
            caption="📚 Syllabus PDF"
        )
    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"❌ Download failed: {str(e)}\nPlease try again."
        )

@bot.message_handler(func=lambda m: True)
def default(message):
    bot.send_message(
        message.chat.id,
        "❓ Unknown command.\nUse /help for available commands.",
        reply_markup=get_main_menu()
    )

# Run bot
if __name__ == "__main__":
    print("="*50)
    print("🚀 BEU Syllabus Bot Starting...")
    print(f"Bot: @{bot.get_me().username}")
    print(f"Admin ID: {ADMIN_CHAT_ID if ADMIN_CHAT_ID else 'Not set'}")
    print("="*50)
    
    # Send startup notification
    send_admin_notification(f"🚀 Bot started at {datetime.now()}")
    
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"Bot error: {e}")
