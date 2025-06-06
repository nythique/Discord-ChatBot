from config import statics
from colorama import Fore, Style
from groq import Groq
from config import statics
from home.cluster.ram import memory
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

class ollama:
    def __init__(self):
        try:
            logging.info("[INFO] ollama class initialization...")
            self.groq_client = Groq(api_key=statics.KEY) 
            self.conversation_history = []
            logging.info("[INFO] ollama class successfully initialized.")
        except Exception as e:
            logging.error(f"[ERROR] Error during ollama class initialization: {e}")
            print(Fore.RED + f"[ERROR] Error during ollama class initialization: {e}" + Style.RESET_ALL)
            raise

    def ask_ollama(self, question, username=None, messages=None):
        try:
            logging.info(f"[INFO] Searching for an answer to the message: {question}")
            print(Fore.MAGENTA + f"[INFO] Answering the message" + Style.RESET_ALL)
            if messages:
                prompt_messages = messages
            else:
                system_prompt = (
                    statics.PROMPT +
                    (f"\nThe Discord user you are chatting with is called: {username}. " if username else "") +
                    "Use this name/nickname in your answers if relevant, but don't repeat it systematically. Be natural and relevant."
                )
                prompt_messages = [{"role": "system", "content": system_prompt}]
                if question:
                    prompt_messages.append({"role": "user", "content": question})

            response = self.groq_client.chat.completions.create(
                model=statics.MODEL,
                messages=prompt_messages,
                temperature=statics.TEMPERATURE,
                max_tokens=statics.MAX_TOKENS,
                top_p=statics.TOP_P,
                frequency_penalty=statics.FREQUENCY,
                presence_penalty=statics.PRESENCE_PENALTY,
            )
            try:
                logging.info(f"[INFO] Generating the answer")
                reply = response.choices[0].message.content.strip()
                self.conversation_history.append({"role": "assistant", "content": reply})
                logging.info(f"[INFO] Answer generated successfully")
                return reply
            except Exception as e:
                logging.error(f"[ERROR] Error while retrieving the answer: {e}")
                print(Fore.RED + f"[ERROR] Error while retrieving the answer: {e}" + Style.RESET_ALL)
                return "Sorry, an error occurred. Please try again later."
        except Exception as e:
            logging.error(f"[ERROR] Error while searching for the answer: {e}")
            print(Fore.RED + f"[ERROR] Error while searching for the answer" + Style.RESET_ALL)
            return "Sorry, an error occurred. Please try again later."

    def get_answer(self, messages, username=None):
        try:
            logging.info(f"[INFO] Retrieving the user's message")
            print(Fore.MAGENTA + f"[INFO] Retrieving the user's message" + Style.RESET_ALL)
            question = "" 
            for msg in reversed(messages):
                if msg["role"] == "user":
                    question = msg["content"]
                    break
            if not question.strip():
                logging.warning("[WARNING] Empty or invalid message.")
                return "I can't answer an empty message."
            
            if not hasattr(self, "user_histories"):
                self.user_histories = {}
            if username not in self.user_histories:
                self.user_histories[username] = []
            self.user_histories[username].append({"role": "user", "content": question})
             
            if not messages or not isinstance(messages, list):
                messages = [] 
            
            try:
                logging.info(f"[INFO] Calling ask_ollama with the message: {question}")
                print(Fore.MAGENTA + f"[INFO] Calling ask_ollama" + Style.RESET_ALL)
                api_response = self.ask_ollama(question, username, messages=messages)
                return api_response
            except Exception as e:
                logging.error(f"[ERROR] Error while calling ask_ollama: {e}")
                print(Fore.RED + f"[ERROR] Error while calling ask_ollama" + Style.RESET_ALL)
                return "Sorry, an error occurred. Please try again later."

        except Exception as e:
            logging.error(f"[ERROR] Error while retrieving the user's message: {e}")
            print(Fore.RED + f"[ERROR] Error while retrieving the user's message" + Style.RESET_ALL)
            return "Sorry, an error occurred. Please try again later."