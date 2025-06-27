import cohere
import os
import sys
import time
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
api_key = os.getenv("COHERE_API_KEY")

if not api_key:
    print("Invalid or missing Cohere API key. Check .env file for mistakes.")

# Initialize Cohere client
co = cohere.Client(api_key)

def get_params(prompt, default, cast_type=float):
    try:
        val = input(f"{prompt} (default={default}): ").strip()
        return cast_type(val) if val else default
    except ValueError:
        print("Invalid input. Using default.")
        return default
    
print("Change the parameters for your response, or press Enter to accept defaults:")
temperature = get_params("Temperature, 0.0-1.0 (creativity of model)", 0.7)
max_tokens = get_params("Max tokens (response length limit)", 150, int)

print("Cohere Chatbot (type 'quit' or 'exit' to quit)\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ["exit", "quit"]:
        break
    elif not user_input or user_input.isspace():
        print("Please enter valid text.")
        continue
    elif len(user_input) > 1000:
        print("Input is too long. Keep <1000 chars")
        continue

    try:
       response = co.generate(
           model="command-r-plus",
           prompt=user_input,
           max_tokens=max_tokens,
           temperature=temperature
       )
       print("Bot:", response.generations[0].text.strip())

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
