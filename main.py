import telebot
from telebot.types import ReplyKeyboardMarkup
import os

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    print("❌ BOT_TOKEN not found")
    exit()

bot = telebot.TeleBot(TOKEN)

user_data = {}

# ===== FULL DATABASE =====
syllabus = {
    # (तुम्हारा पूरा database same रहेगा — कोई change नहीं)
}

# ===== START =====
@bot.message_handler(commands=['start'])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("1stNew","1stOld","2ndNew","2ndOld","3rdNew","3rdOld","4th","5th","6th","7th","8th")
    
    bot.send_message(message.chat.id,
                     "📚 Select Semester",
                     reply_markup=markup)

# ===== SEM SELECT =====
@bot.message_handler(func=lambda m: m.text in syllabus.keys())
def sem_select(message):
    user_data[message.chat.id] = {"sem": message.text}
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("CE","CS","EE","ECE","ME","IOT")  # IOT add किया
    
    bot.send_message(message.chat.id,
                     "🏫 Select Branch",
                     reply_markup=markup)

# ===== BRANCH SELECT =====
@bot.message_handler(func=lambda m: m.text in ["CE","CS","EE","ECE","ME","IOT"])
def send_pdf(message):
    data = user_data.get(message.chat.id)
    
    if not data:
        bot.send_message(message.chat.id, "❌ पहले semester select करो")
        return
    
    sem = data["sem"]
    branch = message.text
    
    try:
        file_url = syllabus[sem][branch]
        
        bot.send_message(message.chat.id, "📥 Sending PDF...")
        bot.send_document(message.chat.id, file_url)
        
    except KeyError:
        bot.send_message(message.chat.id, "❌ इस branch का PDF available नहीं है")
    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Error आया, बाद में try करो")
        print(e)

# ===== RUN =====
print("🚀 Bot Started Successfully...")
bot.infinity_polling(skip_pending=True)
