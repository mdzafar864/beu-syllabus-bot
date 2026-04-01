import telebot
from telebot.types import ReplyKeyboardMarkup
import os
import json
from datetime import datetime

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    print("❌ ERROR: BOT_TOKEN not found!")
    print("Please set BOT_TOKEN in environment variables")
    exit(1)

# Try to initialize bot with error handling
try:
    bot = telebot.TeleBot(TOKEN)
    # Test connection
    bot_info = bot.get_me()
    print(f"✅ Bot connected successfully!")
    print(f"🤖 Bot name: {bot_info.first_name}")
    print(f"🔑 Username: @{bot_info.username}")
except Exception as e:
    print(f"❌ Failed to connect: {e}")
    exit(1)

user_data = {}

# Simple analytics
user_analytics = {
    "total_users": set(),
    "commands_used": {}
}

def track_user(user_id, command="start"):
    """Track user activity"""
    user_analytics["total_users"].add(user_id)
    user_analytics["commands_used"][command] = user_analytics["commands_used"].get(command, 0) + 1

# ===== SYLLABUS DATABASE =====
syllabus = {
    "1stNew": {
        "CE": "https://drive.google.com/uc?export=download&id=1Qd3X732fBWyEax1GTudkBWn7fpe57CgA",
        "CS": "https://drive.google.com/uc?export=download&id=1Zp-UAEgj72UstczPS_wSIBtlPU48USal",
        "EE": "https://drive.google.com/uc?export=download&id=1dZCtmM7w3H9dRpsWMlDhhJZNvFOiA1up",
        "ECE": "https://drive.google.com/uc?export=download&id=14cLD5aiYQp_2U3qKN16pa7U4fowBMg3J",
        "ME": "https://drive.google.com/uc?export=download&id=1yYB-UOYnpkOCYspJeZv83o7Rjy3wfcB8"
    },
    "1stOld": {
        "CE": "https://drive.google.com/uc?export=download&id=1iRWghHRyCP6WPZ3Xoc0DdScIytir3xRn",
        "CS": "https://drive.google.com/uc?export=download&id=1EHpLPUo0_7086gFmk2WRZv2fMw93Jcdb",
        "EE": "https://drive.google.com/uc?export=download&id=1BtS61CEIOidszDe5FLBVQUake_8RQZlK",
        "ECE": "https://drive.google.com/uc?export=download&id=1t57gqcXtYajz6p5q6FXtcBVPb-mUgX1m",
        "ME": "https://drive.google.com/uc?export=download&id=1gyWaJKhhcZNmSF9WlWfqRXfnTeA87hvY"
    },
    "2ndNew": {
        "CE": "https://drive.google.com/uc?export=download&id=13q_AFXP9e2AWyHHtHWp_Fm4bRgtME3qv",
        "CS": "https://drive.google.com/uc?export=download&id=15Y2Vsq8xe3Cl2Sc4BcXtL4XQMsqwKIFh",
        "EE": "https://drive.google.com/uc?export=download&id=1wgmEj8RSBWleYUZ1JjzD7tICuiQgJEDW",
        "ECE": "https://drive.google.com/uc?export=download&id=1THqchJygHP7BVVQjj-kf4YmMHBrjfA_x",
        "ME": "https://drive.google.com/uc?export=download&id=1hhAgOvC2LvbBRv6f7n1MSHPxD9MBVgsy"
    },
    "2ndOld": {
        "CE": "https://drive.google.com/uc?export=download&id=1jW97lTtufHT26vkRP6KISUiKWSYe6F3o",
        "CS": "https://drive.google.com/uc?export=download&id=16JynS8hA5JtsSlIc3-HBUPqI9o1F2ziN",
        "EE": "https://drive.google.com/uc?export=download&id=1CrAHd-0bwzESjiLtb-AQwOeKtopyiJm9",
        "ECE": "https://drive.google.com/uc?export=download&id=1eJQJy3I853QoqfNzOT5XFUgncJKxbnv6",
        "ME": "https://drive.google.com/uc?export=download&id=1xwhvlJIQJRCqKLCPTKeOOdjzkUgr8S5U"
    },
    "3rdNew": {
        "CE": "https://drive.google.com/uc?export=download&id=1GzMwwCkUrHPmc5fgyWOxOSsPof9dQZO8",
        "CS": "https://drive.google.com/uc?export=download&id=18tjQnI2qGtbSzRWEp08KqKY4gDvE25em",
        "IOT": "https://drive.google.com/uc?export=download&id=1DyoqlnntdtG-RA0ET1wH4FrR-DOB3mtF",
        "EE": "https://drive.google.com/uc?export=download&id=1nKpL1rXXa7EGJqbvDkmEem1uh74QWjOU",
        "ECE": "https://drive.google.com/uc?export=download&id=1kWy1_zhggLM9U4jrkTzGWNdLcE-4QXMr",
        "ME": "https://drive.google.com/uc?export=download&id=14yS8pyf83vIA1vs-_DbAvWbYpF8y6gc9"
    },
    "3rdOld": {
        "CE": "https://drive.google.com/uc?export=download&id=1IS4EV9JvOfoLW3cYRW7U-qBkXyRAvFlD",
        "CS": "https://drive.google.com/uc?export=download&id=1ZlU22NFGirTuV01jKYiG9zdSU_IO29-t",
        "EE": "https://drive.google.com/uc?export=download&id=1D2gAZlW299s9f60wcdicGSZK7DpZVXkc",
        "ECE": "https://drive.google.com/uc?export=download&id=1auOpeh5UX4E23rnxIQo1K9TdFrqSXrm0",
        "ME": "https://drive.google.com/uc?export=download&id=1XE_l1tfHGZHMDIxU6KNlcjlqiKxKN-ZW"
    },
    "4th": {
        "CE": "https://drive.google.com/uc?export=download&id=17w5zTFNaWUOg7S_vUrqW_AxtMyf7bPdU",
        "CS": "https://drive.google.com/uc?export=download&id=1ODCj6Omx6dUuHR-Cmwh4iu37TaMQyTLn",
        "EE": "https://drive.google.com/uc?export=download&id=1G-cJOckwjZRoaDz0Nnw-CphpqBcZztA7",
        "ECE": "https://drive.google.com/uc?export=download&id=1nkfp0xRno6_ybJSWqZ6_ryiwI4aNsjXh",
        "ME": "https://drive.google.com/uc?export=download&id=1jVvYbUmth-RIbhLBXbDf3ooB8zgz8fSc"
    },
    "5th": {
        "CE": "https://drive.google.com/uc?export=download&id=1tGXDItZ5g-AsnsXN0KmMifbA36vgxA0C",
        "CS": "https://drive.google.com/uc?export=download&id=1SZdAT8a1vrIfrMPYjl0Q-0cc3hBba3z3",
        "EE": "https://drive.google.com/uc?export=download&id=1MA_tDBF7Fuvg8OGgn8bzg4mHSUTmQ-dC",
        "ECE": "https://drive.google.com/uc?export=download&id=1dJV_E7tPdhmmA7IutIDeaDMz3rxYb9XR",
        "ME": "https://drive.google.com/uc?export=download&id=1FW1-YDLvthfdG52szzsLzTIU9DOI03bc"
    },
    "6th": {
        "CE": "https://drive.google.com/uc?export=download&id=1MxzSoTSdMgCvgCPiDFsDjVuu4QaJCQge",
        "CS": "https://drive.google.com/uc?export=download&id=1ckXxGY5kdHmxlAIGsq-NfDskA4Mj_xQj",
        "EE": "https://drive.google.com/uc?export=download&id=1obhgEQmyRzDg1XPG7Gc6u5SyMugXN9bn",
        "ECE": "https://drive.google.com/uc?export=download&id=1reUmWqura-4UnEx7tpjv6wANADxvW_lc",
        "ME": "https://drive.google.com/uc?export=download&id=19UDBkvdYqgMqRzV_Fgre8vq8utOapy2q"
    },
    "7th": {
        "CE": "https://drive.google.com/uc?export=download&id=1Qy64E3CCdfhQvD8PaihwPDFVz2FwDqGr",
        "CS": "https://drive.google.com/uc?export=download&id=1uW4HVIaLErhWIyj36Lday4JMH1ZfuLEp",
        "EE": "https://drive.google.com/uc?export=download&id=1ey1jhsveL-eO0gc0FgwlNs7U05qRQHp5",
        "ECE": "https://drive.google.com/uc?export=download&id=1aDSSzOz8kWsmO0oJV7Z5CZ2lnCXReEqq",
        "ME": "https://drive.google.com/uc?export=download&id=1kMv43ZFJMctH_iRYbI230GCNN4UkZYud"
    },
    "8th": {
        "EE": "https://drive.google.com/uc?export=download&id=1BwL_f3KCmWzuEulEth3G3hQw5sxLvBOy",
        "ME": "https://drive.google.com/uc?export=download&id=1PPkfTohITDMkIFNuw836gSOSUjCFtt3n"
    }
}

# ===== MAIN MENU =====
def get_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("📚 Syllabus")
    markup.add("📈 Statistics", "ℹ️ Help", "⭐ Feedback")
    return markup

# ===== START COMMAND =====
@bot.message_handler(commands=['start'])
def start(message):
    track_user(message.chat.id, "start")
    bot.send_message(
        message.chat.id,
        "🎓 *Welcome to BEU Syllabus Bot* 🎓\n\n"
        "I can help you with:\n"
        "📚 *Syllabus* - Download semester-wise syllabus PDFs\n"
        "📈 *Statistics* - View bot usage statistics\n"
        "⭐ *Feedback* - Share your feedback/suggestions\n\n"
        "Select an option from the menu below:",
        reply_markup=get_main_menu(),
        parse_mode='Markdown'
    )

# ===== SYLLABUS MENU =====
@bot.message_handler(func=lambda m: m.text == "📚 Syllabus")
def syllabus_menu(message):
    track_user(message.chat.id, "syllabus")
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("1stNew", "1stOld")
    markup.add("2ndNew", "2ndOld")
    markup.add("3rdNew", "3rdOld")
    markup.add("4th", "5th")
    markup.add("6th", "7th", "8th")
    markup.add("🔙 Main Menu")
    bot.send_message(message.chat.id, "📚 *Select your Semester:*", reply_markup=markup, parse_mode='Markdown')

# ===== STATISTICS =====
@bot.message_handler(func=lambda m: m.text == "📈 Statistics")
def show_statistics(message):
    track_user(message.chat.id, "statistics")
    stats_text = "📊 *Bot Usage Statistics*\n━━━━━━━━━━━━━━━━━━━━━\n\n"
    stats_text += f"👥 *Total Users:* {len(user_analytics['total_users'])}\n\n"
    stats_text += "*Top Commands Used:*\n"
    sorted_commands = sorted(user_analytics["commands_used"].items(), key=lambda x: x[1], reverse=True)[:5]
    for cmd, count in sorted_commands:
        stats_text += f"  • {cmd}: {count} times\n"
    bot.send_message(message.chat.id, stats_text, parse_mode='Markdown')

# ===== HELP =====
@bot.message_handler(func=lambda m: m.text == "ℹ️ Help")
def show_help(message):
    help_text = "ℹ️ *Bot Help*\n━━━━━━━━━━━━━━━━━━━━━\n\n"
    help_text += "*Available Features:*\n"
    help_text += "📚 Syllabus - Download semester-wise syllabus PDFs\n"
    help_text += "📈 Statistics - View bot usage statistics\n"
    help_text += "⭐ Feedback - Share your feedback\n\n"
    help_text += "*How to Use:*\n"
    help_text += "1. Click '📚 Syllabus'\n2. Select semester\n3. Choose branch\n4. Download PDF"
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')

# ===== FEEDBACK =====
@bot.message_handler(func=lambda m: m.text == "⭐ Feedback")
def ask_feedback(message):
    track_user(message.chat.id, "feedback_start")
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔙 Main Menu")
    msg = bot.send_message(message.chat.id, "⭐ *Share Your Feedback*\n\nType your message below:", reply_markup=markup, parse_mode='Markdown')
    bot.register_next_step_handler(msg, save_feedback)

def save_feedback(message):
    if message.text == "🔙 Main Menu":
        start(message)
        return
    track_user(message.chat.id, "feedback_submit")
    with open("feedback.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} - User {message.chat.id}: {message.text}\n")
    bot.send_message(message.chat.id, "✅ *Thank you for your feedback!*", reply_markup=get_main_menu(), parse_mode='Markdown')

# ===== BACK BUTTON =====
@bot.message_handler(func=lambda m: m.text == "🔙 Main Menu")
def back_to_main(message):
    start(message)

# ===== SYLLABUS HANDLERS =====
@bot.message_handler(func=lambda m: m.text in syllabus.keys())
def sem_select(message):
    track_user(message.chat.id, f"semester_{message.text}")
    user_data[message.chat.id] = {"sem": message.text}
    available_branches = list(syllabus[message.text].keys())
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for i in range(0, len(available_branches), 2):
        if i + 1 < len(available_branches):
            markup.add(available_branches[i], available_branches[i+1])
        else:
            markup.add(available_branches[i])
    markup.add("🔙 Main Menu")
    bot.send_message(message.chat.id, f"🏫 *Select your Branch for {message.text}:*", reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(func=lambda m: m.text in ["CE", "CS", "EE", "ECE", "ME", "IOT"])
def send_pdf(message):
    track_user(message.chat.id, f"branch_{message.text}")
    data = user_data.get(message.chat.id)
    if not data:
        bot.send_message(message.chat.id, "❌ पहले semester select करो!")
        return
    sem = data["sem"]
    branch = message.text
    if branch not in syllabus[sem]:
        bot.send_message(message.chat.id, f"❌ *{branch}* इस semester में available नहीं है!", parse_mode='Markdown')
        return
    try:
        file_url = syllabus[sem][branch]
        bot.send_message(message.chat.id, f"📥 *{branch} Syllabus ({sem}) भेज रहा हूँ...*", parse_mode='Markdown')
        bot.send_document(message.chat.id, file_url, caption=f"📚 *{sem} Semester - {branch} Branch*\n\n✅ Download complete!", parse_mode='Markdown')
        if message.chat.id in user_data:
            del user_data[message.chat.id]
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Download failed! Try manual link: {file_url}", parse_mode='Markdown')

# ===== DEFAULT HANDLER =====
@bot.message_handler(func=lambda m: True)
def default_handler(message):
    bot.send_message(message.chat.id, "❓ Unknown command!\n\nPlease use the menu buttons:", reply_markup=get_main_menu(), parse_mode='Markdown')

# ===== RUN BOT =====
if __name__ == "__main__":
    print("="*50)
    print("🚀 BEU Syllabus Bot Started...")
    print("="*50)
    print("✅ Bot is running successfully!")
    print("="*50)
    
    try:
        bot.infinity_polling(skip_pending=True, timeout=60)
    except Exception as e:
        print(f"❌ Bot polling error: {e}")
