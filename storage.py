import json
import os


# Location of our JSON file
FILE_PATH = "data/conversations.json"


def load_conversations():
    """
    Load conversations from the JSON file.
    """

    if not os.path.exists(FILE_PATH):
        return []

    try:

        with open(FILE_PATH, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):

        return []


def save_conversation(prompt, response):
    """
    Save one user prompt and Gemini response.
    """

    conversations = load_conversations()

    conversation = {
        "prompt": prompt,
        "response": response
    }

    conversations.append(conversation)

    try:

        with open(FILE_PATH, "w", encoding="utf-8") as file:

            json.dump(
                conversations,
                file,
                indent=4,
                ensure_ascii=False
            )

    except OSError as e:

        print(f"Error saving conversation: {e}")
