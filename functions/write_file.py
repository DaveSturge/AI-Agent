import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Used to write to a file, also creates the file if it doesn't already exist, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory",
            ),
            "content": types.Schema(type=types.Type.STRING, description="The content to be written to the file")
        },
        required=["file_path", "content"],
    ),
)

def write_file(working_directory, file_path, content):
    abs_directory = os.path.abspath(working_directory)
    abs_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file.startswith(f"{abs_directory}/") and not abs_file == abs_directory:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        directories = os.path.dirname(abs_file)
        if directories:
            os.makedirs(directories, exist_ok=True)

        with open(abs_file, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'      
    except Exception as e:
        return f"Error: {str(e)}"