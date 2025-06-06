import discord, logging
from discord.ext import commands
from config import statics
from colorama import Fore, Style

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

def create_bot():
    try:
        logging.info("[INFO] Configuring Discord clients...")
        print(Fore.GREEN + "[INFO] Configuring Discord clients..." + Style.RESET_ALL)
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True
        bot = commands.Bot(command_prefix=statics.PREFIX, help_command=None, intents=intents)
        logging.info("[INFO] Discord clients configured successfully.")
        print(Fore.GREEN + "[INFO] Discord clients configured successfully." + Style.RESET_ALL)
        return bot
    except Exception as e:
        logging.error(f"[ERROR] Error while configuring Discord clients: {e}")
        return None
