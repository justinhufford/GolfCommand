"""
  ▄▄      ▄     ▄▄                            █
 █  ▀     █ ▄▀ █  █                           █
 █ ▀█ █▀▄ █ █▀ █    █▀▄ █▀█▀▄ █▀█▀▄ ▄▀█ █▀▄ ▄▀█
 ▀▄▄█ ▀▀▀ ▀ █  ▀▄▄▀ ▀▀▀ ▀ ▀ ▀ ▀ ▀ ▀ ▀▀▀ ▀ ▀ ▀▀▀ 
 ▄  █       █                            (beta)
  ▀▀                                           
 The world's most advanced text-based golf simulator!
 
"""
import asyncio
from chatbot import run_chatbot


def main():
    print("Welcome to GolfCommand!")
    asyncio.run(run_chatbot())


if __name__ == "__main__":
    main()
