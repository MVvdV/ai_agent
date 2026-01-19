import os
import subprocess

from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_file])
    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if valid_target_dir != working_dir_abs:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if target_file[-3::] != ".py":
        return f'Error: "{file_path}" is not a Python file'

    command = ["python", target_file]
    if args is not None:
        command.extend(args)

    try:
        result = subprocess.run(
            command, capture_output=True, text=True, check=True, timeout=30
        )
        if result.returncode != 0:
            return f"Process exited with code {result.returncode}"
        if not result.stdout and not result.stderr:
            return "No output produced"
        return f"STDOUT: {result.stdout}, STDERR: {result.stderr}"
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"
    except subprocess.TimeoutExpired:
        return "Error: Process took too long to complete, Opperation terminated."
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes specified .py pyhton files from a specified file path with additional arguments as a subprocess and provides stdout and stderr results in a formatted string.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path and name to read the .py pyhton file to be executed in the subprocess, relative to the working directory (default is the working directory itself).",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="A list of specified arguments to be used in executing the specified .py python file from file_path",
            ),
        },
    ),
)
