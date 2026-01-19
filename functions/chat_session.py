from google.genai import types


def get_model_response(client, model_id, messages, tools, system_instruction):
    """Wraps the Gemini API content generation call."""
    return client.models.generate_content(
        model=model_id,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=tools,
            system_instruction=system_instruction,
        ),
    )
