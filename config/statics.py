# NOTE:========================== DISCORD BOT CONFIGURATION ==========================
TOKEN = "YOUR_DISCORD_BOT_TOKEN"
NAME = ("YOUR_BOT_NAME")  
PREFIX = "YOUR_BOT_PREFIX"  
STATUS = [
    "Default Status",
    "Custom Status 1",
    "Custom Status 2",
    "Custom Status 3"
] 

# NOTE:========================== FILE PATHS (FIX) ==========================
ERROR_LOG_PATH = "logs/error/error.log"  
SECURITY_LOG_PATH = "logs/security/security.log"  
TEMP_UPLOAD_PATH = "home/cluster/temp" 
ROM_PATH = "home/cluster/rom.json"  
CONTROLLER_PATH = "config/controller/settings.json" 

# NOTE:========================== MEMORY PARAMETERS ==========================
ROM_LIMIT = 5  
ROM_UPDATE_TIME = 5  # (time between each persistent memory update in minutes)
MEMORY_MAX_INACTIVE_TIME = 5  # (max inactivity duration per user before memory deletion in hours)
MEMORY_CLEAR_TIME = 1440  # (time between each "RAM & ROM" memory cleanup in minutes)

# NOTE:========================== STYLE PARAMETERS ==========================
TYPING_TIME = 0.1  # bot response time in seconds
STATUS_TIME = 2  # time between each status change in seconds
SLOWTYPE_TIME = 0.1  # bot response time in seconds for slowtype

# NOTE:========================== AI PARAMETERS ==========================
KEY = "YOUR_GROQ_API_KEY"
MODEL = "AI-MODEL-NAME" 
FREQUENCY = 1 
TEMPERATURE = 0  
MAX_TOKENS = 256  
TOP_P = 0.95  
PRESENCE_PENALTY = 0 
STOP = ["\n", "User:", "BOT:", "Assistant:"]  # (stop words, phrases, or symbols)
LIMIT_MEMORY = 5 # max number of messages in the conversation history

# NOTE:========================== AI PROMPT ==========================
PROMPT = ("DESCRIPTION OF YOUR BOT PERSONALITY: Name and how it should respond to users. ")