import os
from google.genai import types

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
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

