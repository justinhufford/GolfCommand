import os
import time

def clear_screen():
    # Clear the screen based on the operating system
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    clear_screen()
    print("""
▄▀▀▀     █ █▀ █▀▀█                           █
█ ▀█ █▀█ █ █▀ █    █▀█ █▀█▀▄ █▀█▀▄ ▄▀█ █▀▄ ▄▀█
▀▀▀▀ ▀▀▀ ▀ █  ▀▀▀▀ ▀▀▀ ▀ ▀ ▀ ▀ ▀ ▀ ▀▀▀ ▀ ▀ ▀▀▀
           █  ᴅᴇsɪɢɴᴇᴅ ʙʏ ȷᴜsᴛɪɴ ʜᴜғғᴏʀᴅ                                                 
    """)
    print("[1] New Game")
    print("[2] Settings")
    print("[0] Quit")
    
    choice = input("Enter your choice: ")
    handle_menu_choice(choice)

def handle_menu_choice(choice):
    if choice == "1":
        clear_screen()
        print("Loading Game (todo: build game...)")
    elif choice == "2":
        clear_screen()
        print("Settings (todo: develop settings)")
    elif choice == "0":
        clear_screen()
        print("Goodbye!")
        time.sleep(2)
        clear_screen()
        exit()
    else:
        print("I'm sorry, Dave. I'm afraid I can't do that.")
        time.sleep(2)
        main_menu()

if __name__ == "__main__":
    main_menu()