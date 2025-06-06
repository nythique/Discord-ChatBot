from home.core.client import create_bot
from home.core.main import register_commands
from colorama import Fore, Style
from config import statics
import logging

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

try:
    logging.info("[INFO] Bot initialization...")
    print(Fore.GREEN + "[INFO] Bot initialization..." + Style.RESET_ALL)
    bot = create_bot()
    register_commands(bot)
except Exception as e:
    logging.error(f"[ERROR] Error during bot initialization: {e}")
    print(Fore.RED + f"[ERROR] Error during bot initialization: {e}" + Style.RESET_ALL)
    