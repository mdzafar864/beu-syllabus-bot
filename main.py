import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8580811042:AAEhBmCTKztZV41PJb3Hm01gmdOvoZ4A3Xk"

bot = telebot.TeleBot(TOKEN)

# Start Command with Buttons
@bot.message_handler(commands=['start'])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    
    btn1 = KeyboardButton("CSE")
    btn2 = KeyboardButton("ECE")
    btn3 = KeyboardButton("ME")
    btn4 = KeyboardButton("CE")
    
    markup.add(btn1, btn2, btn3, btn4)
    
    bot.send_message(message.chat.id,
    "👋 Welcome to BEU Syllabus Bot\n\n"
    "👉 Select your Branch",
    reply_markup=markup)

# Handle Branch Selection
@bot.message_handler(func=lambda message: message.text in ["CSE", "ECE", "ME", "CE"])
def branch_selected(message):
    branch = message.text
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    
    for i in range(1, 9):
        markup.add(KeyboardButton(f"Sem {i}"))
    
    bot.send_message(message.chat.id,
    f"📚 {branch} selected\n\n👉 Select Semester",
    reply_markup=markup)
    
    bot.register_next_step_handler(message, lambda msg: send_syllabus(msg, branch))

# Send Syllabus Link
def send_syllabus(message, branch):
    try:
        sem = message.text.split(" ")[1]
        
        link = f"https://mdzafar864.github.io/BEU-Syllabus-App/?branch={branch}&sem={sem}"
        
        bot.send_message(message.chat.id,
        f"📚 Your Syllabus:\n{link}")
        
    except:
        bot.send_message(message.chat.id, "❌ Please select valid semester")

# Run Bot
bot.infinity_polling()
