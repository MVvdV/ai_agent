import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions
from functions.chat_session import get_model_response
from functions.response_handler import handle_function_calls, print_response
from prompts import system_prompt

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
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(20):  # while True:
        # 1. Get response from model
        response = get_model_response(
            client, model, messages, [available_functions], system_prompt
        )

        if not response or not response.candidates:
            raise RuntimeError("No valid response from API")

        # 2. Add model's candidate to history (important for tool context)
        candidate_content = response.candidates[0].content
        if candidate_content is None:
            raise RuntimeError("Response candidate content is None")
        messages.append(candidate_content)

        # 3. Check for function calls
        if response.function_calls:
            # Execute all calls and get their response parts
            tool_parts = handle_function_calls(response.function_calls, args.verbose)

            # Add the tool outputs back to message history
            messages.append(types.Content(role="tool", parts=tool_parts))

            # Loop again so the model can see the tool results
            continue

        # 4. If no function calls, print final text response and exit
        print_response(response, args.verbose)
        break


if __name__ == "__main__":
    main()
