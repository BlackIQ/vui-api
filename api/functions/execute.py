import subprocess


def execute(script_path, *args):
    try:
        # Build the command to execute the script
        command = ['bash', script_path, *args]

        # Execute the script
        subprocess.run(command, check=True)

        return True
    except subprocess.CalledProcessError:
        # Script execution failed
        return False
