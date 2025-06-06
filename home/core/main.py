from gen.smart import ollama
from colorama import Fore, Style
from config import statics
from datetime import datetime
from itertools import cycle
from discord.ext import commands, tasks
from discord.ui import View, Button, Modal, TextInput, Select
from home.cluster.ram import memory
import discord, time, os, sys, json, logging, asyncio

ia = ollama()
status = statics.STATUS
user_memory = memory()
bot = None


"""Handler pour les logs info et warning"""
info_handler = logging.FileHandler(statics.SECURITY_LOG_PATH, encoding='utf-8')
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
))

"""Handler pour les logs error"""
error_handler = logging.FileHandler(statics.ERROR_LOG_PATH, encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
))

"""On réinitialise la config root et on ajoute les handlers"""
logging.getLogger().handlers = []
logging.getLogger().addHandler(info_handler)
logging.getLogger().addHandler(error_handler)
logging.getLogger().setLevel(logging.INFO)


def slowType(text, delay=statics.SLOWTYPE_TIME):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)

async def config_loading():
    try:
        logging.info("[INFO] Loading configuration...")
        with open(statics.CONTROLLER_PATH, "r", encoding="utf-8") as f:
            settings = json.load(f)
        blacklist_user = settings.get("blacklist_user", [])
        blacklist_server = settings.get("blacklist_server", [])
        admin_user = settings.get("admin", [])
        root_user = settings.get("root_user", [])
        alert_room = settings.get("alert_room", [])
        logging.info(f"[INFO] Configuration loaded successfully.")
    except Exception as e:
        logging.error(f"[ERROR] An error occurred while loading configuration: {e}")
        print(Fore.RED + f"[ERROR] An error occurred while loading configuration" + Style.RESET_ALL)
        blacklist_user = []
        blacklist_server = []
    return blacklist_user, blacklist_server, admin_user, alert_room, root_user

status = cycle(status) 
@tasks.loop(seconds=statics.STATUS_TIME)
async def status_swap(bot):
    """Changes the Discord bot status at regular intervals"""
    try:
        await bot.change_presence(activity=discord.CustomActivity(next(status)))
        logging.info(f"[INFO] Status changed: {next(status)}")
    except Exception as e:
        print(Fore.RED + f"[ERROR] An error occurred while changing status" + Style.RESET_ALL)
        logging.error(f"[ERROR] An error occurred while changing status: {e}")

@tasks.loop(minutes=statics.ROM_UPDATE_TIME)
async def save_memory_periodically():
    try:
        print(Fore.CYAN + "[INFO] Periodic memory save..." + Style.RESET_ALL)
        logging.info(f"[INFO] Periodic memory save...")
        if user_memory.modified:
            user_memory.save_to_file()
            user_memory.modified = False
            print(Fore.GREEN + "[INFO] Memory save successful." + Style.RESET_ALL)
            logging.info(f"[INFO] Memory save successful.")
        else:
            logging.info("[INFO] No changes detected in memory. Save skipped.")
            print(Fore.YELLOW + "[INFO] No changes detected in memory. Save skipped." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"[ERROR] Periodic memory save failed" + Style.RESET_ALL)
        logging.error(f"[ERROR] Periodic memory save failed: {e}")

@save_memory_periodically.before_loop
async def before_save_memory():
    try:
        print(Fore.YELLOW + "[INFO] Waiting for the bot to be ready to start periodic memory save..." + Style.RESET_ALL)
        logging.info(f"[INFO] Waiting for the bot to be ready to start periodic memory save...")
        await bot.wait_until_ready()
    except Exception as e:
        print(Fore.RED + f"[ERROR] An error occurred while waiting before periodic memory save" + Style.RESET_ALL)
        logging.error(f"[ERROR] An error occurred while waiting before periodic memory save: {e}")

@tasks.loop(minutes=statics.MEMORY_CLEAR_TIME)
async def clear_inactive_users():
    try:
        print(Fore.CYAN + "[INFO] Cleaning inactive users..." + Style.RESET_ALL)
        logging.info(f"[INFO] Cleaning inactive users...")
        user_memory.clear_context()
        user_memory.save_to_file()  # <-- save the cleanup in ROM
        print(Fore.GREEN + "[INFO] Inactive users cleaned successfully." + Style.RESET_ALL)
        logging.info(f"[INFO] Inactive users cleaned successfully.")
    except Exception as e:
        print(Fore.RED + f"[ERROR] Cleaning inactive users failed: {e}" + Style.RESET_ALL)
        logging.error(f"[ERROR] Cleaning inactive users failed: {e}")

@clear_inactive_users.before_loop
async def before_clear_inactive_users():
    try:
        print(Fore.YELLOW + "[INFO] Waiting for the bot to be ready to start cleaning inactive users..." + Style.RESET_ALL)
        logging.info(f"[INFO] Waiting for the bot to be ready to start cleaning inactive users...")
        await bot.wait_until_ready()
    except Exception as e:
        print(Fore.RED + f"[ERROR] An error occurred while waiting before cleaning inactive users" + Style.RESET_ALL)
        logging.error(f"[ERROR] An error occurred while waiting before cleaning inactive users: {e}")

def display_banner():
    version = "https://github.com/nythique/Discord-ChatBot.git"
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    license_message = f"""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║   This software is developed by Nexium Portal on 01/05/2020.     ║
    ║   All rights reserved.                                           ║
    ║                                                                  ║
    ║   Version: {version}                                             ║
    ║   Bot started on: {current_date}                                 ║
    ║                                                                  ║
    ║   Unauthorized copying, distribution, or modification of this    ║
    ║   software is strictly prohibited. Use is subject to the terms   ║
    ║   of the license agreement.                                      ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """
    print(Fore.YELLOW + license_message + Style.RESET_ALL)

def register_commands(bot_instance):
    global bot
    bot = bot_instance
    """Display the startup banner"""
    display_banner()
    """Connect to APIs"""
    logging.info("[INFO] Connecting to APIs...")
    @bot.event
    async def on_ready():
        try:
            print(Fore.YELLOW + "[INFO] Starting periodic tasks..." + Style.RESET_ALL)
            logging.info("[INFO] Starting periodic tasks...")
            if not save_memory_periodically.is_running():
                save_memory_periodically.start()
            if not clear_inactive_users.is_running():
                clear_inactive_users.start()
            if not status_swap.is_running():
                status_swap.start(bot)
        except Exception as e:
            print(Fore.RED + f"[ERROR] An error occurred while starting periodic tasks" + Style.RESET_ALL)
            logging.error(f"[ERROR] An error occurred while starting periodic tasks: {e}")
        
        try:
            logging.info("[INFO] Starting command sync task...")
            print(Fore.YELLOW + "[INFO] Starting command sync task..." + Style.RESET_ALL)
            client = bot.user
            synced = await bot.tree.sync()
            print(Fore.GREEN + f"[INFO] {len(synced)} commands synced successfully!" + Style.RESET_ALL)
            logging.info(f"[INFO] {len(synced)} commands synced successfully!")
            print(Fore.GREEN + f"[INFO] {len(bot.guilds)} servers connected!" + Style.RESET_ALL)
            logging.info(f"[INFO] {len(bot.guilds)} servers connected!")
            print(Fore.GREEN + f"[INFO] The bot is connected as {client.name} (ID: {client.id})!" + Style.RESET_ALL)
            logging.info(f"[INFO] The bot is connected as {client.name} (ID: {client.id})!")
            slowType(Fore.LIGHTGREEN_EX + f"[START] The bot is ready and online!\n" + Style.RESET_ALL)
            logging.info(f"[START] The bot is ready and online!")
        except Exception as e:
            print(Fore.RED + f"[ERROR] An error occurred while syncing commands" + Style.RESET_ALL)
            logging.error(f"[ERROR] An error occurred while syncing commands: {e}")

    @bot.event
    async def on_message(message):
        if message.author.bot:
            return
        
        blacklist_user, blacklist_server, *_ = await config_loading()
        if message.author.id in blacklist_user:
            return
        if hasattr(message.guild, "id") and message.guild and message.guild.id in blacklist_server:
            return

        content = message.content.strip()
        user_id = message.author.id
        username = message.author.name

        """Fonction interne pour traiter une interaction (DM ou serveur)"""
        async def process_interaction(channel, reply_func):
            try:
                logging.info(f"[INFO] Interaction from {username} in progress...")
                print(Fore.YELLOW + f"[INFO] Interaction from {username} in progress..." + Style.RESET_ALL)
                if not content:
                    await reply_func("You must provide a message to interact with me.")
                    return
                user_context = user_memory.manage(user_id, content)
                """Build the system prompt with user context"""
                system_prompt = (
                    statics.PROMPT +
                    f"\nThe Discord user you are talking to is named: {username}. " +
                    "Use this name/nickname in your answers if relevant, but do not repeat it systematically. Be natural and relevant."
                )
                messages = [{"role": "system", "content": system_prompt}]
                for msg in user_context:
                    if isinstance(msg, dict) and "role" in msg and "content" in msg:
                        messages.append({"role": msg["role"], "content": msg["content"]})
                    else:
                        messages.append({"role": "user", "content": str(msg)})
                messages.append({"role": "user", "content": content})
            except Exception as e:
                await reply_func("An error occurred while processing your message. Please try again later.")
                print(Fore.RED + f"[ERROR] Error while processing message: {e}" + Style.RESET_ALL)
                logging.error(f"[ERROR] Error while processing message: {e}")
                return
            try:
                async with channel.typing():
                    await asyncio.sleep(statics.TYPING_TIME)
                    response = ia.get_answer(messages, username=username)
                    await reply_func(response)
            except Exception as e:
                await reply_func("An error occurred while processing your message. Please try again later.")
                print(Fore.RED + f"[ERROR] Error while sending response: {e}" + Style.RESET_ALL)
                logging.error(f"[ERROR] Error while sending response: {e}")
                return

        """DM : interaction directe"""
        if isinstance(message.channel, discord.DMChannel):
            try:
                await process_interaction(message.channel, message.channel.send)
                return
            except Exception as e:
                await message.channel.send("An error occurred while processing your message. Please try again later.")
                print(Fore.RED + f"[ERROR] Error in DM: {e}" + Style.RESET_ALL)
                logging.error(f"[ERROR] Error in DM: {e}")

        """Server : interaction with mention or keyword"""
        keyWord = statics.NAME
        if (
            bot.user.mention in message.content
            or any(keyword in message.content for keyword in keyWord)
            or (message.reference and message.reference.resolved and message.reference.resolved.author == bot.user)
        ):
            try:
                await process_interaction(message.channel, message.reply)
                return
            except Exception as e:
                await message.reply("An error occurred while processing your message. Please try again later.")
                print(Fore.RED + f"[ERROR] Error in server interaction: {e}" + Style.RESET_ALL)
                logging.error(f"[ERROR] Error in server interaction: {e}")

        await bot.process_commands(message)
    
    @bot.event
    async def on_command_error(ctx, error):
        """Error management for commands"""
        if isinstance(error, commands.CommandNotFound):
            return

    @bot.tree.command(name="empty", description="Clear the bot log files (dev team only).")
    async def empty(interaction: discord.Interaction):
        blacklist_user, blacklist_server, admin_user, alert_room, root_user = await config_loading()
        if not interaction.user.id not in admin_user:
            await interaction.response.send_message("Access denied. You do not have permission to use this command.", ephemeral=True)
            print(Fore.BLUE + f"[SECURITY] Unauthorized user attempted to clear logs: {interaction.user.name}" + Style.RESET_ALL)
            logging.warning(f"[SECURITY] Unauthorized user attempted to clear logs: {interaction.user.name}")
            return
        files_to_clear = {
            "Log File (Sécurité)": statics.SECURITY_LOG_PATH,
            "Log File (Erreur)": statics.ERROR_LOG_PATH,
        }
        errors = []
        for file_name, file_path in files_to_clear.items():
            try:
                if not os.path.exists(file_path):
                    errors.append(f"{file_name} n'existe pas.")
                    continue
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write("")
                print(Fore.GREEN + f"[INFO] {file_name} was cleared." + Style.RESET_ALL)
                logging.info(f"[INFO] {file_name} was cleared. as requested by {interaction.user.name}")
            except Exception as e:
                errors.append(f"Error clearing {file_name}: {e}")
                logging.error(f"[ERROR] Error clearing {file_name}: {e}")
                print(Fore.RED + f"[ERROR] Error clearing {file_name}: {e}" + Style.RESET_ALL)
        if errors:
            error_message = "\n".join(errors)
            await interaction.response.send_message(f"Some errors occurred while clearing logs:\n{error_message}", ephemeral=True)
            logging.error(f"[ERROR] Some errors occurred while clearing logs: {error_message}")
            print(Fore.RED + f"[ERROR] Some errors occurred while clearing logs: {error_message}" + Style.RESET_ALL)
        else:
            try:
                await interaction.response.send_message("All log files have been cleared successfully.", ephemeral=True)
                print(Fore.GREEN + f"[INFO] All log files have been cleared successfully for {interaction.user.name}" + Style.RESET_ALL)
            except Exception as e:
                logging.error(f"[ERROR] Error sending confirmation message to {interaction.user.name}: {e}")
                print(Fore.RED + f"[ERROR] Error sending confirmation message to {interaction.user.name}: {e}" + Style.RESET_ALL)
        
    @bot.command(name="errors")
    async def errors(ctx, lines: int = 10):
        """Display the last lines of the error log file (dev team only)."""
        await ctx.message.delete() 
        await ctx.defer()
        """Verify if the user is authorized to access the error logs"""
        blacklist_user, blacklist_server, admin_user, alert_room, root_user = await config_loading()
        if not ctx.author.id not in admin_user:
            print(Fore.BLUE + f"[SECURITY] User not authorized attempted to access errors: {ctx.author.name}" + Style.RESET_ALL)
            logging.warning(f"[SECURITY] User not authorized attempted to access errors: {ctx.author.name}")
        log_path = statics.ERROR_LOG_PATH
        if not os.path.exists(log_path):
            await ctx.send("The error log file does not exist.")
            return
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                lines_content = f.readlines()[-lines:]
            if not lines_content:
                await ctx.send("```No error logs found.```")
                return
            msg = "```" + "".join(lines_content)[-1900:] + "```"
            await ctx.send(msg)
            print(Fore.GREEN + f"[INFO] Error logs sent to {ctx.author.name}" + Style.RESET_ALL)
            logging.info(f"[INFO] Error logs sent to {ctx.author.name}")
        except Exception as e:
            await ctx.send(f"```An error occurred while reading the logs: {e}```")
            print(Fore.RED + f"[ERROR] Error while reading logs: {e}" + Style.RESET_ALL)
            logging.error(f"[ERROR] Error while reading logs: {e}")

    @bot.command(name="ping")
    async def ping(ctx):
        """Display the bot's latency."""
        try:
            await ctx.message.delete() 
            await ctx.defer()
        except Exception:
            pass  
    
        bot_latency = round(bot.latency * 1000)

        if bot_latency < 150:
            embed = discord.Embed(
                title=f"🏓 Pong !{bot_latency} ms",
                color=discord.Color.green()
            )
            embed.set_footer(text="Powered by Nythique • Nexium Portal")
            await ctx.send(embed=embed)
        elif bot_latency > 150:
            embed = discord.Embed(
                title=f"🏓 Pong !{bot_latency} ms",
                color=discord.Color.orange()
            )
            embed.set_footer(text="Powered by Nythique • Nexium Portal")
            await ctx.send(embed=embed)

    ALLOWED_KEYS = {
        "admin": list,
        "root_user": list,
        "blacklist_user": list,
        "blacklist_server": list,
        "alert_room": int
    }
    
    @bot.command(name="config")
    async def config(ctx, action: str = None, key: str = None, *, value: str = None):
        await ctx.message.delete()
        await ctx.defer()
        blacklist_user, blacklist_server, admin_user, alert_room, root_user = await config_loading()
        if ctx.author.id not in root_user:
            logging.warning(f"[SECURITY] Unauthorized user attempted to access the config panel: {ctx.author.name}")
            print(Fore.BLUE + f"[SECURITY] Unauthorized user attempted to access the config panel: {ctx.author.name}" + Style.RESET_ALL)
            return
    
        config_path = statics.CONTROLLER_PATH
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                settings = json.load(f)
        except Exception as e:
            await ctx.send(f"Error while reading the configuration file: {e}")
            return
    
        color = discord.Color.blue()
        result = None
    
        if action == "add" and key and value is not None:
            if key not in ALLOWED_KEYS or ALLOWED_KEYS[key] != list:
                await ctx.send(f"Key **{key}** is not allowed or is not a list.")
                return
            try:
                val = json.loads(value)
            except Exception:
                val = value
            if not isinstance(val, int):
                await ctx.send(f"The elements of the list **{key}** must be integers.")
                return
            if val not in settings[key]:
                settings[key].append(val)
                result = f"Add to **{key}** : `{val}`"
                color = discord.Color.green()
            else:
                result = f"`{val}` is already in **{key}**."
                color = discord.Color.orange()
            try:
                with open(config_path, "w", encoding="utf-8") as f:
                    json.dump(settings, f, indent=4, ensure_ascii=False)
            except Exception as e:
                result = f"Error while writing: {e}"
                color = discord.Color.red()
            await ctx.send(result)
            return
    
        elif action == "rm" and key and value is not None:
            if key not in ALLOWED_KEYS or ALLOWED_KEYS[key] != list:
                await ctx.send(f"Key **{key}** is not allowed or is not a list.")
                return
            try:
                val = json.loads(value)
            except Exception:
                val = value
            if not isinstance(val, int):
                await ctx.send(f"The elements of the list **{key}** must be integers.")
                return
            if val in settings[key]:
                settings[key].remove(val)
                result = f"Remove of **{key}** : `{val}`"
                color = discord.Color.green()
            else:
                result = f"`{val}` is not in **{key}**."
                color = discord.Color.orange()
            try:
                with open(config_path, "w", encoding="utf-8") as f:
                    json.dump(settings, f, indent=4, ensure_ascii=False)
            except Exception as e:
                result = f"Error while writing: {e}"
                color = discord.Color.red()
            await ctx.send(result)
            return
    
        elif action == "set" and key and value is not None:
            if key not in ALLOWED_KEYS:
                await ctx.send(f"Key **{key}** is not allowed.")
                return
            try:
                parsed_value = json.loads(value)
            except Exception:
                parsed_value = value
            expected_type = ALLOWED_KEYS[key]
            if expected_type == list:
                if not isinstance(parsed_value, list):
                    await ctx.send(f"The value for **{key}** must be a list.")
                    return
                if not all(isinstance(i, int) for i in parsed_value):
                    await ctx.send(f"The elements of the list **{key}** must be integers.")
                    return
            elif expected_type == int:
                if not isinstance(parsed_value, int):
                    await ctx.send(f"The value for **{key}** must be an integer.")
                    return
            settings[key] = parsed_value
            try:
                with open(config_path, "w", encoding="utf-8") as f:
                    json.dump(settings, f, indent=4, ensure_ascii=False)
                result = f"Key updated: **{key}** set to `{parsed_value}`"
                color = discord.Color.green()
            except Exception as e:
                color = discord.Color.red()
                result = f"Error while writing: {e}"
            await ctx.send(result)
            return
    
        embed = discord.Embed(
            title="🛠️ Configuration panel",
            description="This panel allows you to manage the bot's configuration.",
            color=color
        )
        for k, v in settings.items():
            if isinstance(v, list):
                value_str = ", ".join(str(i) for i in v) if v else "None"
            else:
                value_str = str(v)
            embed.add_field(name=k, value=f"`{value_str}`", inline=False)
        embed.set_footer(text="Powered by Nythique • Nexium Portal")
    
        try:
            await ctx.author.send(embed=embed)
            await ctx.send("Configuration details have been sent to your DMs.", delete_after=5)
        except Exception:
            await ctx.send(embed=embed)