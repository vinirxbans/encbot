import os
import time
import base64
import marshal
import random
import zlib
import requests
import telebot
from telebot import types
import requests


TOKEN = "7390865838:AAFnrHEQs3URPB71QP8Wzn8iv9lyDEF84Qs"
bot = telebot.TeleBot(TOKEN)

DONATE_QR_URL = "https://i.postimg.cc/GmFpn3fM/qr.png" 
DONATE_MESSAGE = """
❤️ *Support My Work* ❤️

Scan this QR to donate via UPI/Paytm/Gpay.
UPI ID: `vikhyat7@fam`

_Every contribution helps improve this tool!_
""" 


@bot.message_handler(commands=['start'])

def send_instructions(message):
    help_msg = """
    ⚡ *ADV ENC BOT BY VINI RX | TELEGRAM @u_xjoy*
    
    *Available Commands💗*
    `/start` - To Start The Bot
    `/enc` - To Start Encryption
    `/donate` - Support my work
    `/about` - About the bot
    """
    bot.reply_to(message, help_msg, parse_mode="Markdown")

@bot.message_handler(commands=['donate'])
def send_donate(message):
    try:
        
        bot.send_photo(
            message.chat.id,
            DONATE_QR_URL,
            caption=DONATE_MESSAGE,
            parse_mode="Markdown"
        )
    except Exception as e:
        
        bot.reply_to(message, 
                   "📲 *Donate via UPI ID:* `vikhyat7@fam`\n"
                   "❌ QR code unavailable - please copy UPI ID",
                   parse_mode="Markdown")

@bot.message_handler(commands=['about'])
def send_about(message):
        about_msg = """
    *ADVANCED ENC BOT BY @u_xjoy ✨ 
     INSTAGRAM : @9.3.3.1🫶💗*"""
        
        bot.reply_to(message, about_msg, parse_mode="Markdown")


user_selections = {}


zlb = lambda data: zlib.compress(data)
b64 = lambda data: base64.b64encode(data)
b32 = lambda data: base64.b32encode(data)
b16 = lambda data: base64.b16encode(data)
mar = lambda data: marshal.dumps(compile(data, 'module', 'exec'))


@bot.message_handler(commands=['enc'])
def start(message):
    send_main_menu(message.chat.id)


def send_main_menu(chat_id):
    buttons = [
        types.InlineKeyboardButton("🛠 Base64", callback_data='base64'),
        types.InlineKeyboardButton("🛠 Marshal", callback_data='marshal'),
        types.InlineKeyboardButton("🛠 Zlib", callback_data='zlib'),
        types.InlineKeyboardButton("🛠 Advanced", callback_data='advanced'),
        types.InlineKeyboardButton("🛠 B16", callback_data='base16'),
        types.InlineKeyboardButton("🛠 B32", callback_data='base32'),
        types.InlineKeyboardButton("🛠 MZlib", callback_data='marshal_zlib'),
        types.InlineKeyboardButton("🛠 Complex", callback_data='complex'),
        types.InlineKeyboardButton("ℹ️ Bot Info", callback_data='bot_info')
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*buttons)
    bot.send_message(chat_id, "🔒 Choose an encryption method:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id

    if call.data == "bot_info":
        send_bot_info(call.message)
    elif call.data == "back":
        bot.edit_message_text("🔒 Choose an encryption method:", chat_id=chat_id, message_id=call.message.message_id)
        send_main_menu(chat_id)  
    else:
        user_selections[chat_id] = call.data
        bot.send_message(chat_id, f"📂 Send a file for {call.data} encryption.")


def send_bot_info(message):
    info_text = """
🤖 <b>Bot Name:</b>File Encryptor

<blockquote>💻 <b>Coding Launguage : </b> Python🐍
👤 <b>Owner :</b> @u_xjoy
🛠 <b>Created By : VINI RX WITH 💗 </b>
[◉°] <b>INSTAGRAM : @9.3.3.1</b>
✴ <b>Version : v1.0⚡ </b>

</blockquote>

<b>This bot encrypts Python scripts using various encoding methods.</b>
"""
    markup = types.InlineKeyboardMarkup()
    back_button = types.InlineKeyboardButton("⬅️ Back", callback_data="back")
    markup.add(back_button)
    bot.edit_message_text(info_text, chat_id=message.chat.id, message_id=message.message_id, parse_mode="HTML", reply_markup=markup)


@bot.message_handler(content_types=['document'])
def receive_file(message):
    try:
        chat_id = message.chat.id

        
        if chat_id not in user_selections:
            bot.send_message(chat_id, "❌ Please select an encryption method first!")
            return

        encryption_type = user_selections[chat_id]

        
        send_reaction(chat_id, message.message_id, "👨🏻‍💻")

        
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_id = str(random.randint(1000, 9999))
        file_name = f"{encryption_type}-{file_id}.py"

        with open(file_name, 'wb') as f:
            f.write(downloaded_file)

        
        loading_msg = bot.send_message(chat_id, "⚙️ Processing your file...\n[0%] █▒▒▒▒▒▒▒▒▒")
        for i in range(1, 101, random.randint(7, 14)):
            time.sleep(0.02)
            bot.edit_message_text(chat_id=chat_id, message_id=loading_msg.message_id, text=f"⚙️ Processing your file...\n[{i}%] {'█' * (i // 10)}{'▒' * (10 - (i // 10))}")

        
        encrypted_code = encrypt_file(encryption_type, file_name)

        with open(file_name, 'w') as f:
            f.write(encrypted_code)

        
        bot.delete_message(chat_id, loading_msg.message_id)

        
        with open(file_name, 'rb') as file:
            bot.send_document(chat_id, file)

        os.remove(file_name)  

    except Exception as e:
        bot.send_message(chat_id, f"❌ Error: {e}")


def send_reaction(chat_id, message_id, emoji):
    url = f"https://api.telegram.org/bot{TOKEN}/setMessageReaction"
    data = {
        "chat_id": chat_id,
        "message_id": message_id,
        "reaction": [{"type": "emoji", "emoji": emoji}]
    }
    requests.post(url, json=data)


def encrypt_file(method, file_name):
    original_code = open(file_name, "r").read().encode('utf-8')
    header = "#By @9.3.3.1 VINI RX\n\n"
    footer = "\n\n #By @9.3.3.1 VINI RX\n\n"

    if method == "base64":
        encoded = b64(original_code)[::-1]
        return f"{header}_ = lambda __ : __import__('base64').b64decode(__[::-1]);exec((_)({encoded})) {footer}"

    elif method == "marshal":
        encoded = marshal.dumps(compile(original_code.decode(), 'module', 'exec'))
        return f"{header}import marshal\nexec(marshal.loads({encoded})) {footer}"

    elif method == "zlib":
        encoded = b64(zlb(original_code))[::-1]
        return f"{header}_ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));exec((_)({encoded})) {footer}"

    elif method == "base16":
        encoded = b16(zlb(original_code))[::-1]
        return f"{header}_ = lambda __ : __import__('zlib').decompress(__import__('base64').b16decode(__[::-1]));exec((_)({encoded})) {footer}"

    elif method == "base32":
        encoded = b32(zlb(original_code))[::-1]
        return f"{header}_ = lambda __ : __import__('zlib').decompress(__import__('base64').b32decode(__[::-1]));exec((_)({encoded})) {footer}"

    elif method == "marshal_zlib":
        encoded = b64(zlb(mar(original_code)))[::-1]
        return f"{header}import marshal, zlib, base64\nexec(marshal.loads(zlib.decompress(base64.b64decode({encoded})))) {footer}"

    elif method == "advanced":
        var1, var2, var3 = random.sample(['x', 'y', 'z', 'p', 'q', 'r'], 3)
        encoded = b64(zlb(mar(original_code)))[::-1]
        return f"""{header}
import base64, zlib, marshal
{var1} = lambda {var2}: marshal.loads(zlib.decompress(base64.b64decode({var2})))
{var3} = "{encoded}"
exec({var1}({var3})) {footer}"""

    return " # Error Invalid Encryption Method"




bot.polling(True)