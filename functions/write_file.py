import os

from google.genai import types


def write_file(working_directory, file_path, content):
    working_dir_abs = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_path])
    if os.path.isdir(target_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    if valid_target_dir != working_dir_abs:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        os.makedirs(valid_target_dir, exist_ok=True)
    except Exception as e:
        return f"An issue occured making the directories. Error: {e}"

    try:
        with open(target_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"An issue occured trying to write the file. Error: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes specified content as a string to a specified file, relative to the working directory, parent directories get created along with the file in accordance with the specified file path.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path and name to write the file to, relative to the working directory (default is the working directory itself).",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to be written to the specified file in file_path.",
            ),
        },
    ),
)
