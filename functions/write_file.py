import os


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
