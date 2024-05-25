# command_definitions.py

"""
Command definitions for the chatbot, including command names, functions, and descriptions.
"""
commands = {
    'RANDOM_NUMBER': {
        'func': 'random_number',
        'description': "Generate a random number between min and max. Example: `~RANDOM_NUMBER, min=1, max=100~`."
    },
    'GET_HEALTH': {
        'func': 'get_health',
        'description': "Display the player's current health."
    },
    'SET_HEALTH': {
        'func': 'set_health',
        'description': "Set the player's health to a specific value. Example: `~SET_HEALTH, amount=50~`."
    },
    'MODIFY_HEALTH': {
        'func': 'modify_health',
        'description': "Modify the player's health by a specific amount. Example: `~MODIFY_HEALTH, amount=-10~`."
    },
    'QUIT': {
        'func': 'quit',
        'description': "Exits the program. NOTE: Only run with user permission or to force-quit the program."
    },
    'DEVELOPER_SETTINGS': {
        'func': 'developer_settings',
        'description': "Allows you to modify the game's code to change settings and parameters. Type ~DEVELOPER_SETTINGS~ for more info."
    }
}

developer_commands = {
    'CHANGE_TYPING_SPEED': {
        'func': 'change_typing_speed',
        'description': "Change the typing speed. Example: `~CHANGE_TYPING_SPEED, speed=0.05~`."
    },
    'CHANGE_MODEL': {
        'func': 'change_model',
        'description': "Change the model to either `gpt-3.5-turbo` or `gpt-4o`. Example: `~CHANGE_MODEL, model=gpt-4o~`."
    },
    'LIST_SOURCE_FILES': {
        'func': 'list_source_files',
        'description': "View a list of the python source files for GolfCommand`."
    },
    'READ_SOURCE_FILE': {
        'func': 'read_source_file',
        'description': "Output the contents of a python source file. Example: `~READ_SOURCE_FILE, file=filename~`."
    },
    'TOGGLE_LOGGING': {
        'func': 'toggle_logging',
        'description': "Toggle logging on or off. Example: `~TOGGLE_LOGGING~`."
    }
}
