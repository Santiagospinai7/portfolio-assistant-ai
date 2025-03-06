import os

from dotenv import load_dotenv
from together import Together

load_dotenv()

client = Together(api_key=os.getenv("TOGETHER_AI_API_KEY"))

response = client.chat.completions.create(
    model="mistralai/Mistral-7B-Instruct-v0.3",
    messages=[{"role": "user", "content": "What are some fun things to do in New York?"}],
)
print(response.choices[0].message.content)