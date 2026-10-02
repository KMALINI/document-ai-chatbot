from dotenv import load_dotenv
from openai import OpenAI
import os

# Load variables from .env
load_dotenv()

# Get API key
api_key = os.getenv("OPENAI_API_KEY")

# Check whether the key was loaded
if not api_key:
    print("API key was not found!")
else:
    print("API key loaded successfully!")

# Create OpenAI client
client = OpenAI(api_key=api_key)

# Make a simple test request
response = client.responses.create(
    model="gpt-5-mini",
    input="Say hello in one short sentence."
)

print("AI Response:")
print(response.output_text)