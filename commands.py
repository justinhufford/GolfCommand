# commands.py

import random
import os
from command_definitions import commands, developer_commands
from player import Player
from config import config  # Import the configuration object

class QuitCommandException(Exception):
    """Custom exception to handle quit command."""
    pass

# Instantiate the player
player = Player()
dev_mode_active = False

def execute_command(command_str):
    global dev_mode_active
    try:
        command_str = command_str.strip('~')
        commands_list = command_str.split('~')
        results = []
        pass_command_detected = False

        for command in commands_list:
            parts = command.split(',')
            command_name = parts[0].strip()

            if command_name == "PASS":
                pass_command_detected = True
                continue  # Ignore the PASS command if there are other commands

            params = {}
            for part in parts[1:]:
                key, value = part.split('=')
                params[key.strip()] = value.strip()

            for key in params:
                if key in ('min', 'max', 'amount', 'speed'):
                    params[key] = float(params[key]) if key == 'speed' else int(params[key])

            if command_name in commands:
                func_name = commands[command_name]['func']
                if func_name in globals():
                    command_func = globals()[func_name]
                    result = command_func(**params)
                    results.append(result)
                else:
                    results.append(f"Function {func_name} not found.")
            elif dev_mode_active and command_name in developer_commands:
                func_name = developer_commands[command_name]['func']
                if func_name in globals():
                    command_func = globals()[func_name]
                    result = command_func(**params)
                    results.append(result)
                else:
                    results.append(f"Function {func_name} not found.")
            else:
                results.append(f"Unknown command: {command_name}")

        if pass_command_detected and not results:
            results.append("PASS")

        pass_command_detected = False  # Explicitly reset flag
        return results
    except QuitCommandException:
        raise
    except Exception as e:
        return [f"Error executing command: {e}"]

"""
COMMAND FUNCTIONS
"""

def random_number(min=1, max=100):
    """
    Generates a random number between min and max.
    """
    return random.randint(min, max)

def quit():
    """
    Exits the program.
    """
    raise QuitCommandException("Exiting the program.")

def list_source_files():
    """
    List all source files with their descriptions (docstrings).
    """
    source_files = [f for f in os.listdir('.') if f.endswith('.py')]
    descriptions = []

    for file in source_files:
        with open(file, 'r') as f:
            first_line = f.readline().strip()
            if first_line.startswith('"""') or first_line.startswith("'''"):
                docstring = first_line.strip('"""').strip("'''")
            else:
                docstring = "No description available."
            descriptions.append(f"{file}: {docstring}")

    return "\n".join(descriptions)

def read_source_file(filename):
    """
    Read the contents of a source file.
    """
    if not os.path.exists(filename):
        return f"Error: File {filename} does not exist."

    with open(filename, 'r') as f:
        return f.read()

def get_health():
    """
    Returns the player's current health.
    """
    return f"Player's current health: {player.get_health()}"

def set_health(amount):
    """
    Sets the player's health to a specific amount.
    """
    player.set_health(amount)
    return f"Player's health set to: {player.get_health()}"

def modify_health(amount):
    """
    Modifies the player's health by a specific amount. Use then whenever player is injured or healed.
    """
    new_health = player.modify_health(amount)
    return f"Player's health modified by {amount}. New health: {new_health}"

"""
DEVELOPER COMMAND FUNCTIONS
"""

def developer_settings():
    global dev_mode_active
    dev_mode_active = True
    dev_commands = "\n".join(
        [f"{name}: {info['description']}" for name, info in developer_commands.items()])
    return f"Available developer commands:\n{dev_commands}"

def change_typing_speed(speed):
    config.set_typing_speed(speed)
    return f"Typing speed changed to: {speed}"

def change_model(model):
    if model in ["gpt-3.5-turbo", "gpt-4o"]:
        config.set_model(model)
        return f"Model changed to: {model}"
    else:
        return "Invalid model. Please choose either 'gpt-3.5-turbo' or 'gpt-4o'."

def toggle_logging():
    if config.logging_enabled:
        config.disable_logging()
        return "Logging disabled."
    else:
        config.enable_logging()
        return "Logging enabled."
