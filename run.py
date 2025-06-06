from bot.bot import bot
from config import statics
from colorama import Fore, Style
from config.statics import TOKEN, ERROR_LOG_PATH, SECURITY_LOG_PATH
import logging, datetime

info_handler = logging.FileHandler(statics.SECURITY_LOG_PATH, encoding='utf-8')
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
))

error_handler = logging.FileHandler(statics.ERROR_LOG_PATH, encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
))

logging.getLogger().handlers = []
logging.getLogger().addHandler(info_handler)
logging.getLogger().addHandler(error_handler)
logging.getLogger().setLevel(logging.INFO)

if __name__ == "__main__":
    try:
        logging.info("[INFO] Starting the bot...")
        print(Fore.GREEN + "[INFO] Starting the bot..." + Style.RESET_ALL)
        bot.run(TOKEN)
    except KeyboardInterrupt:
        logging.warning("[WARNING] Bot stopped by user.")
    except Exception as e:
        logging.error(f"[ERROR] Error while starting the bot: {e}")
        print(Fore.RED + f"[ERROR] Error while starting the bot: {e}" + Style.RESET_ALL)
