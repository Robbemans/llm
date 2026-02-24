import os

def write_file(working_directory, file_path, content):
    abs_working_directory = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(abs_working_directory, file_path))

    in_working_dir = os.path.commonpath([abs_working_directory, target_file]) == abs_working_directory
    if not in_working_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    elif os.path.isdir(target_file):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    try:
        os.makedirs(abs_working_directory, mode=0o777, exist_ok=True)
        with open(target_file, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        raise Exception(f"Error: {e}")
