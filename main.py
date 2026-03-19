import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
	raise RuntimeError("API key not found")


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    client = genai.Client(api_key=api_key)
    for _ in range(20):
        result = generate_content(client, messages, args.verbose)
        if result:
            print("Final response:")
            print(result)
            return

    print("Maximum iterations reached")
    sys.exit(1)

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
    model='gemini-2.5-flash', contents=messages, config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt,
    temperature=0
)
)
    for candidate in response.candidates:
        messages.append(candidate.content)
    if response.usage_metadata is None:
        raise RuntimeError("usage_metadata not found")
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    if response.function_calls:
        function_results = []
        for function_call in response.function_calls:
            call_function_result = call_function(function_call, verbose=verbose)
            if not call_function_result.parts:
                raise Exception("No parts in function call result")
            if not call_function_result.parts[0].function_response:
                raise Exception("Not a FunctionResponse")
            if not call_function_result.parts[0].function_response.response:
                raise Exception("Result shouldn't be None")
            function_results.append(call_function_result.parts[0])
            if verbose:
                print(f"-> {call_function_result.parts[0].function_response.response}")
        messages.append(types.Content(role="user", parts=function_results))    
    else:
        return(response.text)


if __name__ == "__main__":
    main()
