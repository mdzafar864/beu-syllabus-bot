import telebot
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import os
import json
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get environment variables
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    logger.error("❌ BOT_TOKEN not found in environment variables!")
    exit(1)

# Email configuration from environment variables
EMAIL_USER = os.getenv("EMAIL_USER", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")

# Add these for debugging
logger.info(f"Email configured: {'Yes' if EMAIL_USER and EMAIL_PASSWORD else 'No'}")

try:
    bot = telebot.TeleBot(TOKEN)
    bot_info = bot.get_me()
    logger.info(f"✅ Bot connected: @{bot_info.username}")
except Exception as e:
    logger.error(f"❌ Bot connection failed: {e}")
    exit(1)

user_data = {}
user_analytics = {
    "total_users": set(),
    "monthly_users": set(),
    "weekly_users": set(),
    "daily_users": set(),
    "last_reset": datetime.now().date().isoformat(),
    "commands_used": {}
}

ANALYTICS_FILE = "user_analytics.json"

def test_email_connection():
    """Test email configuration"""
    if not EMAIL_USER or not EMAIL_PASSWORD:
        logger.warning("Email not configured")
        return False
    
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.set_debuglevel(1)  # Enable debug output
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.quit()
        logger.info("✅ Email connection test successful")
        return True
    except Exception as e:
        logger.error(f"❌ Email connection test failed: {e}")
        return False

def send_email_notification(subject, body, to_email="mdzafarsabour35@gmail.com"):
    """Send email notification with better error handling"""
    if not EMAIL_USER or not EMAIL_PASSWORD:
        logger.warning("Email not configured, skipping notification")
        return False
    
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        logger.info(f"Attempting to send email to {to_email}")
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.set_debuglevel(1)  # Enable debug output
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        logger.info(f"✅ Email sent: {subject}")
        return True
    except Exception as e:
        logger.error(f"❌ Email failed: {e}")
        return False

def load_analytics():
    global user_analytics
    try:
        with open(ANALYTICS_FILE, 'r') as f:
            loaded = json.load(f)
            loaded["total_users"] = set(loaded.get("total_users", []))
            loaded["monthly_users"] = set(loaded.get("monthly_users", []))
            loaded["weekly_users"] = set(loaded.get("weekly_users", []))
            loaded["daily_users"] = set(loaded.get("daily_users", []))
            user_analytics = loaded
            logger.info(f"📊 Analytics loaded: {len(user_analytics['total_users'])} users")
    except FileNotFoundError:
        logger.info("No existing analytics, starting fresh")
        save_analytics()
    except Exception as e:
        logger.error(f"Error loading analytics: {e}")

def save_analytics():
    try:
        to_save = {
            "total_users": list(user_analytics["total_users"]),
            "monthly_users": list(user_analytics["monthly_users"]),
            "weekly_users": list(user_analytics["weekly_users"]),
            "daily_users": list(user_analytics["daily_users"]),
            "last_reset": user_analytics["last_reset"],
            "commands_used": user_analytics["commands_used"]
        }
        with open(ANALYTICS_FILE, 'w') as f:
            json.dump(to_save, f)
    except Exception as e:
        logger.error(f"Error saving analytics: {e}")

def track_user(user_id, command="start"):
    """Track user activity"""
    try:
        current_date = datetime.now().date()
        
        if user_analytics["last_reset"] != current_date.isoformat():
            user_analytics["daily_users"] = set()
            user_analytics["last_reset"] = current_date.isoformat()
        
        user_analytics["total_users"].add(user_id)
        user_analytics["daily_users"].add(user_id)
        user_analytics["commands_used"][command] = user_analytics["commands_used"].get(command, 0) + 1
        
        save_analytics()
    except Exception as e:
        logger.error(f"Error tracking user: {e}")

# Load analytics
load_analytics()

# Test email on startup
test_email_connection()

# ===== SYLLABUS DATABASE WITH VERIFIED LINKS =====
# Note: You need to verify these Google Drive links work
# If they don't work, you'll need to get new shareable links from Google Drive
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
    # ... (rest of your syllabus dictionary remains the same)
}

# Add this function to verify Google Drive links
def verify_google_drive_link(file_id):
    """Check if Google Drive file is accessible"""
    try:
        # Try to get file info without downloading
        url = f"https://drive.google.com/uc?export=download&id={file_id}"
        response = requests.head(url, allow_redirects=True, timeout=10)
        return response.status_code == 200
    except:
        return False

# ===== MAIN MENU =====
def get_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("📚 Syllabus")
    markup.add("📈 Statistics", "ℹ️ Help", "⭐ Feedback")
    return markup

# ===== START COMMAND =====
@bot.message_handler(commands=['start'])
def start(message):
    try:
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
        
        # Send notification with more details
        if EMAIL_USER and EMAIL_PASSWORD:
            subject = "🤖 New User Started Bot"
            body = f"""
New user started the bot!

User ID: {message.chat.id}
Username: @{message.from_user.username if message.from_user.username else 'No username'}
First Name: {message.from_user.first_name}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            send_email_notification(subject, body)
    except Exception as e:
        logger.error(f"Error in start: {e}")
        bot.send_message(message.chat.id, "❌ An error occurred. Please try again.")

# ===== SYLLABUS MENU =====
@bot.message_handler(func=lambda m: m.text == "📚 Syllabus")
def syllabus_menu(message):
    try:
        track_user(message.chat.id, "syllabus")
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add("1stNew", "1stOld")
        markup.add("2ndNew", "2ndOld")
        markup.add("3rdNew", "3rdOld")
        markup.add("4th", "5th")
        markup.add("6th", "7th", "8th")
        markup.add("🔙 Main Menu")
        
        bot.send_message(
            message.chat.id,
            "📚 *Select your Semester:*",
            reply_markup=markup,
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Error in syllabus_menu: {e}")

# ===== STATISTICS =====
@bot.message_handler(func=lambda m: m.text == "📈 Statistics")
def show_statistics(message):
    try:
        track_user(message.chat.id, "statistics")
        
        stats_text = "📊 *Bot Usage Statistics*\n"
        stats_text += "━━━━━━━━━━━━━━━━━━━━━\n\n"
        stats_text += f"👥 *Total Users:* {len(user_analytics['total_users'])}\n"
        stats_text += f"📅 *Daily Active Users:* {len(user_analytics['daily_users'])}\n\n"
        
        stats_text += "*Top Commands Used:*\n"
        sorted_commands = sorted(user_analytics["commands_used"].items(), key=lambda x: x[1], reverse=True)[:5]
        for cmd, count in sorted_commands:
            stats_text += f"  • {cmd}: {count} times\n"
        
        bot.send_message(message.chat.id, stats_text, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Error in statistics: {e}")

# ===== HELP =====
@bot.message_handler(func=lambda m: m.text == "ℹ️ Help")
def show_help(message):
    try:
        help_text = "ℹ️ *Bot Help*\n━━━━━━━━━━━━━━━━━━━━━\n\n"
        help_text += "*How to Use:*\n"
        help_text += "1. Click '📚 Syllabus'\n"
        help_text += "2. Select your semester\n"
        help_text += "3. Choose your branch\n"
        help_text += "4. Download syllabus PDF\n\n"
        help_text += "*Commands:*\n"
        help_text += "/start - Start the bot\n"
        help_text += "/help - Show this help\n\n"
        help_text += "*Note:* If download fails, please try again or contact support."
        
        bot.send_message(message.chat.id, help_text, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Error in help: {e}")

# ===== FEEDBACK =====
@bot.message_handler(func=lambda m: m.text == "⭐ Feedback")
def ask_feedback(message):
    try:
        track_user(message.chat.id, "feedback_start")
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("🔙 Main Menu")
        
        msg = bot.send_message(
            message.chat.id,
            "⭐ *Share Your Feedback*\n\nType your message below:",
            reply_markup=markup,
            parse_mode='Markdown'
        )
        bot.register_next_step_handler(msg, save_feedback)
    except Exception as e:
        logger.error(f"Error in feedback: {e}")

def save_feedback(message):
    try:
        if message.text == "🔙 Main Menu":
            start(message)
            return
        
        track_user(message.chat.id, "feedback_submit")
        
        with open("feedback.txt", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()} - User {message.chat.id}: {message.text}\n")
        
        bot.send_message(
            message.chat.id,
            "✅ *Thank you for your feedback!*",
            reply_markup=get_main_menu(),
            parse_mode='Markdown'
        )
        
        # Send feedback via email
        if EMAIL_USER and EMAIL_PASSWORD:
            subject = "⭐ New Feedback Received"
            body = f"""
New feedback from user!

User ID: {message.chat.id}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Feedback: {message.text}
            """
            send_email_notification(subject, body)
            
    except Exception as e:
        logger.error(f"Error saving feedback: {e}")

# ===== BACK BUTTON =====
@bot.message_handler(func=lambda m: m.text == "🔙 Main Menu")
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
        
        for i in range(0, len(available_branches), 2):
            if i + 1 < len(available_branches):
                markup.add(available_branches[i], available_branches[i+1])
            else:
                markup.add(available_branches[i])
        
        markup.add("🔙 Main Menu")
        
        bot.send_message(
            message.chat.id,
            f"🏫 *Select your Branch for {message.text}:*",
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
            bot.send_message(message.chat.id, "❌ Please select semester first!")
            return
        
        sem = data["sem"]
        branch = message.text
        
        if branch not in syllabus[sem]:
            bot.send_message(message.chat.id, f"❌ *{branch}* not available for {sem}!", parse_mode='Markdown')
            return
        
        file_url = syllabus[sem][branch]
        
        # Send a "processing" message
        processing_msg = bot.send_message(
            message.chat.id, 
            f"📥 *Fetching {branch} Syllabus ({sem})...*\n\nPlease wait while I prepare the download...", 
            parse_mode='Markdown'
        )
        
        try:
            # Try to send the document
            bot.send_document(
                message.chat.id, 
                file_url, 
                caption=f"📚 *{sem} Semester - {branch} Branch*\n\n✅ Download complete!",
                parse_mode='Markdown',
                timeout=30  # Add timeout
            )
            
            # Delete processing message
            bot.delete_message(message.chat.id, processing_msg.message_id)
            
        except Exception as download_error:
            logger.error(f"Download error: {download_error}")
            bot.delete_message(message.chat.id, processing_msg.message_id)
            
            # Send fallback message with direct link
            bot.send_message(
                message.chat.id,
                f"⚠️ *Direct download failed!*\n\n"
                f"Please try downloading from this link:\n"
                f"{file_url}\n\n"
                f"*{sem} Semester - {branch} Branch*",
                parse_mode='Markdown'
            )
        
        # Clear user data
        if message.chat.id in user_data:
            del user_data[message.chat.id]
            
    except Exception as e:
        logger.error(f"Error in send_pdf: {e}")
        bot.send_message(
            message.chat.id, 
            "❌ Download failed! Please try again.\n\n"
            "If the problem persists, contact support.",
            parse_mode='Markdown'
        )

# ===== DEFAULT HANDLER =====
@bot.message_handler(func=lambda m: True)
def default_handler(message):
    bot.send_message(
        message.chat.id,
        "❓ Unknown command!\n\nPlease use the menu buttons:",
        reply_markup=get_main_menu(),
        parse_mode='Markdown'
    )

# ===== BOT START NOTIFICATION =====
def send_bot_start_notification():
    """Send notification when bot starts"""
    if EMAIL_USER and EMAIL_PASSWORD:
        subject = "🚀 BEU Syllabus Bot Started"
        body = f"""
Bot Started Successfully!

Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Bot Name: @{bot_info.username}
Total Users: {len(user_analytics['total_users'])}
Email Status: {'Configured' if EMAIL_USER and EMAIL_PASSWORD else 'Not Configured'}

The bot is now running and accepting requests.
        """
        send_email_notification(subject, body)

# ===== RUN BOT =====
if __name__ == "__main__":
    logger.info("="*50)
    logger.info("🚀 BEU Syllabus Bot Starting...")
    logger.info(f"🤖 Bot: @{bot_info.username}")
    logger.info(f"📊 Total Users: {len(user_analytics['total_users'])}")
    logger.info(f"📧 Email: {'Configured' if EMAIL_USER and EMAIL_PASSWORD else 'Not Configured'}")
    logger.info("="*50)
    
    # Send startup notification
    send_bot_start_notification()
    
    logger.info("✅ Bot is polling...")
    
    try:
        bot.infinity_polling(timeout=60, skip_pending=True)
    except Exception as e:
        logger.error(f"❌ Bot polling error: {e}")
        raise
