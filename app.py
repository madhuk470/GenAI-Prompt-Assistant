import os

import time

from datetime import datetime
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from google import genai
from google.genai import types

from storage import save_conversation, load_conversations


# -----------------------------------
# 1. Load environment variables
# -----------------------------------

load_dotenv(r"D:\Python Files\.env", override=True)


# -----------------------------------
# 2. Get Gemini API key
# -----------------------------------

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing")


# -----------------------------------
# 3. Create Gemini client
# -----------------------------------

client = genai.Client(api_key=api_key)


# -----------------------------------
# 4. Create FastAPI application
# -----------------------------------

app = FastAPI()


# -----------------------------------
# 5. Define request structure
# -----------------------------------

class PromptRequest(BaseModel):
    prompt: str
    system_instruction: str
    temperature: float
    max_output_tokens: int


# -----------------------------------
# 6. Generate response
# -----------------------------------

@app.post("/generate")
def generate_response(request: PromptRequest):

    # Check prompt
    if not request.prompt.strip():
        return {
            "response": "Please enter a prompt."
        }

    # Get current India date/time
    current_datetime = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).strftime("%Y-%m-%d %H:%M:%S")

    # Add current time as context
    prompt_with_context = f"""
        Current date and time in India (IST):
        {current_datetime}

        User question:
        {request.prompt}

        Use the current date/time above when the user asks
        about the current date or time.
        """

    try:

        # Call Gemini
        response = client.models.generate_content(

            model="gemini-3.5-flash-lite",

            contents=prompt_with_context,

            config=types.GenerateContentConfig(

                system_instruction=request.system_instruction,

                temperature=request.temperature,

                max_output_tokens=request.max_output_tokens
            )
        )

        # Send Gemini response to browser

        save_conversation(
            request.prompt,
            response.text
        )

        
        return {
            "response": response.text
        }

    except Exception as e:

        return {
            "response": f"Error: {str(e)}"
        }


# -----------------------------------
# 7. Serve frontend
# -----------------------------------
# -----------------------------------
# 8. Get conversation history
# -----------------------------------

@app.get("/history")
def get_history():

    conversations = load_conversations()

    return {
        "conversations": conversations
    }


# -----------------------------------
# 9. Serve frontend
# -----------------------------------

app.mount(
    "/",
    StaticFiles(directory="static", html=True),
    name="static"
)
