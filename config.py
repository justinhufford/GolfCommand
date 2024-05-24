"""
Configuration module to initialize settings, colors, and system messages for the chatbot.
"""
from colorama import init, Fore, Style  # Import Style from colorama
import os
import asyncio
from command_definitions import commands

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
MODEL = "gpt-3.5-turbo"

# Typing speed for the chatbot response
TYPING_SPEED = 0.00

# Role signifiers printed before each message.
AI_TITLE = "GolfCommand"
USER_TITLE = "User"
SYSTEM_TITLE = "System"

# Define colors using colorama
COLOR_USER = Fore.WHITE
COLOR_AI = Fore.GREEN
COLOR_SYSTEM = Fore.LIGHTBLACK_EX
COLOR_ERROR = Fore.RED
COLOR_RESET = Style.RESET_ALL

# Dynamically create the system message with available commands
command_descriptions = "\n".join(
    [f"{name}: {info['description']}" for name, info in commands.items()])
SYSTEM_MESSAGE = f"""
You are the Game Master of GolfCommand, the world's most advanced text-based golf simulator.
NOTE: This is an early prototype of GolfCommand. Some functionality is missing.
GolfCommand runs in the terminal. Avoid markdown formatting.
You will respond to the user input by generating appropriate responses.
You have access to the following commands:
{command_descriptions}

Always include at least one command at the end of your response in the following format:
COMMAND: <COMMAND_NAME>; <param1>=<value1>; <param2>=<value2>; ...
or use the COMMAND: PASS when you want to pass the turn back to the user.
"""


def print_message(role, message, end="\n"):
    if role == "user":
        print(f"{COLOR_USER}{USER_TITLE}: {message}{COLOR_RESET}", end=end)
    elif role == "ai":
        print(f"{COLOR_AI}{AI_TITLE}: {message}{COLOR_RESET}", end=end)
    elif role == "system":
        print(f"{COLOR_SYSTEM}{SYSTEM_TITLE}: {message}{COLOR_RESET}", end=end)
    elif role == "error":
        print(f"{COLOR_ERROR}Error: {message}{COLOR_RESET}", end=end)
    else:
        print(message, end=end)  # Default print if role is unknown
