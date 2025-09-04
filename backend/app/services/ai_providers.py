import asyncio
import os
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# OpenAI placeholder
async def openai_stream(prompt: str):
    tokens = ["Hello", " ", "from OpenAI!"]
    for token in tokens:
        yield token
        await asyncio.sleep(0.2)

# Claude placeholder
async def anthropic_stream(prompt: str):
    tokens = ["Hello", " ", "from Claude!"]
    for token in tokens:
        yield token
        await asyncio.sleep(0.2)

# Gemini real streaming
async def gemini_stream(prompt: str):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt, stream=True)

    for chunk in response:
        if chunk.text:
            for token in chunk.text.split(" "):
                yield token + " "
                await asyncio.sleep(0.05)