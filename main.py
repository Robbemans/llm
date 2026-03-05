import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model="gemini-2.5-flash", contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
    usage = response.usage_metadata
    prompt_token_count = usage.prompt_token_count
    candidates_token_count = usage.candidates_token_count
    function_calls = response.function_calls

    if usage is not None:
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {prompt_token_count}")
            print(f"Response tokens: {candidates_token_count}")
        if function_calls is not None:
            for function_call in function_calls:
                print(f"Calling function: {function_call.name}({function_call.args})")
        else:
            print(response.text)
    else:
        raise RuntimeError("usage_metadata is None!")

if __name__ == "__main__":
    main()