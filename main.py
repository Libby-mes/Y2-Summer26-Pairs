import os
from anthropic import Anthropic
from dotenv import load_dotenv
from app1 import run_luna as luna
from app2 import run_george as george


load_dotenv()
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))


def choose_starting_agent():
    while True:
        # Move the input request inside the loop!
        choice = input("Choose an agent to start with (luna/george), Type 'exit' to quit: ").lower()
        
        if choice.lower() == "luna":
            print(f"Great! You've chosen to start with {choice}.")
            luna()
        elif choice.lower() == "george":
            print("Great! You've chosen to start with {choice}.")
            george()
        elif choice == "exit":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please choose either 'luna' or 'george'.")
choose_starting_agent()


# def run():
#     current_agent_name = choose_starting_agent()
#     histories = {name: [] for name in agents}

#     print(f"Chatting with {current_agent_name}. Type 'switch to <name>' to change agents, or 'exit' to quit.")

#     while True:
#         user_input = input('>> ')

#         if user_input.lower() == 'exit':
#             break

#         if user_input.lower().startswith("switch to "):
#             requested = user_input.lower().replace("switch to ", "").strip()
#             if requested in agents:
#                 current_agent_name = requested
#                 print(f"Switched to {requested}.")
#             else:
#                 print(f"I don't know an agent called '{requested}'.")
#             continue

#         agent = agents[current_agent_name]
#         history = histories[current_agent_name]
#         history.append({'role': 'user', 'content': user_input})

        

#         reply = response.content[0].text
#         print(f'{current_agent_name.capitalize()}: {reply}')


# run()

