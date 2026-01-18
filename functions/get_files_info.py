import os


def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir])
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    if valid_target_dir != working_dir_abs:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    try:
        current_dir_data = []
        current_dir_contents = os.listdir(target_dir)
        for item in current_dir_contents:
            path = os.path.join(target_dir, item)
            # is_file = os.path.isfile(path)
            is_dir = os.path.isdir(path)
            size = os.path.getsize(path)
            current_dir_data.append(f"{item}: file_size={size} bytes, is_dir={is_dir}")
        result = "\n".join(current_dir_data)
        return result
    except Exception as e:
        return f"Unable to get the directory data, incurred Error: {e}"
