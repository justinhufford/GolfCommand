import os
import platform

def clear():
    """
    Clear the terminal/console screen.
    Works on Windows, macOS, and Linux.
    """
    # Check the operating system
    if platform.system() == "Windows":
        os.system("cls")
    else:
        # For macOS and Linux
        os.system("clear")
