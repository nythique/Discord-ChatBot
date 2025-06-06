import datetime, os, json, logging
from colorama import Fore, Style
from config import statics

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

class memory:
    def __init__(self, max_history=statics.ROM_LIMIT):
        try:
            logging.info("[INFO] Initializing memory...")
            print(Fore.GREEN + "[INFO] Initializing memory..." + Style.RESET_ALL)
            self.conversations = {}
            self.max_history = max_history
            self.last_message_time = {}
            self.modified = False
            self.load_from_file()
        except Exception as e:
            logging.error(f"[ERROR] Error during memory initialization: {e}")
            print(Fore.RED + f"[ERROR] Error during memory initialization" + Style.RESET_ALL)

    def clear_context(self, inactive_time_threshold=statics.MEMORY_MAX_INACTIVE_TIME * 3600):
        """Deletes memory for users inactive for more than inactive_time_threshold seconds."""
        try:
            logging.info("[INFO] Removing memory for inactive users...")
            print(Fore.GREEN + "[INFO] Removing memory for inactive users..." + Style.RESET_ALL)
            now = datetime.datetime.now()
            to_remove = []
            for user_id, last_time in self.last_message_time.items():
                if (now - last_time).total_seconds() > inactive_time_threshold:
                    to_remove.append(user_id)
            for user_id in to_remove:
                self.conversations.pop(user_id, None)
                self.last_message_time.pop(user_id, None)
                self.modified = True
                logging.info(f"[INFO] Memory deleted for user {user_id}.")
                print(Fore.YELLOW + f"[INFO] Memory deleted for user {user_id}." + Style.RESET_ALL)
        except Exception as e:
            logging.error(f"[ERROR] Error while deleting memory: {e}")
            print(Fore.RED + f"[ERROR] Error while deleting memory" + Style.RESET_ALL)

    def manage(self, user_id, message_content):
        """Manages user memory by adding a message to the history."""
        try:
            logging.info("[INFO] Managing memory...")
            print(Fore.GREEN + "[INFO] Managing memory..." + Style.RESET_ALL)
            user_id = str(user_id)
            if user_id not in self.conversations:
                self.conversations[user_id] = []
            if not self.conversations[user_id] or self.conversations[user_id][-1] != message_content:
                self.conversations[user_id].append(message_content)
                self.modified = True
            self.last_message_time[user_id] = datetime.datetime.now()
            if self.max_history > 0:
                self.conversations[user_id] = self.conversations[user_id][-self.max_history:]
            self.save_to_file()  # Automatic save after each addition
            logging.info(f"[INFO] Memory updated for user {user_id}.")
            print(Fore.YELLOW + f"[INFO] Memory updated for user {user_id}." + Style.RESET_ALL)
            return self.conversations[user_id]
        except Exception as e:
            logging.error(f"[ERROR] Error while managing memory: {e}")
            print(Fore.RED + f"[ERROR] Error while managing memory" + Style.RESET_ALL)

    def get_history(self, user_id):
        """Retrieves the message history of a user."""
        try:
            logging.info("[INFO] Retrieving history...")
            user_id = str(user_id)
            return self.conversations.get(user_id, [])
        except Exception as e:
            logging.error(f"[ERROR] Error while retrieving history: {e}")
            print(Fore.RED + f"[ERROR] Error while retrieving history" + Style.RESET_ALL)

    def save_to_file(self):
        try:
            logging.info("[INFO] Saving memory...")
            print(Fore.GREEN + "[INFO] Saving memory..." + Style.RESET_ALL)
            with open(statics.ROM_PATH, "w", encoding="utf-8") as f:
                json.dump({
                    "conversations": self.conversations,
                    "last_message_time": {k: v.isoformat() for k, v in self.last_message_time.items()}
                }, f, indent=4, ensure_ascii=False)
            self.modified = False
            logging.info("[INFO] Memory saved successfully.")
            print(Fore.YELLOW + "[INFO] Memory saved successfully." + Style.RESET_ALL)
        except Exception as e:
            logging.error(f"[ERROR] Error while saving memory: {e}")
            print(Fore.RED + f"[ERROR] Error while saving memory" + Style.RESET_ALL)

    def load_from_file(self):
        """Loads memory from a JSON file."""
        try:
            logging.info("[INFO] Checking memory file...")
            if not os.path.exists(statics.ROM_PATH):
                return
            logging.info("[INFO] Memory file checked.")
        except Exception as e:
            logging.error(f"[ERROR] Error while checking memory file: {e}")
            print(Fore.RED + f"[ERROR] Error while checking memory file" + Style.RESET_ALL)
            return
        try:
            logging.info("[INFO] Loading memory...")
            with open(statics.ROM_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.conversations = data.get("conversations", {})
                self.last_message_time = {
                    k: datetime.datetime.fromisoformat(v) for k, v in data.get("last_message_time", {}).items()
                }
            logging.info("[INFO] Memory loaded successfully.")
        except Exception as e:
            logging.error(f"[ERROR] Error while loading memory: {e}")
            print(Fore.RED + f"[ERROR] Error while loading memory" + Style.RESET_ALL)