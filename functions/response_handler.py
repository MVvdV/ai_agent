from google.genai import types

from call_function import call_function


def handle_function_calls(function_calls, verbose=False):
    """Executes multiple function calls and returns their response parts."""
    tool_parts = []
    for function_call in function_calls:
        # call_function returns a types.Content object containing tool parts
        result_content = call_function(function_call, verbose=verbose)
        if result_content.parts:
            tool_parts.extend(result_content.parts)
    return tool_parts


def print_response(response, verbose=False):
    """Prints the final model response and usage metadata if verbose."""
    if verbose:
        usage = response.usage_metadata
        p_tokens = usage.prompt_token_count if usage else "N/A"
        r_tokens = usage.candidates_token_count if usage else "N/A"
        print(f"Prompt tokens: {p_tokens}")
        print(f"Response tokens: {r_tokens}")

    print(f"Response:\n{response.text}")
