import os

def get_file_content(working_directory, file_path):
    abs_working_directory = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(abs_working_directory, file_path))

    in_working_dir = os.path.commonpath([abs_working_directory, target_file]) == abs_working_directory
    if not in_working_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    elif not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        max_chars = 10000

        with open(target_file, "r") as f:
            file_content_string = f.read(max_chars)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {max_chars} characters]'
            print(file_content_string)

    except Exception as e:
        raise Exception(f"Error: {e}")
