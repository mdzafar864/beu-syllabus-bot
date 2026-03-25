import telebot
from telebot.types import ReplyKeyboardMarkup
import os

TOKEN = os.getenv("8580811042:AAEnH_ETPkcvVaRcltXr4XwIp4wqvhx2V8c")
bot = telebot.TeleBot(TOKEN)

user_data = {}

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
    markup.add("CE","CS","EE","ECE","ME")
    
    bot.send_message(message.chat.id,
                     "🏫 Select Branch",
                     reply_markup=markup)

# ===== BRANCH SELECT =====
@bot.message_handler(func=lambda m: m.text in ["CE","CS","EE","ECE","ME"])
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
        
    except:
        bot.send_message(message.chat.id, "❌ PDF not available")

# ===== RUN =====
print("Bot Started...")
bot.infinity_polling(skip_pending=True)
