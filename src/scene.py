from dataclasses import dataclass
from typing import List, Tuple, Callable, Union
import display

@dataclass
class Scene:
    title: str
    content: list
    options: list

def main_menu():
    return Scene(
        title="Main Menu",

        content=[
            display.logotype,
            "Welcome to GolfCommand!"
        ],
        options=[
            ("1", "Play", play_menu),
            ("2", "Settings", settings_menu),
            ("0", "Exit", exit)
        ]
    )


def play_menu():
    return Scene(
        title="Play",

        content=[
            "TODO: Play menu",
        ],
        options=[
            ("1", "New Game", TODO),
            ("2", "Load Game", TODO),
            ("0", "Main Menu", main_menu)
        ]
    )

def settings_menu():
    return Scene(
        title="Settings",
        content=[
            "TODO: Settings menu",
        ],
        options=[
            ("1", "General", TODO),
            ("0", "Main Menu", main_menu)
        ]
    )

def TODO():
    return Scene(
        title="TODO",
        content=[
            "⚠︎ Under construction",
        ],
        options=[
            ("0", "Main Menu", main_menu)
        ]
    )