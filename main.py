import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from call_function import call_function

def main():
    load_dotenv()

    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )

    system_prompt = """
        You are a helpful AI coding agent.
        
        When a user asks a question or makes a request, make a function call. You can perform the following operations:
        
        - List files and directories
        - Read the content of a file
        - Write to a file (create or update)
        - Run a python file with optional arguments
        
        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    if len(sys.argv) < 2:
        print("Usage: python main.py <PROMPT>")
        sys.exit(1)
    prompt = sys.argv[1]

    verbose_flag = False
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose_flag = True

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file
        ]
    )

    config=types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt
    )

    max_iters = 20
    for i in range (0, max_iters):
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=messages,
            config=config
        )

        if response is None or response.usage_metadata is None:
            print("response is malformed")
            return

        if verbose_flag:
            print(f"User prompt: {prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        if response.candidates:
            for candidate in response.candidates:
                if candidate is None or candidate.content is None:
                    continue
                messages.append(candidate.content)

        if response.function_calls:
            for function_call_part in response.function_calls:
                result = call_function(function_call_part, verbose_flag)
                messages.append(result)
        else:
            # final agent text message
            print(response.text)
            return


main()