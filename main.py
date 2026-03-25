import telebot
from telebot.types import ReplyKeyboardMarkup
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

user_data = {}

# Start
@bot.message_handler(commands=['start'])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("CSE", "ECE", "ME", "CE")
    
    bot.send_message(
        message.chat.id,
        "👋 Welcome to BEU Syllabus Bot\n\n👉 Select your Branch",
        reply_markup=markup
    )

# Branch Select
@bot.message_handler(func=lambda m: m.text in ["CSE","ECE","ME","CE"])
def branch(message):
    user_data[message.chat.id] = message.text
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(1,9):
        markup.add(f"Sem {i}")
    
    bot.send_message(
        message.chat.id,
        f"📚 {message.text} selected\n\n👉 Select Semester",
        reply_markup=markup
    )

# Semester Select
@bot.message_handler(func=lambda m: m.text.startswith("Sem"))
def semester(message):
    branch = user_data.get(message.chat.id)
    
    if not branch:
        bot.send_message(message.chat.id, "❌ पहले branch select करो")
        return
    
    sem = message.text.split()[1]
    
    link = f"https://mdzafar864.github.io/BEU-Syllabus-App/?branch={branch}&sem={sem}"
    
    bot.send_message(message.chat.id, f"📚 Your Syllabus:\n{link}")

# Run
bot.infinity_polling()
