from anthropic import Anthropic
import os
from datetime import datetime
from PIL import Image, ImageGrab
import io
import pyautogui
import base64
from colorama import init, Fore, Style
import cv2
import numpy as np

import subprocess
client = Anthropic(api_key=os.environ.get("API_KEY"))

def focus_chrome():
    apple_script = """
    tell application "Google Chrome"
        activate
    end tell
    """
    subprocess.run(["osascript", "-e", apple_script])


def break_function():
    return "Done with the task, breaking out to get user input"

# Initialize colorama
init()


# Color constants
USER_COLOR = Fore.WHITE
CLAUDE_COLOR = Fore.BLUE
TOOL_COLOR = Fore.YELLOW
RESULT_COLOR = Fore.GREEN

# MODEL_NAME = "claude-3-haiku-20240307"
MODEL_NAME = "claude-3-5-sonnet-20240620"

# Helper function to print colored text
def print_colored(text, color):
    print(f"{color}{text}{Style.RESET_ALL}")

messages = []

system_prompt = '''
You are Claude, an AI assistant capable of controlling the user's browser with the help of Vimium extension hint tags and the keyboard control.


You can do six types of function calls

1. take_screenshot - Take screenshot and see the hint tags to determine which element to click. 
2. type_vimium_command - type the hint tags as vimium chrome extension commands that you saw from the screenshot. Pass input as lowercase. DO NOT add 'f' in front of the command.
3. type_text -> Type text.
4. break -> Break out of the loop and get user input.
5. search -> Search via hint tag of the search query bar or worst case: Open Vimium's search box and type a query. 
6. copy_or_paste_url -> Copy url to clipboard or paste the url from clipboard.

Always see if the asked thing is in the screenshot or not before going for search.

If you are not sure about the hint tag, take a screenshot again.

If you have to search, always look for search query bar hint tag on the web page. Don't look for the button.
Please try to figure out the search bar as sometimes the text "search" may be hidden by the tag.

"search" function call is the last resort.

When user asks you to do something, you are required to look at the screenshot and find the vimium hint tag. If you can see it on the screen good, otherwise
you can use the search option like Youtube search or vimium_search

- You can plan multiple function calls in a row (combination of vimium command or text)
- Plan function calls in a proper sequence

'''

def take_screenshot(tool_id):

    
    focus_chrome()

    pyautogui.sleep(1)
    pyautogui.typewrite('f')

    
    screenshot = ImageGrab.grab()
    
    # Calculate the new size while maintaining aspect ratio
    max_size = (1280, 720)
    screenshot.thumbnail(max_size, Image.LANCZOS)

    screenshot = screenshot.convert('RGB')
    
    # Create a directory to store screenshots if it doesn't exist
    screenshot_dir = os.path.join(os.path.expanduser("~"), "Desktop", "vimSonnet")
    os.makedirs(screenshot_dir, exist_ok=True)
    
    # Generate a unique filename based on the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.jpg"
    filepath = os.path.join(screenshot_dir, filename)
    
    # Save the screenshot as JPEG with 100% quality
    screenshot.save(filepath, format='JPEG', quality=100)

    print_colored(f"Screenshot saved to: {filepath}", TOOL_COLOR)
    
    # Encode the image to base64
    with io.BytesIO() as buffer:
        screenshot.save(buffer, format="JPEG", quality=100)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    tool_result_message = [
        {
            "type": "text",
            "text": f"I have provided you with a screenshot. The image has been resized to fit within 1280x720 pixels while maintaining its aspect ratio. Look at the hint markers carefully"
        },
        {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/jpeg",
                "data": image_base64
            }
        }
    ]
    pyautogui.press('escape')
    print(f"Screenshot saved to: {filepath}")
    return tool_result_message

def type_vimium_command(command):
    pyautogui.write(command)
    pyautogui.press('escape')
    return f"Executed Vimium command: {command}"

def search(query, hint_tag=None):
    if hint_tag:
        # Hint tag search
        pyautogui.write(hint_tag)  # Type the hint tag
        
        if query:
            pyautogui.write(query)  # Type the search query
            pyautogui.press('enter')  # Press enter to execute the search
        return f"Used hint tag '{hint_tag}' and searched for: {query}"
    else:
        # Vimium search box
        pyautogui.press('o')  # Press 'o' to open Vimium's search box
        pyautogui.write(query)  # Type the search query
        pyautogui.press('enter')  # Press enter to execute the search
        return f"Opened search box and searched for: {query}"

def type_text(text, interval=0.1):
    pyautogui.write(text, interval=interval)

    # get back into insert mode
    pyautogui.press('escape')
    
    return f"Typed: {text}"

def copy_or_paste_url(command):
    command_descriptions = {
        "yy": "Copied current URL to clipboard",
        "paste": "Pasted URL from clipboard"
    }
    
    if command == "yy":
        pyautogui.press(command)
    elif command == "paste":
        pyautogui.hotkey('ctrl', 'v')
    else:
        return f"Unknown command: {command}"
    
    return command_descriptions.get(command, f"Executed command: {command}")

tools = [
    {
        "name": "type_text",
        "description": "Type the specified text with an optional interval between keystrokes.",
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to type"
                },
                "interval": {
                    "type": "number",
                    "description": "The interval between keystrokes in seconds (optional, default: 0.1)"
                }
            },
            "required": ["text"]
        }
    },
        {
        "name": "take_screenshot",
        "description": "Take a screenshot of the current screen and return both the file path and the image data for analysis. Send to claude before doing executing other tools",
        "input_schema": {
            "type": "object",
              "properties": {
                "tool_id": {
                    "type": "string",
                    "description": "tool id"
                }
            },
            "required": ["tool_id"]
        }
    },

      {
        "name": "type_vimium_command",
        "description": "Type a Vimium command to control the browser.",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The Vimium command to execute"
                }
            },
            "required": ["command"]
        }
    },

     {
        "name": "break",
        "description": "Break out of loop when done with task.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },

    {
    "name": "search",
    "description": "Search. Uses hint tag - higher priority if provided, otherwise uses Vimium search box.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query."
            },
            "hint_tag": {
                "type": "string",
                "description": "The Vimium hint tag for the search field"
            }
        },
        "required": ["query"]
    }
},

    {
    "name": "copy_or_paste_url",
    "description": "Copy current URL to clipboard or paste URL from clipboard: yy (copy URL), paste (paste URL)",
    "input_schema": {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "enum": ["yy", "paste"],
                "description": "The command to execute: 'yy' to copy, 'paste' to paste"
            }
        },
        "required": ["command"]
    }
}
]


def execute_tool(tool_name, tool_input):
    if tool_name == "type_text":
        return type_text(tool_input["text"], tool_input.get("interval", 0.1))
    elif tool_name == "take_screenshot":
        return take_screenshot(tool_input["tool_id"])
    elif tool_name == "type_vimium_command":
        return type_vimium_command(tool_input["command"])
    elif tool_name == "get_user_input":
        return break_function()
    elif tool_name == "search":
        return search(tool_input["query"], tool_input.get("hint_tag"))
    elif tool_name == "copy_or_paste_url":
        return copy_or_paste_url(tool_input["command"])
    else:
        return f"Unknown tool: {tool_name}"


def chat_with_claude(user_input, image_path=None):
    global messages

    print(f"\n{'='*50}\nUser Message: {user_input}\n{'='*50}")

    messages.append({"role": "user", "content": user_input})
    

    break_out_of_loop = False
    while break_out_of_loop == False:
        try:
            response = client.messages.create(
                model= MODEL_NAME,
                max_tokens=4000,
                system=system_prompt,
                messages=messages,
                tools=tools,
                tool_choice={"type": "tool", "name": "take_screenshot"}
            )
        except Exception as e:
            print(f"Error calling Claude API: {str(e)}")
            return "Error while taking screenshot."

        print(f"\nInitial Response:")

        print(response)

        messages.append({"role": "assistant", "content": response.content})
        for block in response.content:
            
            if block.type == "tool_use":
                tool_name = block.name
                tool_input = block.input
                tool_use_id = block.id
                result = execute_tool(tool_name, tool_input)
            
                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": tool_use_id,
                            "content": result
                        }
                    ]
                })

                if tool_name == "take_screenshot":

                    print(f"Tool Used: {tool_name}")

                    try:
                    
                        second_response = response = client.messages.create(
                                    model = MODEL_NAME,
                                    max_tokens=4000,
                                    system=system_prompt,
                                    messages=messages,
                                    tools=tools,
                                    tool_choice={"type": "auto"}
                                )

                        messages.append({"role": "assistant", "content": second_response.content})

                        for block in second_response.content:

                            if block.type == "text":
                                # messages.append({"role": "assistant", "content": [block]})
                                print(block)
                                pass


                            elif block.type == "tool_use":
                                second_tool_name = block.name
                                second_tool_input = block.input
                                second_tool_use_id = block.id
                                second_result = execute_tool(second_tool_name, second_tool_input)

                          

                                messages.append({
                                    "role": "user",
                                    "content": [
                                        {
                                            "type": "tool_result",
                                            "tool_use_id": second_tool_use_id,
                                            "content": second_result
                                        }
                                    ]
                                })

                                if second_tool_name == "break":
                                    print(result)
                                    break_out_of_loop = True
                                    break

                        print("*******************************")
                        print(second_response.content)
                        print("*******************************")

                    except Exception as e:
                        print(f"Error calling Claude API: {str(e)}")
                        return "I'm sorry, there was an error communicating with the AI. Please try again."
                    
                else:
                    print(f"Tool Used: {tool_name}")

        

    
    return "all fine"


def main():
    print_colored("Welcome anon", CLAUDE_COLOR)
    print_colored("Type 'exit' to end the conversation.", CLAUDE_COLOR)
    print_colored("To include an image, type 'image' and press enter. Then drag and drop the image into the terminal.", CLAUDE_COLOR)
    
    while True:
        user_input = input(f"\n{USER_COLOR}You: {Style.RESET_ALL}")
 

        if user_input.lower() == 'exit':
            print_colored("Thanks, goodbye.", CLAUDE_COLOR)
            break
        
        else:
            response = chat_with_claude(user_input)
        
        if response.startswith("Error") or response.startswith("Sorry we encountered an error communicating with the AI."):
            print_colored(response, TOOL_COLOR)

if __name__ == "__main__":
    main()