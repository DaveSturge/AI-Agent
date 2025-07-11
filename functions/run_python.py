import os
import subprocess

def run_python_file(working_directory, file_path):
    abs_directory = os.path.abspath(working_directory)
    abs_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file.startswith(f"{abs_directory}/") and not abs_file == abs_directory:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_file):
        return f'Error: File "{file_path}" not found.'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        subprocess_result = subprocess.run(["uv", "run", abs_file], capture_output=True, timeout=30, cwd= abs_directory)

        stdout = subprocess_result.stdout.decode()
        stderr = subprocess_result.stderr.decode()

        output = f"STDOUT:{stdout}\nSTDERR:{stderr}"

        if subprocess_result.returncode != 0:
            output += f"\nProcess exited with code {subprocess_result.returncode}"

        if stdout.strip() == "" and stderr.strip() == "":
            output = "No output produced."

        return output
    except Exception as e:
        f"Error: executing Python file: {e}"
