import argparse
import os
from types import NoneType

from dotenv import load_dotenv
from google import genai
from google.genai import types

# --- ENVIRONMENT ---
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not isinstance(api_key, str):
    raise RuntimeError("No valid API key found")


# ------ MAIN -------
def main():
    client = genai.Client(api_key=api_key)
    model = "gemini-2.5-flash"

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    response = client.models.generate_content(model=model, contents=messages)
    if isinstance(response, NoneType):
        raise RuntimeError("No responce from the API call")
    print(
        f"Prompt: {args.user_prompt}\n"
        f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n"
        f"Response tokens: {response.usage_metadata.candidates_token_count}\n"
        f"Response:\n{response.text}"
    )


if __name__ == "__main__":
    main()
