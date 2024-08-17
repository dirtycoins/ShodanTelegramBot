import telebot
import logging
from config import TELEGRAM_BOT_TOKEN, USER_DATA_FILE, ADMIN_ID
from helpers import load_user_data, save_user_data
from commands import register_commands
import time

# Cấu hình logging
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Tải dữ liệu người dùng
user_data = load_user_data(USER_DATA_FILE)

# Đăng ký các lệnh
register_commands(bot, user_data)

if __name__ == "__main__":
    logger.info("Bot đã khởi động")
    while True:
        try:
            bot.infinity_polling()
        except Exception as e:
            logger.error(f"Lỗi polling bot: {str(e)}")
            time.sleep(10)
