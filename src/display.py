import os
import platform
import time
import logging
from scene import Scene

# Set up logging at the top of the file
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

WIDTH = 80
MARGIN = 4

SLOW = 0.2
FAST = 0.08
TYPE = 0.02

def clear():
    """
    Clears the terminal/console screen.
    """
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def print_body(content, typing=False):
    print((" " * MARGIN), end="")
    if typing:
        for char in content:
            print(char, end="", flush=True)
            time.sleep(TYPE)
        print()
    else:
        print(content)

def top_bar(title):
    INVERT = "\033[7m"
    RESET = "\033[27m"
    print(INVERT, end="")
    print_body(title + (" " * (WIDTH - len(title))))
    print(RESET)
    
def typing(content):
    for char in content:
        print(char, end="", flush=True)
        time.sleep(TYPE)
    print()

def logotype():
    # Get the folder where this file (display.py) is located
    current_folder = os.path.dirname(__file__)
    logo_path = os.path.join(current_folder, 'logo.txt')
    
    with open(logo_path, 'r', encoding='utf-8') as logo:
        logotype = logo.read()
        for line in logotype.split("\n"):
            print_body(line)
    print()

def input_field():
    command = input((" " * MARGIN) + "> ")
    return command

def scene(scene: Scene):
    clear()

    # Print the top bar
    top_bar(scene.title)
    time.sleep(SLOW)

    # Output the content
    for item in scene.content:
        if callable(item):
            item()
            time.sleep(SLOW)
        else:
            print_body(item, typing=True)       
    print()
    time.sleep(SLOW)

    # Display the options
    for key, name, func in scene.options:
        print_body(f"[{key}] {name}")
        time.sleep(FAST)
    print()
    time.sleep(SLOW)

    # Collect user input
    command = input_field()
    print(f"Debug - command is: '{command}'")  # The quotes will help you see any extra characters

    # Find the matching option
    for key, name, func in scene.options:
        if command == key:
            # Call the function and load the next scene
            return func()
    
    # If we get here, the input wasn't valid.  
    print_body("Invalid option", typing=True)
    time.sleep(SLOW)