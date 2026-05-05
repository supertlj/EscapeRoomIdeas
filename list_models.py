from google import genai
import os

client = genai.Client()
for model in client.models.list():
    print(model.name)
