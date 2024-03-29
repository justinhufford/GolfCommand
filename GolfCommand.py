GolfCommand = """
  ▄▄      ▄     ▄▄                            █
 █  ▀     █ ▄▀ █  █                           █
 █ ▀█ █▀▄ █ █▀ █    █▀▄ █▀█▀▄ █▀█▀▄ ▄▀█ █▀▄ ▄▀█
 ▀▄▄█ ▀▀▀ ▀ █  ▀▄▄▀ ▀▀▀ ▀ ▀ ▀ ▀ ▀ ▀ ▀▀▀ ▀ ▀ ▀▀▀
 ▄  █       █        
  ▀▀                                           """
# The world's most advanced text-based golf simulator!



#𝗜𝗠𝗣𝗢𝗥𝗧𝗦
import sys# for system-specific parameters and functions,
from rich.console import Console# for UI layout
from blessed import Terminal# To get access to terminal functionality,
import time# for sleep functionality,
import math# for mathing,
import random# to mix things up
import textwrap# for better text rendering,
from openai import OpenAI# for AI magic
import os

#𝗖𝗢𝗡𝗦𝗧𝗔𝗡𝗧𝗦
term = Terminal()
client = OpenAI()
console = Console()
content_width = 48# Set the width for the content
typing_speed = 0.01# Set the speed of the typing effect, 0 = intant

#Coloring
# Assume default player strength, accuracy, and swing power:
strength = 0.8
accuracy = 0.8
swing_power = 1.0 

generate_hole_distance = random.randint(300, 550)# Randomly assign a starting distance to the hole
win_tolerance = 10  # will win if ball is within 10 yards of hole
condition_threshold = 0.2 # ball and club will break if condition falls below this number

#UI symbols to visually identify message roles
ai = (" ")# Game narration
us = (" ")# User input
er = (" ")# Error message



#This is the prompt sent to ChatGPT that allows it to return numeric values for the calculate_swing_distance formula:
#Later versions of the game may use a fine-tuned 3.5 model instead to reduce API costs.
build_object = """
Potential:
The potential is a number between 0 and 100 that we can use in an equation to calculate the distance a ball hit with any object will travel.  Consider the material of the object, and how likely it is to transfer its energy and momentum to the ball when hit, or how likely energy will transfer from the club to the object. Objects with a high Coefficient of restitution, (or lower impact absorption) will have a high potential. 

Mass:
The standard mass of the object in pounds, to the first decimal point. Estimating is okay.

Condition:
A number from 0-1 describing the condition of the object. Most objects will start out with a condition close to or equal to 1, signifying a new object. Objects specified as old or beat up or otherwise in poor condition will have low condition values. Use your best judgment, and if uncertain, use a high value.

Decay:
A number from 0 to 100 describing how fragile the object is. This number will modify the condition variable whenever the object is hit, or whenever the object hits another object. Objects that would break instantly (thin glass, exploding golfball, etc.) on impact will have a decay of 100 or higher to ensure their condition value drops to 0 quickly.


|Object|Smash Factor|mass|condition|decay|
|---|---|---|---|---|
|golfball|95|0.1|1|0.2|
|new golfball|95|0.1|1|0.2|
|lucky golfball|96|0.1|1|0.0|
|old golfball|84|0.1|0.6|1.3|
|exploding golfball|98|0.2|1|500|
|baseball|70|0.5|0.8|2.4|
|bowling ball|10|16|0.7|5.2|
|driver|92|1.5|0.8|0.1|
|iron|89|1.2|0.8|0.1|
|putter|50|1|0.9|1.4|
|apple|12|0.1|0.9|85|
|banana|9|0.3|0.8|93|
|pool noodle|5|0.5|0.7|74|
|broom|21|3|0.6|42|
|fishing rod|8|2|0.7|61|
|toilet plunger|15|1|0.4|39|
|bazooka|500|20|0.8|9|
|tennis racket|72|0.7|0.8|8.6|
|guitar|78|8.4|0.7|13.7|
|pool cue|40|1.2|0.6|41.8|
|baseball bat|81|2.4|0.8|12.3|
|sledgehammer|92|18|0.8|0.1|
|crowbar|83|9.8|0.7|0.1|ru
|pickup truck|400|6000|0.7|2.9|
|the moon|10000|162,000,000,000,000,000,000,000|0.5|0.1|
|the sun|1000000000|4,400,000,000,000,000,000,000,000,000|0.8|0.1|
"""



class Item:             
#   ┆                
#   ┆      
    def __init__(self, name: str, qty: float, type: str, bio: str, potential: float, mass: float, condition: float, decay: float):
        self.name = name
        self.qty = qty
        self.type = type
        self.bio = bio 
        self.potential = potential
        self.mass = mass
        self.condition = condition
        self.decay = decay
        

class Golfer:
    def __init__(self, club: Item, ball: Item, accessory: Item, strength: float, accuracy: float):
        self.club = club
        self.ball = ball
        self.accessory = accessory
        self.strength = strength
        self.accuracy = accuracy
        self.inventory = [club, ball, accessory]


default_club = Item("Driver", 
    1, 
    "Club", 
    "Great for long shots, not so good for puttin'",
    92,
    1.5,
    80,
    0.2,
)

default_ball = Item("Golf Ball", 
    10, 
    "Ball", 
    "A mystical orb with unknown powers.",
    95,
    0.1,
    100,
    0.2,
)

default_accessory = Item("Lucky Hat", 
    1, 
    "Accessory", 
    "You swear you swing better when you wear this hat...",
    5,
    0.2,
    71,
    20,
)

golfer = Golfer(default_club, default_ball, default_accessory, strength, accuracy)

def chat_with_gpt(client, messages, model="gpt-4-1106-preview", stream=False):
    """
Model:                  Input Cost:         Output Cost:         
gpt-4-1106-preview      $0.010 / 1K tokens	$0.030 / 1K tokens
gpt-3.5-turbo-1106      $0.001 / 1K tokens	$0.002 / 1K tokens

    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=stream
        )
        if stream:
            return map(map_chunks, response)
        else:
            return response.choices[0].message.content.strip()
    except Exception as e:
        return str(e)
    
def map_chunks(chunk):
    return chunk.choices[0].delta.content

def print_with_typing_effect(text, speed=typing_speed):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()  # Ensure each character is flushed immediately
        time.sleep(speed)  # Wait a bit before printing the next character
    print()  # Move to the next line after the sentence is complete

def print_stream_with_typing_effect(chunks, speed=typing_speed, prefix=""):
    sys.stdout.write(prefix)
    sys.stdout.flush()
    for chunk in chunks:
        for char in chunk:
            sys.stdout.write(char)
            sys.stdout.flush()  # Ensure each character is flushed immediately
            time.sleep(speed)  # Wait a bit before printing the next character


def input_with_typing_effect(prompt, speed=typing_speed):
# Applies the typing effect to input messages.
    print_with_typing_effect(prompt, speed=speed)
    return input(us)# Adds the user symbol at the start of the input line

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    pass

"""
GAMEPLAY
"""

def choose_club():
    while True:
        print('CHOOSE CLUB:')
        for index, item in enumerate(golfer.inventory):
            print(f'[{index + 1}] {item.name}')
        print('[0] NEW CLUB')
        choice = int(input())
        
        try:
            if choice == 0 or '':
                build_club()
                golfer.inventory.append(golfer.club)
            else:
                golfer.club = golfer.inventory[choice - 1]

            return

        except ValueError:
            print("Invalid input. Please enter a number.")
            
        except IndexError:
            print("Invalid number. Please enter a number from the list.")
        except Exception as e:
            print(f"Problem in selecting item from inventory: {e}")

def choose_ball():
    while True:
        print('CHOOSE BALL:')
        for index, item in enumerate(golfer.inventory):
            print(f'[{index + 1}] {item.name}')
        print('[0] NEW BALL')
        choice = int(input())
        
        try:
            if choice == 0 or '':
                build_ball()
                golfer.inventory.append(golfer.ball)
            else:
                golfer.ball = golfer.inventory[choice - 1]
            return

        except ValueError:
            print("Invalid input. Please enter a number.")
            
        except IndexError:
            print("Invalid number. Please enter a number from the list.")
        except Exception as e:
            print(f"Problem in selecting item from inventory: {e}")

#CLUB
def build_club():
    #1.1 The player chooses an object to use as a club:
    print()
    print_with_typing_effect(term.yellow(ai + "What would you like to use as your golf club? "))
    print()
    golfer.club.name = input(us + term.yellow("GOLF CLUB:  "))

    #1.2 ChatGPT generates the club's values for physics calculations:
    build_club = [
        {"role": "user", "content": build_object + f"Please estimate the potential, mass, condition, and decay values for this object: {golfer.club.name}. Please output your response as a comma-separated list, with no other comment, narration, or explanation. Always provide some values, even if you don't know, just make something up. What are the values of {golfer.club.name}?"},
    ]#  ˄ Send ChatGPT detailed club build instructions
    response_build_club = chat_with_gpt(client, build_club)# ChatGPT's Response
    response_values = response_build_club.split(",")# I think this separates the values generated by ChatGPT into a format the program can use?

    if len(response_values) != 4:# If ChatGPT does not return 4 values,
        print_with_typing_effect(term.red(er + f"Error building {golfer.club.name}, please try again or choose a different club."))# display an error message.
        return False

    golfer.club.potential = float(response_values[0]) / 100
    golfer.club.mass = float(response_values[1]) * 10
    golfer.club.condition = float(response_values[2])
    golfer.club.decay = float(response_values[3]) / 100

    
    #1.3 Display the club's stats:
    print_with_typing_effect(term.yellow(f" Potential: " + term.white(f"{golfer.club.potential * 100:.2f}%")))
    print_with_typing_effect(term.yellow(f" Mass:      " + term.white(f"{golfer.club.mass / 10} lbs")))
    print_with_typing_effect(term.yellow(f" Condition: " + term.white(f"{golfer.club.condition * 100:.2f}%")))
    print_with_typing_effect(term.yellow(f" Decay:     " + term.white(f"{golfer.club.decay * 100:.2f}%")))

    return True



#Build Ball
def build_ball():
    #2.1 The player chooses an object to use as the ball:
    print()
    golfer.ball.name = print_with_typing_effect(term.yellow(ai + "What would you like to use as your golf ball? "))
    print()
    golfer.ball.name = input(us + term.yellow("GOLF BALL:  "))

    #2.2 ChatGPT generates the ball's values for physics calculations:
    build_ball = [
        {"role": "user", "content": build_object + f"Please estimate the potential, mass, condition, and decay values for this object: {golfer.ball.name}. Please output your response as a comma-separated list, with no other comment, narration, or explanation. Always provide some values, even if you don't know, just make something up. What are the values of {golfer.ball.name}?"},
    ]#  ˄ Send ChatGPT detailed ball build instructions
    response_build_ball = chat_with_gpt(client, build_ball)# ChatGPT's Response
    response_values = response_build_ball.split(",")# I think this separates the values generated by ChatGPT into a format the program can use?

    if len(response_values) != 4:# If ChatGPT does not return 4 values,
        print_with_typing_effect(term.red(er + f"Error building {golfer.ball.name}, please try again or choose a different ball."))# display an error message.
        return False

    golfer.ball.potential = float(response_values[0]) / 100
    golfer.ball.mass = float(response_values[1]) * 10
    golfer.ball.condition = float(response_values[2])
    golfer.ball.decay = float(response_values[3]) / 100

    
    #2.3 Display the ball's stats:
    print_with_typing_effect(term.yellow(f" Potential: " + term.white(f"{golfer.ball.potential * 100:.2f}%")))
    print_with_typing_effect(term.yellow(f" Mass:      " + term.white(f"{golfer.ball.mass / 10} lbs")))
    print_with_typing_effect(term.yellow(f" Condition: " + term.white(f"{golfer.ball.condition * 100:.2f}%")))
    print_with_typing_effect(term.yellow(f" Decay:     " + term.white(f"{golfer.ball.decay * 100:.2f}%")))
    return True



def calculate_swing_distance(swing_power, strength, accuracy, club_potential, ball_potential, ball_condition, ball_mass, hole_distance):
    f_mass = 800 / (ball_mass + (1 / ball_mass))
    raw_distance = (swing_power * strength * club_potential * ball_potential * ball_condition) * f_mass

    # Adjust distance based on accuracy
    accuracy_factor = 1 - (1 - accuracy) * 0.5  # Adjust the 0.5 to control the influence of accuracy
    distance = raw_distance * accuracy_factor

    # Calculate remaining distance to hole
    remaining_distance = hole_distance - distance
    remaining_distance = abs(remaining_distance)  # Keeps the distance positive

    # Rubber band effect: define a tolerance range
    if abs(remaining_distance) <= win_tolerance:
        remaining_distance = 0  # Considered as landed in the hole

    return (distance, remaining_distance)

def update_ball_condition(initial_condition, ball_decay):
# Formula to lower the ball's quality after it is hit
    return initial_condition * math.exp(-3 * ball_decay)



def main():
    print(term.yellow(GolfCommand))# Print the ASCII art (see top of document)
    
    hole_distance = generate_hole_distance
    print_with_typing_effect(term.yellow(ai + "The hole is " + term.white(f"{hole_distance} yards ") + term.normal + "away. Good luck!"))

    while True:
        try:
            success = build_ball()
            if not success:
                continue

            success = build_club()
            if not success:
                continue


            #SWING
            while True:
                print()
                print_with_typing_effect(term.yellow("swinging " + golfer.club.name + "..."))
                distance_items = calculate_swing_distance(swing_power, golfer.strength, golfer.accuracy, golfer.club.potential, golfer.ball.potential, golfer.ball.condition, golfer.ball.mass, hole_distance)
                distance = distance_items[0]
                previous_hole_distance = hole_distance
                hole_distance = distance_items[1]

                golfer.ball.condition = update_ball_condition(golfer.ball.condition, golfer.ball.decay)


                # Determine if the player overshot the hole
                overshot = distance > previous_hole_distance



                # Sound Effects
                print()
                prompt = f"What sound effect would a {golfer.club.name} hitting a {golfer.ball.name} make? Reply with one word, all caps, and an exclamation mark!"
                conversation_swing = [
                    {"role": "user", "content": prompt}
                ]
                sound_effect_response = chat_with_gpt(client, conversation_swing)
                print_with_typing_effect("            " + sound_effect_response)
                print()
                time.sleep(0.5)
                print_with_typing_effect(term.yellow("Calculating " + golfer.ball.name + " trajectory..."))
                time.sleep(1)
                if hole_distance == 0:
                    print()
                    input_with_typing_effect(ai + "Congratulations! You've hit the ball into the hole!")# This should be AI generated.
                    break




                # Information for ChatGPT Narration
                # Check the ball's condition and prepare appropriate message for ChatGPT
                if golfer.ball.condition < condition_threshold:
                    ball_status = f"The {golfer.ball.name} is destroyed beyond use after being hit too hard with the {golfer.club.name}. describe the state of the destroyed {golfer.ball.name} descriptivly and humourously, describing the condition a {golfer.ball.name} would be in after being hit with a {golfer.club.name} in real life."
                else:
                    ball_status = f""
                swing_detail = f"The player is using {golfer.ball.name} as a golfball and a {golfer.club.name} as their golf club. They hit the {golfer.ball.name} a distance of {distance:.2f} yards, and the {golfer.ball.name} is now {hole_distance} yards from the hole."
                if overshot:
                    swing_detail += f"The player overshot the hole by {distance - previous_hole_distance:.2f} yards. Let the player know this."
                else:
                    swing_detail += "The player is approaching the hole."
                swing_detail += f"{ball_status} Please generate a short comment on the swing's outcome (and the ball's condition if it is bad) in two sentences, speaking directly to the player, avoiding technical jargon like 'threshold' and instead giving a plain-english summary of the outcome."

                conversation_swing = [
                    {"role": "user", "content": swing_detail}
                ]
                response_conversation_swing = chat_with_gpt(client, conversation_swing)# ChatGPT's narration 


                # Display Game Narration:
                print()
                print_with_typing_effect(term.yellow(ai + f"it traveled ") + term.white(f"{distance:.2f} yards"))
                print()
                print_with_typing_effect(ai + f"{golfer.ball.name} condition: {golfer.ball.condition * 100:.2f}%")# 
                print()
                print_with_typing_effect(ai + response_conversation_swing)# ChatGPT's naration
                print()
                print_with_typing_effect(ai + f"Distance to hole: {hole_distance:2f} yards")



                # Check if the ball is still usable
                if golfer.ball.condition <= condition_threshold:
                    print()
                    print_with_typing_effect(ai + f"The {golfer.ball.name} is no longer usable.")# TODO: Have ChatGPT rewrite to fix any grammar issues.
                    golfer.inventory.remove(golfer.ball)
                    choose_ball()

                # Ask if the player wants to swing again
                while True:
                    print()
                    next_turn = input_with_typing_effect(ai +
                        "[1] Swing Again\n" +
                        "[2] Change Club\n" +
                        "[3] Change Ball")
                    
                    if next_turn == "1":
                        break
                    elif next_turn == "2":
                        print()
                        choose_club()
                    elif next_turn == "3":
                        print()
                        choose_ball()




            # Ask if the player wants to play again
            print()
            play_again = input_with_typing_effect(ai + "Would you like to play again? (yes/no): ").lower()
            if play_again == "yes":
                print_with_typing_effect(ai + f"The new hole is {hole_distance} yards away. Good luck!")
            else:
                break
        except ValueError:
            print()
            print_with_typing_effect((er + "Invalid input. Please enter valid numerical values."))
    print()
    print_with_typing_effect(ai + "Thank you for playing GolfCommand")
    time.sleep(1)

if __name__ == "__main__":
    main()
    
"""
Special thanks to:
- ChatGPT for writing most of the code for me.
- Playtesters
    - Josh Hufford
    - Phillip Rose
    - Drew "Muffins" Snyder
    - Joe Hufford
    - Mckenna Hufford
    - Jill Hufford
    - Drew
    - Nick 
"""
