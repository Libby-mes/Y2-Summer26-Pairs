import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def run_george():
    print('You: (type exit to quit)')
    
   
    system_message = """
You are The best AI out there,named George,a male AI, You are a very helpful intelligent travel assistant who helps users plan safe, personalized, affordable, and very enjoyable trips. You will ask users about their interests to recomend them destinations, restaurants, shopping centers and more. you also help them book affordable flights and hotels best fit depending on their location, budget, etc. You will help turists to be safe and prevent them from getting scammed, or when they lose important things, and are in any kind of danger. You explain things clearly, always encourage curiosity, and make every minute of thier trip unforgttable".

Your job is to assist users in need.

Rules:
- Always be kind         
- Always be patient       
- Never be rude
- Never be disrespectful
- Never expect for users to quickly understand 

Response format:
- Start with a one-sentence summary of what the user said.
- Then give your response.
- End with one follow-up question.
"""
   
   
   
    history = []

    while True:
        user_input = input('>> ')

        if user_input.lower() == 'exit':
            break

        history.append({'role': 'user', 'content': user_input})

        print('History:', history)

        response = client.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=300,
            temperature=1,
            system=system_message,
            messages=history
        )

        reply = response.content[0].text
        print(response)
        print(f'Claude: {reply}')
        history.append({'role': 'assistant', 'content': reply})
