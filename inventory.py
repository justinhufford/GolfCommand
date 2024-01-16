import time
import os
import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    pass


async def chatgpt_stream(client, messages, model="gpt-4-1106-preview", stream=True):
    
    #          Model:                  Input Cost:          Output Cost:      
    #          gpt-4-1106-preview      $0.010 / 1K tokens	$0.030 / 1K tokens
    #          gpt-3.5-turbo-1106      $0.001 / 1K tokens	$0.002 / 1K tokens
    stream = await client.chat.completions.create(
        model=model,
        messages=messages,
        stream=stream
    )

    async for chunk in stream:
        content = chunk.choices[0].delta.content or ""
        for char in content:
            print(char, end="", flush=True)
            await asyncio.sleep(0.000000001)  # Adjust delay to simulate typing speed
            
async def chatgpt(client, messages, model="gpt-4-1106-preview", stream=False):
    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        stream=stream
    )

    # Access the response content correctly
    # The exact way to access this depends on the response structure
    if response.choices and len(response.choices) > 0:
        content = response.choices[0].message.content  # Modify according to the actual structure
        return content.strip()

    return ""  # Return an empty string if no content is found
    
    

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
        
          
#   ┆                
#   ┆      
    def __str__(self):
        return f"{self.name}\nQty: {self.qty}\nType: {self.type}\n{self.bio}\nPotential: {self.potential}\nMass: {self.mass}\nCondition: {self.condition}\nDecay: {self.decay}"
    
    
    
    
class Inventory:           
#   ┆                
#   ┆  
    def __init__(self):
       self.inv = [
           
            Item("Driver", 
                1, 
                "Club", 
                "Great for long shots, not so good for puttin'",
                92,
                1.5,
                80,
                0.2,
            ),    
            Item("Golf Ball", 
                10, 
                "Ball", 
                "A mystical orb with unknown powers.",
                95,
                0.1,
                100,
                0.2,
            ),
            Item("Lucky Hat", 
                1, 
                "Accessory", 
                "You swear you swing better when you wear this hat...",
                5,
                0.2,
                71,
                20,
            )
       ]           
#   ┆                
#   ┆  
    async def list_inv(self):
        while True:
            clear()
            print('INVENTORY:')
            for index, item in enumerate(self.inv):
                print(f'[{index + 1}] {item.name}')
            print('[0] BACK')
            choice = int(input())
            
            try:
                if choice == 0 or '':
                    return
                else:
                    selected_item = self.inv[choice - 1]
                    clear()
                    print(selected_item)
                    input()

            except ValueError:
                print("Invalid input. Please enter a number.")
                
            except IndexError:
                print("Invalid number. Please enter a number from the list.")
            except Exception as e:
                print(f"Problem in selecting item from inventory: {e}")            
# 
        
    #This is the prompt sent to ChatGPT that allows it to return numeric values for the calculate_swing_distance formula:
    #Later versions of the game may use a vector database instead to reduce API costs.
    build_object_prompt = """
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
|the sun|1000000000|4,400,000,000,000,000,000,000,000,000|0.8|0.1 
    """
    
        
    async def build_object(self):
        print("What would you like to add?")
        name = input()
        print(f'Generating {name}...')
        qty = '1'
        type = 'object'
        bio = "I'll implement this later. -JH"
        
        build_object_request = [
            {"role": "user", "content": self.build_object_prompt + f"Please estimate the potential, mass, condition, and decay values for this object: {name}. Please output your response as a comma-separated list, with no other comment, narration, or explanation. Always provide some values, even if you don't know, just make something up. What are the values of {name}?"},
        ]
        
        response_build_object = await chatgpt(client, build_object_request)# ChatGPT's Response
        
        if response_build_object and isinstance(response_build_object, str):
            response_values = response_build_object.split(",")  # Separates the values generated by ChatGPT
            
            if len(response_values) != 4:  # If ChatGPT does not return 4 values,
                print(f"Error building {name}, please try again or choose a different object.")
                return False
        

            potential = float(response_values[0]) / 100
            mass = float(response_values[1]) * 10
            condition = float(response_values[2])
            decay = float(response_values[3]) / 100
            
            new_item = Item(name, qty, type, bio, potential, mass, condition, decay)
            self.inv.append(new_item)
            clear()
            print(new_item)
            input()
            return True
        else:
            print(f"Failed to get valid response for building {name}. Please try again.")



async def display_menu(inventory):    
    menu_items = ["INVENTORY", "ADD ITEM"]
    
    while True:
        clear()
        print('MAIN MENU')
        for index, item in enumerate(menu_items):
            print(f'[{index + 1}]', item)
        print('[0] QUIT')
        
        choice = input()
        
        if choice == '1':
            await inventory.list_inv()
        elif choice == '2':
            clear()
            try:
                await inventory.build_object()
            except Exception as e:
                print(f"Error adding item. Failure is part of the learning process!\n{e}")
                input()
        elif choice == '0':
            clear()
            print('Goodbye!')
            time.sleep(0.5)
            break
        else:
            clear()
            print('\nPlease try again')
            input() 
        
        
async def main():
    inventory = Inventory()
    try:
        await display_menu(inventory)
    except Exception as e:
        print(f"Unexpected error: {e}")

    
asyncio.run(main())
