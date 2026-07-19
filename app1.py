import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def run_chat():
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
    - remind the user about their goal, dont over do it."""

    history = []

    user_goal = input("Do you have a goal for this conversation? What is it? ")

    if "no" in user_goal.lower():
        print("Okay, let's just chat then! whats on your mind?")
    else:
        history.append({'role': 'user', 'content': user_goal})
        print("Great! Let's work towards that goal together. what is the first step you want to take?")

    while True:
        user_input = input('>> ')

        if user_input.lower() == 'exit':
            break

        history.append({'role': 'user', 'content': user_input})
        print('History:', history)

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            temperature=1,
            system=system_message,
            messages=history,
            tools=tools
        )

        # Add Claude's response to history (needed even if it's a tool call)
        history.append({'role': 'assistant', 'content': response.content})

        if response.stop_reason == "tool_use":
            for block in response.content:
                if block.type == "tool_use":
                    if block.name == "get_transit_options":
                        result = get_transit_options(**block.input)

                        # send the tool result back to Claude
                        history.append({
                            'role': 'user',
                            'content': [{
                                'type': 'tool_result',
                                'tool_use_id': block.id,
                                'content': result
                            }]
                        })

            # ask Claude again, now that it has the tool result
            followup = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=300,
                temperature=1,
                system=system_message,
                messages=history,
                tools=tools
            )
            reply = followup.content[0].text
            history.append({'role': 'assistant', 'content': followup.content})
        else:
            reply = response.content[0].text

        print(f'Claude: {reply}')
run_chat()
