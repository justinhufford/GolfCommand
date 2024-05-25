import asyncio
import logging
import json
from datetime import datetime
import os
from openai import AsyncOpenAI
from config import API_KEY, SYSTEM_MESSAGE, AI_TITLE, USER_TITLE, COLOR_USER, COLOR_AI, COLOR_SYSTEM, COLOR_ERROR, COLOR_RESET, config, print_message
from commands import execute_command, QuitCommandException
from colorama import Fore, Style, init  # Ensure this import is present

# Initialize colorama
init(autoreset=True)

# Initialize OpenAI client
client = AsyncOpenAI(api_key=API_KEY)

# Ensure to import the Player
from player import Player
player = Player()

def generate_filename(folder="message_history"):
    if not os.path.exists(folder):
        os.makedirs(folder)
    now = datetime.now()
    return os.path.join(folder, now.strftime("%Y-%m-%d_%H-%M-%S") + "_messages.json")

def write_mirror_conversation(conversation, filename):
    with open(filename, 'w') as f:
        json.dump(conversation, f, indent=2)

def add_message_to_conversation(conversation, role, content, filename):
    message = {"role": role, "content": content}
    conversation.append(message)
    write_mirror_conversation(conversation, filename)

async def stream_gpt_response(client, conversation, model=None):
    try:
        if model is None:
            model = config.model
        stream = await client.chat.completions.create(
            model=model,
            messages=conversation,
            stream=True,
        )

        response_content = ""  # Empty string to store the response.

        # Add role signifier to the UI.
        print(f"{COLOR_AI}{AI_TITLE}: ", end="", flush=True)

        async for chunk in stream:
            content = chunk.choices[0].delta.content or ""
            for char in content:  # Print the response character by character on the same line
                print(f"{COLOR_AI}{char}", end="", flush=True)
                response_content += char
                await asyncio.sleep(config.typing_speed)

        print(Style.RESET_ALL)
        print("\n")  # Add a line break after the AI response
        return response_content.strip()
    except Exception as e:
        logging.error(f"Error in AI response: {e}")
        print_message("error", str(e))
        return str(e)

async def prompt_for_command(client, conversation, filename):
    system_message = "Input command or PASS"
    add_message_to_conversation(conversation, "system", system_message, filename)
    print_message("system", system_message)
    gpt_response = await stream_gpt_response(client, conversation)
    add_message_to_conversation(conversation, "assistant", gpt_response, filename)
    return gpt_response

async def run_chatbot():
    filename = generate_filename()
    conversation = [{"role": "system", "content": SYSTEM_MESSAGE}]
    add_message_to_conversation(conversation, "system", SYSTEM_MESSAGE, filename)
    print_message("system", SYSTEM_MESSAGE)

    # AI starts the conversation
    try:
        gpt_response = await stream_gpt_response(client, conversation)
        add_message_to_conversation(conversation, "assistant", gpt_response, filename)

        while True:
            command_included = "~" in gpt_response
            if command_included:
                while True:
                    command_start = gpt_response.find("~")
                    if command_start != -1:
                        command_end = gpt_response.find("~", command_start + 1)
                        command_str = gpt_response[command_start:command_end + 1].strip()
                        command_result = execute_command(command_str)
                        for result in command_result:
                            if result == "PASS":
                                logging.debug("PASS command executed, breaking loop")
                                gpt_response = ""  # Clear gpt_response to exit the inner loop and wait for user input
                                break
                            print_message("system", f"\nCommand result: {result}\n")
                            add_message_to_conversation(conversation, "system", f"Command result: {result}", filename)
                        if result == "PASS":
                            break
                        gpt_response = gpt_response[:command_start].strip() + gpt_response[command_end + 1:].strip()
                    else:
                        break

            if not command_included:
                gpt_response = await prompt_for_command(client, conversation, filename)

            if result == "PASS":
                logging.debug("PASS command found, breaking outer loop")
                break

    except QuitCommandException:
        print_message("system", "Exiting the program.")
        return
    except Exception as e:
        logging.error(f"Error in initial AI response: {e}")
        print_message("error", str(e))

    # Main conversation loop
    while True:
        try:
            user_input = input(f"{COLOR_USER}{USER_TITLE}: {COLOR_RESET}")
            add_message_to_conversation(conversation, "user", user_input, filename)
            print()  # Add a line break after user input

            while True:
                try:
                    gpt_response = await stream_gpt_response(client, conversation)
                    add_message_to_conversation(conversation, "assistant", gpt_response, filename)

                    command_included = "~" in gpt_response

                    if command_included:
                        while True:
                            command_start = gpt_response.find("~")
                            if command_start != -1:
                                command_end = gpt_response.find("~", command_start + 1)
                                command_str = gpt_response[command_start:command_end + 1].strip()
                                command_result = execute_command(command_str)
                                for result in command_result:
                                    if result == "PASS":
                                        logging.debug("PASS command executed, breaking loop")
                                        gpt_response = ""  # Clear gpt_response to exit the inner loop and wait for user input
                                        break
                                    print_message("system", f"\nCommand result: {result}\n")
                                    add_message_to_conversation(conversation, "system", f"Command result: {result}", filename)
                                if result == "PASS":
                                    break
                                gpt_response = gpt_response[:command_start].strip() + gpt_response[command_end + 1:].strip()
                            else:
                                break

                    if not command_included:
                        gpt_response = await prompt_for_command(client, conversation, filename)

                    if result == "PASS":
                        logging.debug("PASS command found, breaking outer loop")
                        break

                except QuitCommandException:
                    print_message("system", "Exiting the program.")
                    return
        except Exception as e:
            logging.error(f"Error in run_chatbot: {e}")
            print_message("error", str(e))

# Initialize logging based on config
config.configure_logging()
