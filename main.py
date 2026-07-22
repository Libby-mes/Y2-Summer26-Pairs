
import os
from anthropic import Anthropic
from dotenv import load_dotenv
from app1 import run_luna as luna
from app2 import run_george as george


load_dotenv()
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def print_intro():
    print("=" * 50)
    print("       ✈️  Welcome to Your Travel Assistant  🚌")
    print("=" * 50)
    print("Two AI agents are here to help you:")
    print("  • Luna   – plans your local transportation")
    print("  • George – plans your whole trip, safely and affordably")
    print("=" * 50)
    print()


def print_menu():
    print("=" * 40)
    print("   Welcome to the Travel Assistant")
    print("=" * 40)
    print("  1. Luna   - Transportation planning")
    print("  2. George - Trip planning & booking")
    print("=" * 40)

def choose_starting_agent():
    while True:
        print_intro()

        # Move the input request inside the loop!
        choice = input("Choose an agent to start with (luna/george), Type 'exit' to quit: ").lower()
        
        if choice.lower() == "luna":
            print(f"Great! You've chosen to start with {choice}.")
            return luna()
        elif choice.lower() == "george":
            print(f"Great! You've chosen to start with {choice}.")
            return george()
        elif choice == "exit":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please choose either 'luna' or 'george'.")
            print_menu()

choose_starting_agent() 
