import os
from google import genai
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory = None):
    abs_working_dir = os.path.abspath(working_directory)

    joined = os.path.join(working_directory, directory)
    abs_dir = os.path.abspath(joined)
    
    if not abs_dir.startswith(f"{abs_working_dir}/") and not abs_dir == abs_working_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(abs_dir):
        return f'Error: "{directory}" is not a directory'
    
    dir_content = os.listdir(joined)

    output_list = []
    for file in dir_content:
        try:
            full_file_path = os.path.join(joined, file)
            file_size = os.path.getsize(full_file_path)
            is_dir = os.path.isdir(full_file_path)

            output_list.append(f"- {file}: file_size={file_size} bytes, is_dir={is_dir}")
        except Exception as e:
            return f"Error: {str(e)}"
    
    joined_string = '\n'.join(output_list)

    return joined_string

