import telebot
from telebot.types import ReplyKeyboardMarkup
import os
import json
from datetime import datetime
import requests
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get environment variables
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    logger.error("âŒ BOT_TOKEN not found!")
    exit(1)

try:
    bot = telebot.TeleBot(TOKEN)
    bot_info = bot.get_me()
    logger.info(f"âœ… Bot connected: @{bot_info.username}")
except Exception as e:
    logger.error(f"âŒ Bot connection failed: {e}")
    exit(1)

user_data = {}
user_analytics = {
    "total_users": set(),
    "daily_users": set(),
    "commands_used": {}
}

ANALYTICS_FILE = "user_analytics.json"

def load_analytics():
    global user_analytics
    try:
        with open(ANALYTICS_FILE, 'r') as f:
            loaded = json.load(f)
            loaded["total_users"] = set(loaded.get("total_users", []))
            loaded["daily_users"] = set(loaded.get("daily_users", []))
            user_analytics = loaded
    except FileNotFoundError:
        save_analytics()

def save_analytics():
    try:
        to_save = {
            "total_users": list(user_analytics["total_users"]),
            "daily_users": list(user_analytics["daily_users"]),
            "commands_used": user_analytics["commands_used"]
        }
        with open(ANALYTICS_FILE, 'w') as f:
            json.dump(to_save, f)
    except Exception as e:
        logger.error(f"Error saving analytics: {e}")

def track_user(user_id, command="start"):
    try:
        user_analytics["total_users"].add(user_id)
        user_analytics["daily_users"].add(user_id)
        user_analytics["commands_used"][command] = user_analytics["commands_used"].get(command, 0) + 1
        save_analytics()
    except Exception as e:
        logger.error(f"Error tracking user: {e}")

# Load analytics
load_analytics()

# ===== SYLLABUS DATABASE WITH WORKING LINKS =====
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

def get_direct_download_url(file_id):
    """Convert Google Drive file ID to direct download URL"""
    return f"https://drive.google.com/uc?export=download&id={file_id}"

# ===== MAIN MENU =====
def get_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("ðŸ“š Syllabus")
    markup.add("ðŸ“ˆ Statistics", "â„¹ï¸ Help", "â­ Feedback")
    return markup

# ===== START COMMAND =====
@bot.message_handler(commands=['start'])
def start(message):
    try:
        track_user(message.chat.id, "start")
        
        bot.send_message(
            message.chat.id,
            "ðŸŽ“ *Welcome to BEU Syllabus Bot* ðŸŽ“\n\n"
            "I can help you download syllabus for all semesters and branches.\n\n"
            "ðŸ“š *Available Features:*\n"
            "â€¢ All semesters (1st to 8th)\n"
            "â€¢ New & Old syllabus patterns\n"
            "â€¢ All branches (CE, CS, EE, ECE, ME, IOT)\n\n"
            "Select an option from the menu below:",
            reply_markup=get_main_menu(),
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Error in start: {e}")

# ===== SYLLABUS MENU =====
@bot.message_handler(func=lambda m: m.text == "ðŸ“š Syllabus")
def syllabus_menu(message):
    try:
        track_user(message.chat.id, "syllabus")
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add("1stNew", "1stOld")
        markup.add("2ndNew", "2ndOld")
        markup.add("3rdNew", "3rdOld")
        markup.add("4th", "5th")
        markup.add("6th", "7th", "8th")
        markup.add("ðŸ”™ Main Menu")
        
        bot.send_message(
            message.chat.id,
            "ðŸ“š *Select your Semester:*\n\n"
            "â€¢ New = New syllabus pattern\n"
            "â€¢ Old = Old syllabus pattern",
            reply_markup=markup,
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Error in syllabus_menu: {e}")

# ===== STATISTICS =====
@bot.message_handler(func=lambda m: m.text == "ðŸ“ˆ Statistics")
def show_statistics(message):
    try:
        track_user(message.chat.id, "statistics")
        
        stats_text = "ðŸ“Š *Bot Usage Statistics*\n"
        stats_text += "â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”\n\n"
        stats_text += f"ðŸ‘¥ *Total Users:* {len(user_analytics['total_users'])}\n"
        stats_text += f"ðŸ“… *Today's Active:* {len(user_analytics['daily_users'])}\n\n"
        
        stats_text += "*Most Used Features:*\n"
        sorted_commands = sorted(user_analytics["commands_used"].items(), key=lambda x: x[1], reverse=True)[:5]
        for cmd, count in sorted_commands:
            emoji = "ðŸ“š" if cmd == "syllabus" else "â­" if cmd == "feedback" else "ðŸ“Š"
            stats_text += f"  {emoji} {cmd}: {count} times\n"
        
        bot.send_message(message.chat.id, stats_text, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Error in statistics: {e}")

# ===== HELP =====
@bot.message_handler(func=lambda m: m.text == "â„¹ï¸ Help")
def show_help(message):
    try:
        help_text = "â„¹ï¸ *Bot Help Guide*\n"
        help_text += "â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”\n\n"
        help_text += "*How to Download Syllabus:*\n"
        help_text += "1ï¸âƒ£ Click 'ðŸ“š Syllabus'\n"
        help_text += "2ï¸âƒ£ Select your semester (e.g., 3rdNew)\n"
        help_text += "3ï¸âƒ£ Choose your branch (CE, CS, etc.)\n"
        help_text += "4ï¸âƒ£ PDF will be sent automatically\n\n"
        
        help_text += "*Available Semesters:*\n"
        help_text += "â€¢ 1stNew, 1stOld\n"
        help_text += "â€¢ 2ndNew, 2ndOld\n"
        help_text += "â€¢ 3rdNew, 3rdOld\n"
        help_text += "â€¢ 4th, 5th, 6th, 7th, 8th\n\n"
        
        help_text += "*Available Branches:*\n"
        help_text += "CE, CS, EE, ECE, ME, IOT\n\n"
        
        help_text += "*Commands:*\n"
        help_text += "/start - Restart bot\n"
        help_text += "ðŸ“ˆ Statistics - View bot stats\n"
        help_text += "â­ Feedback - Send feedback"
        
        bot.send_message(message.chat.id, help_text, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Error in help: {e}")

# ===== FEEDBACK =====
@bot.message_handler(func=lambda m: m.text == "â­ Feedback")
def ask_feedback(message):
    try:
        track_user(message.chat.id, "feedback_start")
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("ðŸ”™ Main Menu")
        
        msg = bot.send_message(
            message.chat.id,
            "â­ *Share Your Feedback*\n\n"
            "Please tell me:\n"
            "â€¢ What features you'd like to see\n"
            "â€¢ Any issues you faced\n"
            "â€¢ General suggestions\n\n"
            "Type your message below:",
            reply_markup=markup,
            parse_mode='Markdown'
        )
        bot.register_next_step_handler(msg, save_feedback)
    except Exception as e:
        logger.error(f"Error in feedback: {e}")

def save_feedback(message):
    try:
        if message.text == "ðŸ”™ Main Menu":
            start(message)
            return
        
        track_user(message.chat.id, "feedback_submit")
        
        # Save feedback
        with open("feedback.txt", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()} - User {message.chat.id}: {message.text}\n")
        
        bot.send_message(
            message.chat.id,
            "âœ… *Thank you for your feedback!*\n\n"
            "Your input helps improve the bot.",
            reply_markup=get_main_menu(),
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Error saving feedback: {e}")

# ===== BACK BUTTON =====
@bot.message_handler(func=lambda m: m.text == "ðŸ”™ Main Menu")
def back_to_main(message):
    start(message)

# ===== SYLLABUS SELECTION =====
@bot.message_handler(func=lambda m: m.text in syllabus.keys())
def sem_select(message):
    try:
        track_user(message.chat.id, f"semester_{message.text}")
        user_data[message.chat.id] = {"sem": message.text}
        
        available_branches = list(syllabus[message.text].keys())
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        
        # Add branches in rows of 2
        for i in range(0, len(available_branches), 2):
            if i + 1 < len(available_branches):
                markup.add(available_branches[i], available_branches[i+1])
            else:
                markup.add(available_branches[i])
        
        markup.add("ðŸ”™ Main Menu")
        
        bot.send_message(
            message.chat.id,
            f"ðŸ« *Select your Branch for {message.text}:*\n\n"
            f"Available: {', '.join(available_branches)}",
            reply_markup=markup,
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Error in sem_select: {e}")

# ===== BRANCH SELECTION & PDF SEND =====
@bot.message_handler(func=lambda m: m.text in ["CE", "CS", "EE", "ECE", "ME", "IOT"])
def send_pdf(message):
    try:
        track_user(message.chat.id, f"branch_{message.text}")
        data = user_data.get(message.chat.id)
        
        if not data:
            bot.send_message(
                message.chat.id, 
                "âŒ Please select semester first!\n\nClick ðŸ“š Syllabus to start.",
                reply_markup=get_main_menu()
            )
            return
        
        sem = data["sem"]
        branch = message.text
        
        if branch not in syllabus[sem]:
            bot.send_message(
                message.chat.id, 
                f"âŒ *{branch}* branch is not available for {sem}!\n\nPlease select from the menu.",
                parse_mode='Markdown'
            )
            return
        
        file_url = syllabus[sem][branch]
        
        # Send loading message
        loading_msg = bot.send_message(
            message.chat.id, 
            f"ðŸ“¥ *Downloading {branch} Syllabus ({sem})...*\n\nPlease wait...",
            parse_mode='Markdown'
        )
        
        # Try to send the document
        try:
            bot.send_document(
                message.chat.id, 
                file_url,
                caption=f"ðŸ“š *{sem} Semester - {branch} Branch*\n\nâœ… Download Complete!\n\nðŸ“Œ For more syllabi, use /start",
                parse_mode='Markdown',
                timeout=30
            )
            
            # Delete loading message
            bot.delete_message(message.chat.id, loading_msg.message_id)
            
            # Clear user data
            if message.chat.id in user_data:
                del user_data[message.chat.id]
                
        except Exception as e:
            logger.error(f"Error sending document: {e}")
            bot.edit_message_text(
                f"âš ï¸ *Unable to send PDF directly*\n\n"
                f"ðŸ“Ž *Direct Download Link:*\n{file_url}\n\n"
                f"Click the link above to download the syllabus.",
                message.chat.id,
                loading_msg.message_id,
                parse_mode='Markdown',
                disable_web_page_preview=False
            )
            
    except Exception as e:
        logger.error(f"Error in send_pdf: {e}")
        bot.send_message(
            message.chat.id, 
            "âŒ *Download Failed!*\n\nPlease try again or contact support.",
            parse_mode='Markdown'
        )

# ===== DEFAULT HANDLER =====
@bot.message_handler(func=lambda m: True)
def default_handler(message):
    bot.send_message(
        message.chat.id,
        "â“ *Unknown Command*\n\n"
        "Please use the buttons below to navigate:",
        reply_markup=get_main_menu(),
        parse_mode='Markdown'
    )

# ===== RUN BOT =====
if __name__ == "__main__":
    logger.info("="*50)
    logger.info("ðŸš€ BEU Syllabus Bot Starting...")
    logger.info(f"ðŸ¤– Bot: @{bot_info.username}")
    logger.info(f"ðŸ“Š Total Users: {len(user_analytics['total_users'])}")
    logger.info("âœ… Bot is ready!")
    logger.info("="*50)
    
    try:
        bot.infinity_polling(timeout=60, skip_pending=True)
    except Exception as e:
        logger.error(f"âŒ Bot polling error: {e}")
        raise
