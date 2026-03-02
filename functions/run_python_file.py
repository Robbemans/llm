import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    abs_working_directory = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(abs_working_directory, file_path))

    in_working_dir = os.path.commonpath([abs_working_directory, target_file]) == abs_working_directory
    if not in_working_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    elif not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    elif not target_file.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    
    try:
        command = ["python", target_file]
        if args != None:
            command.extend(args)
        result = subprocess.run(command, capture_output=True, cwd = abs_working_directory, timeout=30, text=True)

        parts = []

        if result.returncode != 0:
            parts.append(f"Process exited with code {result.returncode}")

        stdout_text = (result.stdout or "").strip()
        stderr_text = (result.stderr or "").strip()

        if not stdout_text and not stderr_text:
            parts.append("No output produced")
        else:
            if stdout_text:
                parts.append(f"STDOUT:\n{stdout_text}")
            if stderr_text:
                parts.append(f"STDERR:\n{stderr_text}")

        return "\n".join(parts)

    except Exception as e:
        raise Exception(f"Error: executing Python file: {e}")

    