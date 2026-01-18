import os


def get_file_content(working_directory, file_path):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_file])
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    if valid_target_dir != working_dir_abs:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    try:
        with open(target_file, "r") as file:
            content = file.read(10000)
            return content
    except FileNotFoundError:
        print("The file was not found.")
    except PermissionError:
        print("You do not have permission to read the file.")
    except Exception as e:
        print(f"Something unexpected happend. Error: {e}")
