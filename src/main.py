"""
┏┓  ╻┏┏┓             ╻
┃┓┏┓┃╋┃ ┏┓┏┳┓┏┳┓┏┓┏┓┏┫
┗┫┗┛╹┃┗┛┗┛╹╹╹╹╹╹┗┻╹╹┗┛
┗┛   ╹                
"""

import display
import scene

def main():
    current_scene = scene.main_menu()

    while current_scene:
        current_scene = display.scene(current_scene)

if __name__ == "__main__":
    main()