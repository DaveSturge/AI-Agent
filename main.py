import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

function_dict = {"get_file_content": get_file_content, "get_files_info": get_files_info, "run_python_file": run_python_file, "write_file": write_file}

def call_function(function_call_part: types.FunctionCall, verbose=False):

    function_name = function_call_part.name

    if function_name not in function_dict:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    new_dict = function_call_part.args.copy()
    new_dict['working_directory'] = './calculator'

    if verbose:
        print(f"Calling function: {function_name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_name}")

    function = function_dict[function_name]

    function_result = function(**new_dict)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

args = sys.argv

if len(args) <= 1:
    print("no argument provided")
    sys.exit(1)

user_prompt = args[1]
messages = [types.Content(role = "user", parts=[types.Part(text = user_prompt)])]

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(function_declarations=[schema_get_files_info,schema_get_file_content,schema_write_file,schema_run_python_file])

response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))

if "--verbose" in args:
    verbose = True

    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
else:
    verbose = False

if response.function_calls: 
    function = response.function_calls[0]
    function_res = call_function(function, verbose)

    if function_res.parts and function_res.parts[0] and function_res.parts[0].function_response and function_res.parts[0].function_response.response:
        if verbose:
            print(f"-> {function_res.parts[0].function_response.response}")
    else:
        raise Exception("No response")

else:
    print(response.text)



