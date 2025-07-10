import os

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