import random
import os
from command_definitions import commands


class QuitCommandException(Exception):
    """Custom exception to handle quit command."""
    pass


def execute_command(command_str):
    """
    Parses and executes the command from the command string.
    """
    try:
        commands_list = command_str.split('\n')
        results = []
        pass_command_detected = False

        for command in commands_list:
            parts = command.split(';')
            command_name = parts[0].split(':')[1].strip()

            if command_name == "PASS":
                pass_command_detected = True
                continue  # Ignore the PASS command if there are other commands

            params = {}
            for part in parts[1:]:
                key, value = part.split('=')
                params[key.strip()] = value.strip()

            # Convert params to the appropriate types
            for key in params:
                if key in ('min', 'max'):
                    params[key] = int(params[key])

            if command_name in commands:
                func_name = commands[command_name]['func']
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
