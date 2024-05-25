"""
Configuration module to initialize settings, colors, and system messages for the chatbot.
"""
from colorama import init, Fore, Style  # Import Style from colorama
import os
import json
from command_definitions import commands
import logging

# Initialize colorama
init(autoreset=True)

# Load API key from environment variable or .txt file
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    try:
        with open("OPENAI_API_KEY.txt", "r") as file:
            API_KEY = file.read().strip()
    except FileNotFoundError:
        raise Exception(
            "API key not found. Please set the OPENAI_API_KEY environment variable or provide an OPENAI_API_KEY.txt file.")

# Default model to use
DEFAULT_MODEL = "gpt-4o"

# Configuration file path
CONFIG_FILE_PATH = "config.json"

# Role signifiers printed before each message.
AI_TITLE = "GolfCommand"
USER_TITLE = "User"
SYSTEM_TITLE = "System"

# Define colors using colorama
COLOR_USER = Fore.WHITE
COLOR_AI = Fore.GREEN
COLOR_SYSTEM = Fore.LIGHTBLACK_EX
COLOR_ERROR = Fore.RED
COLOR_LOG = Fore.BLUE  # Add blue color for logs
COLOR_RESET = Style.RESET_ALL

# Define a custom formatter for colored logging
class ColoredFormatter(logging.Formatter):
    def format(self, record):
        log_fmt = f"{COLOR_LOG}{record.msg}{COLOR_RESET}"
        return log_fmt

# Configuration class to manage dynamic settings
class Config:
    def __init__(self):
        self.typing_speed = 0.01
        self.model = DEFAULT_MODEL
        self.logging_enabled = False  # New attribute for logging state
        self.load()

    def set_typing_speed(self, speed):
        self.typing_speed = speed
        self.save()

    def set_model(self, model):
        self.model = model
        self.save()

    def enable_logging(self):
        self.logging_enabled = True
        self.save()
        self.configure_logging()

    def disable_logging(self):
        self.logging_enabled = False
        self.save()
        self.configure_logging()

    def configure_logging(self):
        logger = logging.getLogger()
        logger.handlers.clear()
        if self.logging_enabled:
            handler = logging.StreamHandler()
            handler.setFormatter(ColoredFormatter())
            logger.addHandler(handler)
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.NOTSET)
            logger.addHandler(logging.NullHandler())  # Ensure no messages are logged

    def save(self):
        with open(CONFIG_FILE_PATH, 'w') as f:
            json.dump(self.__dict__, f, indent=2)

    def load(self):
        if os.path.exists(CONFIG_FILE_PATH):
            with open(CONFIG_FILE_PATH, 'r') as f:
                self.__dict__.update(json.load(f))
        self.configure_logging()  # Ensure logging is configured based on saved state

config = Config()

# Dynamically create the system message with available commands
command_descriptions = "\n".join(
    [f"{name}: {info['description']}" for name, info in commands.items()])

SYSTEM_MESSAGE = f"""
You are the Game Master of GolfCommand, the world's most advanced text-based golf simulator.
NOTE: This is an early prototype of GolfCommand. Some functionality is missing.
GolfCommand is whimsical open-ended game. Go along with the player's requests, but stay in control.
Let the player be creative, but don't break continuity just because the player wants to. The player's actions have consequences.
Remember, it's just a game. The player knows this. The player's actions may result in cartoon injury, but the actual user is safe.

Game runs in the terminal. Avoid markdown formatting.
Shortest responses are best, user pays per token.
You will respond to the user input by generating appropriate responses.
You have access to the following commands:
{command_descriptions}

Always include at least one command at the end of your response in the following format:
~<COMMAND_NAME>, <param1>=<value1>, <param2>=<value2>, ~
or use the ~PASS~ when you want to pass the turn back to the user.
Calling RANDOM_NUMBER roll D20 to determine outcome of actions that don't have a designated command.
Nat20 is an overwhelmingly epic success far beyond expectations or possibility. Nat1 is extreme over-exaggerated catastrophe. Be as unexpectedly over-the-top as possible for both extremes!)
"""

def print_message(role, message, end="\n"):  # Set default end to "\n"
    if role == "user":
        print(f"{COLOR_USER}{USER_TITLE}: {message}{COLOR_RESET}", end=end)
    elif role == "ai":
        print(f"{COLOR_AI}{AI_TITLE}: {message}{COLOR_RESET}", end=end)
    elif role == "system":
        print(f"{COLOR_SYSTEM}{SYSTEM_TITLE}: {message}{COLOR_RESET}", end=end)
    elif role == "error":
        print(f"{COLOR_ERROR}Error: {message}{COLOR_RESET}", end=end)
    elif role == "log":  # Add log role to handle log messages
        print(f"{COLOR_LOG}Log: {message}{COLOR_RESET}", end=end)
    else:
        print(message, end=end)  # Default print if role is unknown
    print()
