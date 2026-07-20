import os
import requests
from datetime import datetime
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()  

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))


# Turn a place name into coordinates 
def geocode_place(place_name):
    # Nominatim is a free service that converts place names into lat/lon
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": place_name, "format": "json", "limit": 1, "countrycodes": "us"}
    headers = {"User-Agent": "student-transit-agent"}  # required by Nominatim

    data = requests.get(url, params=params, headers=headers).json()
    if not data:
        return None
    return float(data[0]["lat"]), float(data[0]["lon"])


# Use those coordinates to ask Transitland for a route 
def get_transit_options(origin, destination):
    origin_coords = geocode_place(origin)
    dest_coords = geocode_place(destination)

    if not origin_coords or not dest_coords:
        return f"Couldn't find '{origin}' or '{destination}'."

    now = datetime.now()
    params = {
        "fromPlace": f"{origin_coords[0]},{origin_coords[1]}",
        "toPlace": f"{dest_coords[0]},{dest_coords[1]}",
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "api_key": os.getenv("TRANSITLAND_API_KEY")
    }

    data = requests.get("https://transit.land/api/v2/routing/otp/plan", params=params).json()
    itineraries = data.get("plan", {}).get("itineraries", [])

    if not itineraries:
        return f"No routes found from {origin} to {destination}."

    best = itineraries[0]
    minutes = best["duration"] // 60

    steps = []
    for leg in best["legs"]:
        if leg["mode"] == "WALK":
            steps.append(f"walk to {leg['to']['name'] or destination}")
        else:
            route_name = leg.get("routeShortName") or leg.get("routeLongName") or leg["mode"]
            steps.append(f"take {route_name} from {leg['from']['name']} to {leg['to']['name']}")

    return f"{origin} to {destination}, ~{minutes} min: " + "; then ".join(steps)


# Tell the agent this function exists, so it can call it when needed
tools = [
    {
        "name": "get_transit_options",
        "description": "Always call this tool whenever the user asks how to get from one place to another, or asks about transit/route options between two locations. Do not answer from general knowledge — use this tool to get real, current transit data.",
        "input_schema": {
            "type": "object",
            "properties": {
                "origin": {"type": "string", "description": "Starting place name"},
                "destination": {"type": "string", "description": "Destination place name"}
            },
            "required": ["origin", "destination"]
        }
    }
]


def run_luna():
    print("=" * 50)
    print("       🚌  Welcome to Luna, Your Transportation Agent  ✈️")
    print("=" * 50)
    print("Luna is here to help you plan your transportation needs for your trip.")
    print('You: (type exit to quit)')

    system_message = """you are Luna, a women AI, you are a Transpotation Agent AI, 
    Your job is to help People and families to plan the transportation in their vacation, or just help with transportation.
    You will provide the user with the correct inforamation. you will tell them the best option always,
    meaning you will take in consideration if they are traveling as a family or solo, if they ids or not,
    if its better by car or train or bus.
    you always stay calm and collected, even if the user is being rude or mean.
    you have a calm aura. you are intelligent and knw every thing about transportation n the world.
    you may add fun emojis to your responses to make them more fun and engaging, but you must not overuse them.

   you may also sometimes invite them to visit a special place depeding on their reqest but not in every answer.

       When you answer follow the next format:
    - [Summary]: one sentence repeating what the user asked to make sure you got it correctly.
    - [Response]: the main answer, that in informative and not messy.
    - [Next Step]: one concrete action the user can take to help them achive their goal, or a question to get more information from the user.


    you must never:
    - break character
    - be rude
    - be mean
    - take personal information from the user
    - give personal information to the user
    - give medical advice
    - give legal advice
    - give instruction on how to do illegal things
    - help someone hurt themeself or others
    
    you must always:
    - be kind
    - be helpful
    - be informative
    - be friendly
    - be organized
    - be understandable
    - warn the user if a tool or action they are asking about is illegal, unsafe, or harmful
    - warn the user if a tool is asking for personal information or if it is unsafe to use or acting weirdly
    - ask the user for clarification if you are unsure what they mean
    - ask questions to get more information on the input
    - ask if the information that is given is personal information or not
    - remind the user about their goal, dont over do it.
    - always use the get_transit_options tool when the user asks about travel between two places,
    instead of answering from your own knowledge"""

    history = []

    user_goal = input("Do you have a goal for this conversation? What is it? ")
    if "no" in user_goal.lower():
        print("Okay, let's just chat then! whats on your mind?")
    elif user_goal.lower() == "exit":
        print("Exiting the program.")
        return
    else:
        history.append({'role': 'user', 'content': user_goal})
        print("Great! Let's work towards that goal together. what is the first step you want to take?")

    while True:

        MAX_CHARS = 8000

        user_input = input('>> ')

        if user_input.lower() == 'exit':
            print("Exiting the program.")
            break
        elif user_input.lower().startswith('switch to george'):
            from app2 import run_george as george
            return george()
        
        # Check length of message before sending to Anthropic
        if len(user_input) > MAX_CHARS:
            print("Input is too long!")
            continue

        else:
            
            history.append({'role': 'user', 'content': user_input})

            # send the conversation to the agent, letting it know it can use our tool
            response = client.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=300,
                temperature=1,
                system=system_message,
                messages=history,
                tools=tools
            )

            history.append({'role': 'assistant', 'content': response.content})

            # keep resolving tool calls until the model gives a final text reply
            while response.stop_reason == "tool_use":
                for block in response.content:
                    if block.type == "tool_use" and block.name == "get_transit_options":
                        result = get_transit_options(**block.input)

                        # send the tool's result back to the agent so it can use it in a reply
                        history.append({
                            'role': 'user',
                            'content': [{'type': 'tool_result', 'tool_use_id': block.id, 'content': result}]
                        })

                # ask the agent again, now that it has the real transit data
                response = client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=300,
                    temperature=1,
                    system=system_message,
                    messages=history,
                    tools=tools
                )
                history.append({'role': 'assistant', 'content': response.content})

            # safely pull out the text block instead of assuming content[0] is text
            reply = next((block.text for block in response.content if block.type == "text"), "")
            print(f'Luna: {reply}')

