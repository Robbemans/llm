import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model="gemini-2.5-flash", contents=messages)
    usage = response.usage_metadata
    prompt_token_count = usage.prompt_token_count
    candidates_token_count = usage.candidates_token_count

    if usage is not None:
        print(f"Prompt tokens: {prompt_token_count}\nResponse tokens: {candidates_token_count}")
        print(response.text)
    else:
        raise RuntimeError("usage_metadata is None!")

if __name__ == "__main__":
    main()