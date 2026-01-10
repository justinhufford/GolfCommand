README = """src.display
User experience and interface design.
"""
# ------------------------------------------------------------------------------

import os
import time
import display
import shutil
import cursor

# ------------------------------------------------------------------------------

WIDTH = 36

def clear():
    os.system('cls')

cursor = cursor.cursor
gutter = len(cursor) + 1

def _body(content):
    cols, rows = shutil.get_terminal_size()
    margin = ( cols - len(content) // 2 )
    for line in content.split("\n"):
        print(" " * margin, end = "")
        print(line)




def draw(content):
    lines = content.split("\n")
    for line in lines:
        print( (" " * gutter) + line )

def draw_centered(content):
    cols, rows = shutil.get_terminal_size()
    lines = content.split("\n")
    v_margin = (rows - len(lines)) // 2 # Terminal height - content height / 2 (rounded)

    print("\n" * v_margin,  end = "")

    for line in lines:
        h_margin = (cols - len(line)) // 2
        print(" " * h_margin, end = "")
        print(line)

    print("\n" * v_margin,  end = "")





# ------------------------------------------------------------------------------

def start():
    turn = 0
    
    while True:
        turn += 1
        display.clear()

        draw(f"TURN: {turn}")

        if turn == 1:
            draw_centered(README)
            input("> ")
            continue
        

        input(cursor)

if __name__ == "__main__":
    start()
    input("END")