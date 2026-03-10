import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    for _ in range(20):
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(model="gemini-2.5-flash", contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
        usage = response.usage_metadata
        prompt_token_count = usage.prompt_token_count
        candidates_token_count = usage.candidates_token_count
        function_calls = response.function_calls
        function_responses = []

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if usage is not None:
            if args.verbose:
                print(f"User prompt: {args.user_prompt}")
                print(f"Prompt tokens: {prompt_token_count}")
                print(f"Response tokens: {candidates_token_count}")

            if function_calls is not None:
                function_results = []

                for function_call in function_calls:
                    function_call_result = call_function(function_call)

                    if not function_call_result.parts:
                        raise Exception("Function call result has no parts")

                    function_response = function_call_result.parts[0].function_response
                    if function_response is None:
                        raise Exception("Function response is None")

                    if function_response.response is None:
                        raise Exception("Function response has no response")

                    function_responses.append(function_call_result.parts[0])
                    messages.append(types.Content(role="user", parts=function_responses))
                
                    if args.verbose:
                        print(f"-> {function_response.response}")

            else:
                print(response.text)
                break
        else:
            raise RuntimeError("usage_metadata is None!")

    else:    
        print("Agent stopped: reached maximum number of iterations without producing a final answer.")
        exit(1)

if __name__ == "__main__":
    main()