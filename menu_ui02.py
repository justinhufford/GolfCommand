GolfCommand = """
  ▄▄      ▄     ▄▄                            █
 █  ▀     █ ▄▀ █  █                           █
 █ ▀█ █▀▄ █ █▀ █    █▀▄ █▀█▀▄ █▀█▀▄ ▄▀█ █▀▄ ▄▀█
 ▀▄▄█ ▀▀▀ ▀ █  ▀▄▄▀ ▀▀▀ ▀ ▀ ▀ ▀ ▀ ▀ ▀▀▀ ▀ ▀ ▀▀▀
 ▄  █       █                      Menu UI Test
  ▀▀                                           """


from blessed import Terminal
import time
term = Terminal()


def center_logo():
    # Split the ASCII art into lines
    GolfCommand_lines = GolfCommand.split('\n')

    # Calculate the width of the longest line in the ASCII art
    art_width = max(len(line) for line in GolfCommand_lines)

    # Calculate left padding for centering
    left_padding = (term.width - art_width) // 2

    # Apply left padding to each line and print
    for line in GolfCommand_lines:
        print(" " * left_padding + line)

    



def clr():
    print(term.home + term.clear)

def continue_game():
    clr()
    print("Stub for continue game functionality.")
    input() # to pause screen in terminal and prevent program from closing until after user input
    # Placeholder function for the 'CONTINUE' action
    # Replace with actual game continuation logic

def new_game():
    clr()
    print("Stub for new game functionality.")
    input() # to pause screen in terminal and prevent program from closing until after user input
    # Placeholder function for the 'NEW GAME' action
    # Replace with actual new game initialization logic

def settings():
    clr()
    print("Stub for settings functionality.")
    input() # to pause screen in terminal and prevent program from closing until after user input
    # Placeholder function for the 'SETTINGS' action
    # Replace with actual settings adjustment logic

def quit_game():
    clr()
    print("Quitting game...")


    # Animation frames
    frames = ["Good", "Bye"]
 # Find the width of the widest line in the animation
    max_frame_width = max(len(line) for frame in frames for line in frame.split('\n'))

    # Calculate the horizontal center position
    animation_col = (term.width - max_frame_width) // 2

    # Calculate the number of lines in the tallest frame
    max_frame_height = max(len(frame.split('\n')) for frame in frames)

    # Calculate the vertical center position
    animation_row = 0 #(term.height - max_frame_height) // 2

    # Loop through each frame
    for frame in frames:
        # Clear the previous frame's area
        for i in range(max_frame_height):
            print(term.move_xy(animation_col, animation_row + i) + ' ' * max_frame_width)

        # Print the new frame
        frame_lines = frame.split('\n')
        for i, line in enumerate(frame_lines):
            print(term.move_xy(animation_col, animation_row + i) + line)

        time.sleep(0.025)  # Adjust for smoother animation
    exit()

        

def main():
    menu_items = ["CONTINUE", "NEW GAME", "SETTINGS", "QUIT"]
    selected = 0
    previous_selected = None  # Variable to keep track of the previously selected item

    longest_word = max(menu_items, key=len)
    menu_padding = int(6)
    menu_width = len(longest_word) + menu_padding

    # Calculate positions for each menu item
    menu_start_line = len(GolfCommand.split('\n')) + 1
    menu_item_lines = {i: menu_start_line + i for i in range(len(menu_items))}

    def print_menu_item(index, selected, redraw=False):
        # Move cursor to the correct position if redrawing
        if redraw:
            print(term.move_xy(0, menu_item_lines[index]), end='')

        centered_item = menu_items[index].center(menu_width)
        if index == selected:
            # Print the selected item with reversed colors
            print(" " * left_padding + term.reverse(centered_item))
        else:
            # Print non-selected items normally
            print(" " * left_padding + centered_item)

    with term.cbreak(), term.hidden_cursor():
        print(term.home + term.clear)
        center_logo()
        left_padding = (term.width - menu_width) // 2

        # Initial draw of all menu items
        for i in range(len(menu_items)):
            print_menu_item(i, selected)

        while True:
            key = term.inkey()

            if key.name in ["KEY_UP", "KEY_LEFT"]:
                previous_selected = selected
                selected = (selected - 1) % len(menu_items)
            elif key.name in ["KEY_DOWN", "KEY_RIGHT"]:
                previous_selected = selected
                selected = (selected + 1) % len(menu_items)
            elif key.name == "KEY_ENTER":
                if selected == 0:
                    continue_game()
                elif selected == 1:
                    new_game()
                elif selected == 2:
                    settings()
                elif selected == 3:
                    quit_game()
                
            if previous_selected is not None:
                # Redraw only the previously selected and currently selected items
                print_menu_item(previous_selected, selected, redraw=True)
                print_menu_item(selected, selected, redraw=True)
                previous_selected = None  # Reset the previous_selected variable

                

if __name__ == "__main__":
    main()