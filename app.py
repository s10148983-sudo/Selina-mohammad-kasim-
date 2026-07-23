import os
from google import genai

os.environ["GEMINI_API_KEY"] = "YOUR_GEMINI_API_KEY_HERE"

client = genai.Client()

response = client.models.generate_content(
    model="gemini-1.5-flash",
    contents="வணக்கம், எப்படி இருக்கிறீர்கள்?",
)

print(response.text)
