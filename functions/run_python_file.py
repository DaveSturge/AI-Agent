import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"]
    ),
)

def run_python_file(working_directory, file_path, args = None):
    abs_directory = os.path.abspath(working_directory)
    abs_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file.startswith(f"{abs_directory}/") and not abs_file == abs_directory:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_file):
        return f'Error: File "{file_path}" not found.'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        commands = ["uv", "run", abs_file]

        if args:
            commands.extend(args) 

        subprocess_result = subprocess.run(commands, capture_output=True, text=True, timeout=30, cwd= abs_directory)
        
        stdout = subprocess_result.stdout.strip()
        stderr = subprocess_result.stderr.strip()

        output = f"STDOUT:{stdout}\nSTDERR:{stderr}"

        if subprocess_result.returncode != 0:
            output += f"\nProcess exited with code {subprocess_result.returncode}"

        if stdout == "" and stderr == "":
            output = "No output produced."

        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"
