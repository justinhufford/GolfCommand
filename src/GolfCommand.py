file = "src.GolfCommand"
README = """
┎┒  ┒┎┎┒             ┒
┃┰┎┒┃╂┃ ┎┒┰┰┒┰┰┒┎┒┰┒┎┨
┖┨┖┚┸┃┖┚┖┚┖┖┖┖┖┖┖┸┖┖┖┸
┖┚   ┚                
© 2026 Justin Hufford
"""

import display
import logo
import font
import time

# ------------------------------------------------------------------------------

def start():
    display.draw_centered("Howdy!")
    time.sleep(1)

    display.clear()
    time.sleep(0.5)

    display.draw_centered("We're just getting set up...")
    time.sleep(2)

    display.clear()
    time.sleep(1)



    logotype_large = logo.square_tall
    display.draw_centered(logotype_large)
    time.sleep(2)

    display.clear()
    time.sleep(0.5)


    logotype = font.draw("GolfCommand")
    display.draw_centered(logotype)
    input()

    display.clear()
    time.sleep(1)

if __name__ == "__main__":
    while True:
        start()

# ------------------------------------------------------------------------------


kilroy_was_here = """
  ╭─╮  
╶ɷ┴Ü┴ɷ╴
"""
