import telebot
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
import os
import json
from datetime import datetime, timedelta
import threading
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import socket

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

user_data = {}
user_analytics = {
    "total_users": set(),
    "monthly_users": set(),
    "weekly_users": set(),
    "daily_users": set(),
    "last_reset": datetime.now().date().isoformat(),
    "commands_used": {},
    "feature_usage": {}
}

# Email configuration
EMAIL_CONFIG = {
    "sender_email": "mdzafarsabour35@gmail.com.com",  # Replace with your email
    "sender_password": "twly tnwa jhqw wlmw",  # Replace with your app password
    "receiver_email": "mdzafarsabour35@gmail.com",
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587
}

# File to persist analytics
ANALYTICS_FILE = "user_analytics.json"

def send_email_notification(subject, body):
    """Send email notification"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_CONFIG["sender_email"]
        msg['To'] = EMAIL_CONFIG["receiver_email"]
        msg['Subject'] = subject
        
        # Attach body
        msg.attach(MIMEText(body, 'plain'))
        
        # Create SMTP session
        server = smtplib.SMTP(EMAIL_CONFIG["smtp_server"], EMAIL_CONFIG["smtp_port"])
        server.starttls()
        server.login(EMAIL_CONFIG["sender_email"], EMAIL_CONFIG["sender_password"])
        
        # Send email
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Email notification sent: {subject}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

def load_analytics():
    global user_analytics
    try:
        with open(ANALYTICS_FILE, 'r') as f:
            loaded = json.load(f)
            # Convert sets from lists
            loaded["total_users"] = set(loaded.get("total_users", []))
            loaded["monthly_users"] = set(loaded.get("monthly_users", []))
            loaded["weekly_users"] = set(loaded.get("weekly_users", []))
            loaded["daily_users"] = set(loaded.get("daily_users", []))
            user_analytics = loaded
    except FileNotFoundError:
        save_analytics()

def save_analytics():
    to_save = {
        "total_users": list(user_analytics["total_users"]),
        "monthly_users": list(user_analytics["monthly_users"]),
        "weekly_users": list(user_analytics["weekly_users"]),
        "daily_users": list(user_analytics["daily_users"]),
        "last_reset": user_analytics["last_reset"],
        "commands_used": user_analytics["commands_used"],
        "feature_usage": user_analytics["feature_usage"]
    }
    with open(ANALYTICS_FILE, 'w') as f:
        json.dump(to_save, f)

def track_user(user_id, command="start"):
    """Track user activity"""
    current_date = datetime.now().date()
    
    # Check if we need to reset daily/weekly/monthly counts
    if user_analytics["last_reset"] != current_date.isoformat():
        user_analytics["daily_users"] = set()
        user_analytics["weekly_users"] = set(
            u for u in user_analytics["weekly_users"] 
            if datetime.fromisoformat(u) > datetime.now() - timedelta(days=7)
        ) if user_analytics["weekly_users"] else set()
        user_analytics["monthly_users"] = set(
            u for u in user_analytics["monthly_users"]
            if datetime.fromisoformat(u) > datetime.now() - timedelta(days=30)
        ) if user_analytics["monthly_users"] else set()
        user_analytics["last_reset"] = current_date.isoformat()
    
    # Update user counts
    user_analytics["total_users"].add(user_id)
    user_analytics["daily_users"].add(user_id)
    user_analytics["weekly_users"].add(user_id)
    user_analytics["monthly_users"].add(user_id)
    
    # Track command usage
    user_analytics["commands_used"][command] = user_analytics["commands_used"].get(command, 0) + 1
    
    save_analytics()

# Load analytics on startup
load_analytics()

# ===== FULL DATABASE =====
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
    
    # Send notification email when new user starts
    subject = f"🤖 New User Started Bot"
    body = f"""
Bot Start Notification
━━━━━━━━━━━━━━━━━━━━━

📊 User Details:
• User ID: {message.chat.id}
• Username: @{message.from_user.username if message.from_user.username else 'N/A'}
• First Name: {message.from_user.first_name}
• Last Name: {message.from_user.last_name if message.from_user.last_name else 'N/A'}
• Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📈 Current Statistics:
• Total Users: {len(user_analytics['total_users'])}
• Monthly Users: {len(user_analytics['monthly_users'])}
• Daily Users: {len(user_analytics['daily_users'])}

🤖 Bot Status: Running Successfully
    """
    
    send_email_notification(subject, body)
    
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
    
    bot.send_message(
        message.chat.id,
        "📚 *Select your Semester:*",
        reply_markup=markup,
        parse_mode='Markdown'
    )

# ===== STATISTICS FEATURE =====
@bot.message_handler(func=lambda m: m.text == "📈 Statistics")
def show_statistics(message):
    track_user(message.chat.id, "statistics")
    
    stats_text = "📊 *Bot Usage Statistics*\n"
    stats_text += "━━━━━━━━━━━━━━━━━━━━━\n\n"
    stats_text += f"👥 *Total Users:* {len(user_analytics['total_users'])}\n"
    stats_text += f"📅 *Daily Active Users:* {len(user_analytics['daily_users'])}\n"
    stats_text += f"📆 *Weekly Active Users:* {len(user_analytics['weekly_users'])}\n"
    stats_text += f"📈 *Monthly Active Users:* {len(user_analytics['monthly_users'])}\n\n"
    
    stats_text += "*Top Commands Used:*\n"
    sorted_commands = sorted(user_analytics["commands_used"].items(), key=lambda x: x[1], reverse=True)[:5]
    for cmd, count in sorted_commands:
        stats_text += f"  • {cmd}: {count} times\n"
    
    stats_text += "\n💡 *Note:* Statistics are updated in real-time."
    
    bot.send_message(message.chat.id, stats_text, parse_mode='Markdown')

# ===== HELP FEATURE =====
@bot.message_handler(func=lambda m: m.text == "ℹ️ Help")
def show_help(message):
    track_user(message.chat.id, "help")
    
    help_text = "ℹ️ *Bot Help & Features*\n"
    help_text += "━━━━━━━━━━━━━━━━━━━━━\n\n"
    help_text += "*Available Features:*\n"
    help_text += "📚 *Syllabus* - Download semester-wise syllabus PDFs\n"
    help_text += "   • Available for all semesters (1st to 8th)\n"
    help_text += "   • New & Old syllabus patterns\n"
    help_text += "   • All branches (CE, CS, EE, ECE, ME, IOT)\n\n"
    help_text += "📈 *Statistics* - View bot usage statistics\n"
    help_text += "⭐ *Feedback* - Share your feedback/suggestions\n\n"
    
    help_text += "*How to Use:*\n"
    help_text += "1. Click on '📚 Syllabus'\n"
    help_text += "2. Select your semester\n"
    help_text += "3. Choose your branch\n"
    help_text += "4. Download your syllabus PDF\n\n"
    
    help_text += "*Commands:*\n"
    help_text += "/start - Start the bot\n"
    help_text += "/help - Show this help message\n"
    help_text += "/stats - View bot statistics (Admin only)\n\n"
    
    help_text += "*Support:*\n"
    help_text += "For any issues or suggestions, please use the feedback feature."
    
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')

# ===== FEEDBACK FEATURE =====
@bot.message_handler(func=lambda m: m.text == "⭐ Feedback")
def ask_feedback(message):
    track_user(message.chat.id, "feedback_start")
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🔙 Main Menu")
    
    msg = bot.send_message(
        message.chat.id,
        "⭐ *Share Your Feedback*\n\n"
        "Please send your feedback/suggestions. "
        "This will help us improve the bot.\n\n"
        "You can send:\n"
        "• Feature suggestions\n"
        "• Bug reports\n"
        "• Syllabus corrections\n"
        "• General feedback\n\n"
        "Type your message below:",
        reply_markup=markup,
        parse_mode='Markdown'
    )
    bot.register_next_step_handler(msg, save_feedback)

def save_feedback(message):
    if message.text == "🔙 Main Menu":
        start(message)
        return
    
    track_user(message.chat.id, "feedback_submit")
    
    # Save to file (simple storage)
    with open("feedback.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat()} - User {message.chat.id} ({message.from_user.username}):\n")
        f.write(f"{message.text}\n")
        f.write("-" * 50 + "\n")
    
    # Send email notification for feedback
    subject = f"⭐ New Feedback Received"
    body = f"""
Feedback Received
━━━━━━━━━━━━━━━━━━━━━

📊 User Details:
• User ID: {message.chat.id}
• Username: @{message.from_user.username if message.from_user.username else 'N/A'}
• Name: {message.from_user.first_name}
• Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

💬 Feedback:
{message.text}

━━━━━━━━━━━━━━━━━━━━━
Total Users: {len(user_analytics['total_users'])}
Monthly Users: {len(user_analytics['monthly_users'])}
    """
    
    send_email_notification(subject, body)
    
    bot.send_message(
        message.chat.id,
        "✅ *Thank you for your feedback!*\n\n"
        "Your feedback has been recorded and will help us improve the bot.",
        reply_markup=get_main_menu(),
        parse_mode='Markdown'
    )

# ===== BACK TO MAIN MENU =====
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
    
    bot.send_message(
        message.chat.id,
        f"🏫 *Select your Branch for {message.text}:*",
        reply_markup=markup,
        parse_mode='Markdown'
    )

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
        
        bot.send_document(
            message.chat.id, 
            file_url, 
            caption=f"📚 *{sem} Semester - {branch} Branch*\n\n✅ Download complete!\n\nFor more syllabi, use /start",
            parse_mode='Markdown'
        )
        
        # Send email notification for syllabus download
        subject = f"📚 Syllabus Downloaded"
        body = f"""
Syllabus Downloaded
━━━━━━━━━━━━━━━━━━━━━

📊 User Details:
• User ID: {message.chat.id}
• Username: @{message.from_user.username if message.from_user.username else 'N/A'}
• Name: {message.from_user.first_name}
• Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📚 Download Details:
• Semester: {sem}
• Branch: {branch}
• File: Syllabus PDF

📈 Current Statistics:
• Total Users: {len(user_analytics['total_users'])}
• Monthly Users: {len(user_analytics['monthly_users'])}
        """
        
        send_email_notification(subject, body)
            
        if message.chat.id in user_data:
            del user_data[message.chat.id]
            
    except Exception as e:
        bot.send_message(
            message.chat.id, 
            f"❌ PDF download failed!\n\n🔗 Direct Link: {file_url}\n\nPlease try downloading manually.",
            parse_mode='Markdown'
        )

# ===== ADMIN STATISTICS COMMAND =====
@bot.message_handler(commands=['stats'])
def admin_stats(message):
    # You can add admin user IDs here
    admin_ids = []  # Add admin user IDs like: [123456789, 987654321]
    
    if message.from_user.id in admin_ids:
        stats_text = "📊 *Detailed Bot Statistics*\n\n"
        stats_text += f"👥 Total Users: {len(user_analytics['total_users'])}\n"
        stats_text += f"📈 Monthly Users: {len(user_analytics['monthly_users'])}\n"
        stats_text += f"📆 Weekly Users: {len(user_analytics['weekly_users'])}\n"
        stats_text += f"📅 Daily Users: {len(user_analytics['daily_users'])}\n\n"
        stats_text += f"📊 Command Usage:\n"
        
        sorted_commands = sorted(user_analytics["commands_used"].items(), key=lambda x: x[1], reverse=True)
        for cmd, count in sorted_commands[:10]:
            stats_text += f"  • {c
