"""
Chatbot module to handle conversation with GPT, manage logging, and execute commands.
"""
import asyncio
import logging
import json
from datetime import datetime
import os
from openai import AsyncOpenAI
from config import API_KEY, MODEL, SYSTEM_MESSAGE, TYPING_SPEED, AI_TITLE, USER_TITLE, COLOR_USER, COLOR_AI, COLOR_SYSTEM, COLOR_ERROR, COLOR_RESET
from config import print_message
from commands import execute_command, QuitCommandException
from colorama import Style  # Ensure this import is present

# Configure logging
logging.basicConfig(level=logging.CRITICAL)

# Initialize OpenAI client
client = AsyncOpenAI(api_key=API_KEY)


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


async def stream_gpt_response(client, conversation, model=MODEL):
    try:
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
                await asyncio.sleep(TYPING_SPEED)

        print(Style.RESET_ALL)
        return response_content.strip()
    except Exception as e:
        logging.error(f"Error in AI response: {e}")
        print_message("error", str(e))
        return str(e)


async def run_chatbot():
    filename = generate_filename()
    conversation = [{"role": "system", "content": SYSTEM_MESSAGE}]
    add_message_to_conversation(
        conversation, "system", SYSTEM_MESSAGE, filename)
    print_message("system", SYSTEM_MESSAGE)

    # AI starts the conversation
    try:
        gpt_response = await stream_gpt_response(client, conversation, model="gpt-4o")
        add_message_to_conversation(
            conversation, "assistant", gpt_response, filename)

        while True:
            command_start = gpt_response.find("COMMAND:")
            if command_start != -1:
                command_str = gpt_response[command_start:].strip()
                command_result = execute_command(command_str)
                for result in command_result:
                    if result == "PASS":
                        gpt_response = ""  # Clear gpt_response to exit the inner loop and wait for user input
                        break
                    print_message("system", f"\nCommand result: {result}\n")
                    add_message_to_conversation(
                        conversation, "system", f"Command result: {result}", filename)
                if result == "PASS":
                    break
                gpt_response = gpt_response[:command_start].strip()
            else:
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
            add_message_to_conversation(
                conversation, "user", user_input, filename)

            while True:
                try:
                    gpt_response = await stream_gpt_response(client, conversation, model="gpt-4o")
                    add_message_to_conversation(
                        conversation, "assistant", gpt_response, filename)

                    while True:
                        command_start = gpt_response.find("COMMAND:")
                        if command_start != -1:
                            command_str = gpt_response[command_start:].strip()
                            command_result = execute_command(command_str)
                            for result in command_result:
                                if result == "PASS":
                                    gpt_response = ""  # Clear gpt_response to exit the inner loop and wait for user input
                                    break
                                print_message(
                                    "system", f"\nCommand result: {result}\n")
                                add_message_to_conversation(
                                    conversation, "system", f"Command result: {result}", filename)
                            if result == "PASS":
                                break
                            gpt_response = gpt_response[:command_start].strip()
                        else:
                            break

                    if result == "PASS":
                        break

                except QuitCommandException:
                    print_message("system", "Exiting the program.")
                    return
        except Exception as e:
            logging.error(f"Error in run_chatbot: {e}")
            print_message("error", str(e))
