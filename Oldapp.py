import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from google import genai
from datetime import datetime
from zoneinfo import ZoneInfo

# Load environment variables
load_dotenv(r"D:\Python Files\Applicatation\.env", override=True)

# Read API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing")


# Create Gemini client
client = genai.Client(api_key=api_key)


# Create FastAPI application
app = FastAPI()


# Request model
class PromptRequest(BaseModel):
    prompt: str


# API endpoint
@app.post("/generate")
def generate_response(request: PromptRequest):

    if not request.prompt.strip():
        return {"response": "Please enter a prompt."}

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=request.prompt
	    #contents=prompt_with_context
        )

        return {
            "response": response.text
        }

    except Exception as e:
        return {
            "response": f"Error: {str(e)}"
        }


# Serve frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")
