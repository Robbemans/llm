import os

def get_files_info(working_directory, directory="."):
    abs_working_directory = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(abs_working_directory, directory))

    valid_target_dir = os.path.commonpath([abs_working_directory, target_dir]) == abs_working_directory
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    elif not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    
    try:

        lines = []
        for item in os.listdir(target_dir):
            full_path = os.path.join(target_dir, item)
            lines.append(
                f"- {item}: file_size={os.path.getsize(full_path)}, is_dir={os.path.isdir(full_path)}"
            )
        return "\n".join(lines)
    except Exception as e:
        raise Exception(f"Error: {e}")